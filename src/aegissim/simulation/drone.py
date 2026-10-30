from __future__ import annotations

from panda3d.core import Vec3

from aegissim.config import DroneConfig
from aegissim.utils.math_utils import clamp
from aegissim.world.procedural_assets import make_box


class Drone:
    def __init__(self, app, config: DroneConfig):
        self.app = app
        self.config = config
        self.node = app.render.attachNewNode("drone")
        self.visual = make_box("drone_body", (0.9, 0.9, 0.28), (0.1, 0.45, 1.0, 1))
        self.visual.reparentTo(self.node)
        self.velocity = Vec3(0, 0, 0)

    def spawn(self, position: Vec3) -> None:
        self.node.setPos(position)
        self.node.setH(0)
        self.velocity = Vec3(0, 0, 0)

    def apply_action(self, action, dt: float) -> None:
        forward, strafe, vertical, yaw = [clamp(float(a), -1.0, 1.0) for a in action]
        self.node.setH(self.node.getH() + yaw * self.config.yaw_speed * dt)

        quat = self.node.getQuat(self.app.render)
        forward_vec = quat.getForward()
        right_vec = quat.getRight()

        acceleration = (
            forward_vec * forward * self.config.acceleration
            + right_vec * strafe * self.config.acceleration
            + Vec3(0, 0, vertical * self.config.acceleration)
        )
        self.velocity += acceleration * dt

        horizontal = Vec3(self.velocity.x, self.velocity.y, 0)
        if horizontal.length() > self.config.max_speed:
            horizontal.normalize()
            horizontal *= self.config.max_speed
            self.velocity.x = horizontal.x
            self.velocity.y = horizontal.y

        self.velocity.z = clamp(self.velocity.z, -self.config.max_vertical_speed, self.config.max_vertical_speed)
        self.velocity *= 0.985

        new_pos = self.node.getPos() + self.velocity * dt
        new_pos.z = clamp(new_pos.z, 0.8, 4.5)
        self.node.setPos(new_pos)

    def get_state_vector(self) -> list[float]:
        pos = self.node.getPos()
        return [
            float(pos.x), float(pos.y), float(pos.z),
            float(self.velocity.x), float(self.velocity.y), float(self.velocity.z),
            float(self.node.getH()),
        ]
