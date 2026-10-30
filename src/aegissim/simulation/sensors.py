from __future__ import annotations

import math
import numpy as np
from panda3d.core import LineSegs, NodePath, Vec3

from aegissim.config import SensorConfig
from aegissim.utils.math_utils import heading_to_direction_xy, ray_intersects_aabb_2d


class LidarSensor:
    def __init__(self, app, drone, world, config: SensorConfig, debug_enabled: bool):
        self.app = app
        self.drone = drone
        self.world = world
        self.config = config
        self.debug_enabled = debug_enabled
        self.debug_node: NodePath | None = None

    def toggle_debug(self) -> None:
        self.debug_enabled = not self.debug_enabled
        if not self.debug_enabled and self.debug_node is not None:
            self.debug_node.removeNode()
            self.debug_node = None

    def scan(self) -> np.ndarray:
        origin_v = self.drone.node.getPos() + Vec3(0, 0, self.config.lidar_height_offset)
        origin = (float(origin_v.x), float(origin_v.y), float(origin_v.z))
        heading = float(self.drone.node.getH())
        distances = np.ones(self.config.lidar_rays, dtype=np.float32) * self.config.lidar_range

        hit_points: list[tuple[float, float, float]] = []

        for i in range(self.config.lidar_rays):
            local_angle = 2.0 * math.pi * i / self.config.lidar_rays
            dx, dy = heading_to_direction_xy(heading, local_angle)
            best = self.config.lidar_range
            for box in self.world.obstacles:
                hit = ray_intersects_aabb_2d(origin, (dx, dy), box, self.config.lidar_range)
                if hit is not None and hit < best:
                    best = hit
            distances[i] = best
            hit_points.append((origin[0] + dx * best, origin[1] + dy * best, origin[2]))

        if self.debug_enabled:
            self._draw_debug(origin, hit_points, distances)

        return distances / self.config.lidar_range

    def _draw_debug(self, origin: tuple[float, float, float], hit_points, distances) -> None:
        if self.debug_node is not None:
            self.debug_node.removeNode()
        segs = LineSegs("lidar_debug")
        segs.setThickness(1.2)
        for pt, dist in zip(hit_points, distances):
            if dist < self.config.lidar_range:
                segs.setColor(1, 0.2, 0.1, 1)
            else:
                segs.setColor(0.1, 0.7, 1, 0.35)
            segs.moveTo(*origin)
            segs.drawTo(*pt)
        self.debug_node = self.app.render.attachNewNode(segs.create())
