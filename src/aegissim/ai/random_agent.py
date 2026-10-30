from __future__ import annotations

import random


class RandomAgent:
    def act(self, observation) -> list[float]:
        return [
            random.uniform(-1.0, 1.0),
            random.uniform(-1.0, 1.0),
            random.uniform(-0.35, 0.35),
            random.uniform(-0.6, 0.6),
        ]
