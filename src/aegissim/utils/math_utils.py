from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class AABB:
    name: str
    center: tuple[float, float, float]
    half_extents: tuple[float, float, float]

    @property
    def min(self) -> tuple[float, float, float]:
        return tuple(c - h for c, h in zip(self.center, self.half_extents))

    @property
    def max(self) -> tuple[float, float, float]:
        return tuple(c + h for c, h in zip(self.center, self.half_extents))


def clamp(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def sphere_intersects_aabb(center: tuple[float, float, float], radius: float, box: AABB) -> bool:
    mins = box.min
    maxs = box.max
    sq_dist = 0.0
    for i in range(3):
        v = center[i]
        if v < mins[i]:
            sq_dist += (mins[i] - v) ** 2
        elif v > maxs[i]:
            sq_dist += (v - maxs[i]) ** 2
    return sq_dist <= radius * radius


def ray_intersects_aabb_2d(
    origin: tuple[float, float, float],
    direction_xy: tuple[float, float],
    box: AABB,
    max_distance: float,
) -> float | None:
    """Return hit distance for a horizontal ray against an AABB, or None."""
    ox, oy, oz = origin
    dx, dy = direction_xy
    mins = box.min
    maxs = box.max

    if oz < mins[2] or oz > maxs[2]:
        return None

    tmin = 0.0
    tmax = max_distance

    for axis, o, d in ((0, ox, dx), (1, oy, dy)):
        minv = mins[axis]
        maxv = maxs[axis]
        if abs(d) < 1e-8:
            if o < minv or o > maxv:
                return None
        else:
            inv = 1.0 / d
            t1 = (minv - o) * inv
            t2 = (maxv - o) * inv
            if t1 > t2:
                t1, t2 = t2, t1
            tmin = max(tmin, t1)
            tmax = min(tmax, t2)
            if tmin > tmax:
                return None

    if 0.0 <= tmin <= max_distance:
        return tmin
    return None


def heading_to_direction_xy(heading_degrees: float, local_angle_radians: float = 0.0) -> tuple[float, float]:
    angle = math.radians(heading_degrees) + local_angle_radians
    return math.sin(angle), math.cos(angle)
