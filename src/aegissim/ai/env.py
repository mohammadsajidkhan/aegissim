from __future__ import annotations

import numpy as np

from aegissim.app import AegisSimApp
from aegissim.config import load_config


class AegisSimEnv:
    """Small Gym-like wrapper for local AI experiments."""

    def __init__(self, config_path: str = "config/default.toml"):
        self.config = load_config(config_path)
        self.app = AegisSimApp(self.config)

    def reset(self) -> np.ndarray:
        obs = self.app.episode.reset()
        self.app.taskMgr.step()
        return np.asarray(obs, dtype=np.float32)

    def step(self, action):
        obs, reward, done, info = self.app.episode.step(action, self.config.simulation.fixed_dt)
        self.app.taskMgr.step()
        return np.asarray(obs, dtype=np.float32), float(reward), bool(done), info

    def close(self) -> None:
        self.app.telemetry.flush()
        self.app.destroy()
