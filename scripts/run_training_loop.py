from __future__ import annotations

import argparse

from aegissim.ai.env import AegisSimEnv
from aegissim.ai.random_agent import RandomAgent
from aegissim.logging_setup import configure_logging


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/default.toml")
    parser.add_argument("--episodes", type=int, default=5)
    return parser.parse_args()


def main():
    args = parse_args()
    configure_logging()
    env = AegisSimEnv(args.config)
    agent = RandomAgent()

    try:
        for ep in range(args.episodes):
            obs = env.reset()
            total = 0.0
            info = {}
            for _ in range(env.config.simulation.max_episode_steps):
                action = agent.act(obs)
                obs, reward, done, info = env.step(action)
                total += reward
                if done:
                    break
            print(f"episode={ep} total_reward={total:.3f} info={info}")
    finally:
        env.close()


if __name__ == "__main__":
    main()
