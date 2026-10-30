from __future__ import annotations


def compute_reward(
    previous_distance: float,
    current_distance: float,
    collided: bool,
    reached_goal: bool,
    altitude: float,
    min_lidar_fraction: float,
) -> float:
    if reached_goal:
        return 10.0
    if collided:
        return -10.0

    reward = -0.01
    progress = previous_distance - current_distance
    reward += progress * 0.2

    if altitude < 1.0 or altitude > 4.2:
        reward -= 0.05
    if min_lidar_fraction < 0.12:
        reward -= 0.1

    return float(reward)
