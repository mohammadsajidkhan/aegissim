from __future__ import annotations

from panda3d.core import Vec3


class FollowCamera:
    def __init__(self, app, target):
        self.app = app
        self.target = target
        self.offset = Vec3(0, -12, 7)

    def update(self, dt: float) -> None:
        target_pos = self.target.getPos()
        desired = target_pos + self.offset
        current = self.app.camera.getPos()
        smoothed = current + (desired - current) * min(1.0, dt * 5.0)
        self.app.camera.setPos(smoothed)
        self.app.camera.lookAt(target_pos)
