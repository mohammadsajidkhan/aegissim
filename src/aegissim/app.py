from __future__ import annotations

import logging

from direct.showbase.ShowBase import ShowBase
from panda3d.core import loadPrcFileData, Vec3, AmbientLight, DirectionalLight

from aegissim.config import AppConfig
from aegissim.rendering.camera import FollowCamera
from aegissim.rendering.performance import PerformanceManager
from aegissim.simulation.drone import Drone
from aegissim.simulation.episode import EpisodeManager
from aegissim.simulation.sensors import LidarSensor
from aegissim.telemetry.recorder import TelemetryRecorder
from aegissim.world.warehouse import WarehouseWorld

logger = logging.getLogger(__name__)


class AegisSimApp(ShowBase):
    def __init__(self, config: AppConfig):
        self.config = config
        self._configure_panda()
        super().__init__()

        self.disableMouse()
        self.accept("escape", self.userExit)

        self.performance = PerformanceManager(self, config)
        self.performance.apply()
        self._setup_lighting()

        self.world = WarehouseWorld(self, config)
        self.world.build()

        self.drone = Drone(self, config.drone)
        self.drone.spawn(Vec3(*config.drone.start_position))

        self.lidar = LidarSensor(
            app=self,
            drone=self.drone,
            world=self.world,
            config=config.sensors,
            debug_enabled=config.graphics.enable_debug_lidar,
        )

        self.telemetry = TelemetryRecorder()
        self.episode = EpisodeManager(
            app=self,
            config=config,
            drone=self.drone,
            world=self.world,
            lidar=self.lidar,
            telemetry=self.telemetry,
        )
        self.camera_controller = FollowCamera(self, self.drone.node)

        self.taskMgr.add(self._update, "aegissim_update")
        logger.info("AegisSim initialized")

    def _configure_panda(self) -> None:
        w = self.config.window
        g = self.config.graphics
        loadPrcFileData("", f"win-size {w.width} {w.height}")
        loadPrcFileData("", f"window-title {w.title}")
        loadPrcFileData("", f"sync-video {'1' if g.vsync else '0'}")
        loadPrcFileData("", "show-frame-rate-meter false")
        if w.fullscreen:
            loadPrcFileData("", "fullscreen true")
        if self.config.training.headless:
            loadPrcFileData("", "window-type offscreen")

    def _setup_lighting(self) -> None:
        ambient = AmbientLight("ambient_light")
        ambient.setColor((0.35, 0.35, 0.38, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)

        directional = DirectionalLight("sun_key_light")
        directional.setColor((0.85, 0.85, 0.8, 1))
        directional_np = self.render.attachNewNode(directional)
        directional_np.setHpr(-35, -50, 0)
        self.render.setLight(directional_np)

    def _update(self, task):
        dt = min(globalClock.getDt(), self.config.simulation.fixed_dt * 2.0)
        self.episode.update(dt)
        self.camera_controller.update(dt)
        self.performance.update()
        return task.cont
