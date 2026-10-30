from __future__ import annotations

from panda3d.core import Vec3

from aegissim.config import AppConfig
from aegissim.utils.math_utils import AABB, sphere_intersects_aabb
from aegissim.world.procedural_assets import make_box, make_floor


class WarehouseWorld:
    def __init__(self, app, config: AppConfig):
        self.app = app
        self.config = config
        self.root = app.render.attachNewNode("warehouse")
        self.goal_position = Vec3(0, 30, 1)
        self.obstacles: list[AABB] = []

    def build(self) -> None:
        sim = self.config.simulation
        floor = make_floor(sim.warehouse_width, sim.warehouse_depth)
        floor.reparentTo(self.root)
        self._build_boundary_walls(sim.warehouse_width, sim.warehouse_depth)
        self._build_shelves(sim.shelf_rows, sim.shelves_per_row, sim.warehouse_width)
        self._build_goal_pad()

    def _add_obstacle(
        self,
        name: str,
        pos: tuple[float, float, float],
        scale: tuple[float, float, float],
        color: tuple[float, float, float, float],
    ):
        node = make_box(name, scale, color)
        node.setPos(*pos)
        node.reparentTo(self.root)
        self.obstacles.append(
            AABB(
                name=name,
                center=(float(pos[0]), float(pos[1]), float(pos[2])),
                half_extents=(float(scale[0]) / 2.0, float(scale[1]) / 2.0, float(scale[2]) / 2.0),
            )
        )
        return node

    def _build_boundary_walls(self, width: float, depth: float) -> None:
        wall_height = 5.0
        wall_thickness = 0.4
        color = (0.35, 0.35, 0.38, 1)
        self._add_obstacle("wall_left", (-width / 2, 0, wall_height / 2), (wall_thickness, depth, wall_height), color)
        self._add_obstacle("wall_right", (width / 2, 0, wall_height / 2), (wall_thickness, depth, wall_height), color)
        self._add_obstacle("wall_back", (0, -depth / 2, wall_height / 2), (width, wall_thickness, wall_height), color)
        self._add_obstacle("wall_front", (0, depth / 2, wall_height / 2), (width, wall_thickness, wall_height), color)

    def _build_shelves(self, rows: int, per_row: int, width: float) -> None:
        start_y = -22.0
        row_spacing = 8.0
        shelf_spacing_x = width / float(per_row + 1)
        for r in range(rows):
            y = start_y + r * row_spacing
            for i in range(per_row):
                x = -width / 2 + shelf_spacing_x * (i + 1)
                self._add_obstacle(
                    name=f"shelf_{r}_{i}",
                    pos=(x, y, 1.5),
                    scale=(2.0, 5.5, 3.0),
                    color=(0.55, 0.36, 0.16, 1),
                )

    def _build_goal_pad(self) -> None:
        goal = make_box("goal_pad", (4.0, 4.0, 0.15), (0.1, 0.8, 0.25, 1))
        goal.setPos(self.goal_position)
        goal.reparentTo(self.root)

    def check_sphere_collision(self, center: Vec3, radius: float) -> bool:
        c = (center.x, center.y, center.z)
        return any(sphere_intersects_aabb(c, radius, box) for box in self.obstacles)
