from __future__ import annotations


class HeuristicAgent:
    """Simple baseline policy. Replace with RL policy later."""

    def act(self, observation) -> list[float]:
        # Observation layout:
        # x, y, z, vx, vy, vz, yaw, distance_to_goal, lidar...
        lidar = observation[8:]
        min_left = min(lidar[: len(lidar) // 2]) if lidar else 1.0
        min_right = min(lidar[len(lidar) // 2 :]) if lidar else 1.0
        yaw = 0.0
        if min_left < 0.18:
            yaw = 0.5
        elif min_right < 0.18:
            yaw = -0.5
        return [0.8, 0.0, 0.0, yaw]
