from __future__ import annotations

import logging
from panda3d.core import Vec3

from aegissim.config import AppConfig
from aegissim.simulation.reward import compute_reward

logger = logging.getLogger(__name__)


class EpisodeManager:
    def __init__(self, app, config: AppConfig, drone, world, lidar, telemetry):
        self.app = app
        self.config = config
        self.drone = drone
        self.world = world
        self.lidar = lidar
        self.telemetry = telemetry
        self.step_count = 0
        self.done = False
        self.total_reward = 0.0
        self.previous_distance = self._distance_to_goal()

        self.keys = {
            "w": False, "s": False, "a": False, "d": False,
            "q": False, "e": False, "arrow_left": False, "arrow_right": False,
        }
        for key in self.keys:
            app.accept(key, self._set_key, [key, True])
            app.accept(f"{key}-up", self._set_key, [key, False])
        app.accept("r", self.reset)
        app.accept("l", self.lidar.toggle_debug)

    def _set_key(self, key: str, value: bool) -> None:
        self.keys[key] = value

    def _distance_to_goal(self) -> float:
        return float((self.drone.node.getPos() - self.world.goal_position).length())

    def _manual_action(self) -> list[float]:
        return [
            float(self.keys["w"]) - float(self.keys["s"]),
            float(self.keys["d"]) - float(self.keys["a"]),
            float(self.keys["e"]) - float(self.keys["q"]),
            float(self.keys["arrow_right"]) - float(self.keys["arrow_left"]),
        ]

    def update(self, dt: float) -> None:
        if self.done:
            return
        obs, reward, done, info = self.step(self._manual_action(), dt)
        if done:
            logger.info("Episode done reward=%.3f info=%s", self.total_reward, info)

    def step(self, action, dt: float):
        if self.done:
            lidar = self.lidar.scan()
            return self.get_observation(lidar, self._distance_to_goal()), 0.0, True, {"already_done": True}

        self.drone.apply_action(action, dt)
        lidar = self.lidar.scan()
        current_distance = self._distance_to_goal()
        collided = self.world.check_sphere_collision(self.drone.node.getPos(), self.config.drone.radius)
        reached_goal = current_distance < 2.5
        min_lidar = float(lidar.min()) if len(lidar) else 1.0

        reward = compute_reward(
            previous_distance=self.previous_distance,
            current_distance=current_distance,
            collided=collided,
            reached_goal=reached_goal,
            altitude=float(self.drone.node.getZ()),
            min_lidar_fraction=min_lidar,
        )

        self.previous_distance = current_distance
        self.total_reward += reward
        self.step_count += 1

        timeout = self.step_count >= self.config.simulation.max_episode_steps
        self.done = bool(collided or reached_goal or timeout)

        obs = self.get_observation(lidar, current_distance)
        info = {
            "distance_to_goal": current_distance,
            "collided": collided,
            "reached_goal": reached_goal,
            "timeout": timeout,
            "step": self.step_count,
            "total_reward": self.total_reward,
            "min_lidar": min_lidar,
        }
        self.telemetry.record(self.step_count, reward, self.total_reward, info)
        return obs, reward, self.done, info

    def get_observation(self, lidar, distance_to_goal: float) -> list[float]:
        state = self.drone.get_state_vector()
        return state + [float(distance_to_goal)] + lidar.astype(float).tolist()

    def reset(self):
        self.drone.spawn(Vec3(*self.config.drone.start_position))
        self.step_count = 0
        self.done = False
        self.total_reward = 0.0
        self.previous_distance = self._distance_to_goal()
        return self.get_observation(self.lidar.scan(), self.previous_distance)
