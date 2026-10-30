from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class TelemetryRecorder:
    def __init__(self, path: str = "telemetry/episode_metrics.csv"):
        self.path = Path(path)
        self.path.parent.mkdir(exist_ok=True)
        self.rows: list[dict[str, Any]] = []

    def record(self, step: int, reward: float, total_reward: float, info: dict[str, Any]) -> None:
        self.rows.append(
            {
                "step": step,
                "reward": reward,
                "total_reward": total_reward,
                "distance_to_goal": info.get("distance_to_goal"),
                "collided": info.get("collided"),
                "reached_goal": info.get("reached_goal"),
                "timeout": info.get("timeout"),
                "min_lidar": info.get("min_lidar"),
            }
        )
        if len(self.rows) >= 250:
            self.flush()

    def flush(self) -> None:
        if not self.rows:
            return
        write_header = not self.path.exists()
        with self.path.open("a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(self.rows[0].keys()))
            if write_header:
                writer.writeheader()
            writer.writerows(self.rows)
        self.rows.clear()
