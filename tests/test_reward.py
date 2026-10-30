from aegissim.simulation.reward import compute_reward


def test_reaching_goal_reward():
    assert compute_reward(10, 0.5, False, True, 2.0, 1.0) == 10.0


def test_collision_penalty():
    assert compute_reward(10, 9, True, False, 2.0, 0.1) == -10.0


def test_progress_reward_positive():
    reward = compute_reward(10, 8, False, False, 2.0, 1.0)
    assert reward > 0
