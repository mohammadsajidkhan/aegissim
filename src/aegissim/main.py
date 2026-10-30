from __future__ import annotations

import argparse

from aegissim.app import AegisSimApp
from aegissim.config import load_config
from aegissim.logging_setup import configure_logging


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run AegisSim Panda3D simulator")
    parser.add_argument("--config", default="config/default.toml", help="Path to TOML config")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    configure_logging()
    config = load_config(args.config)
    app = AegisSimApp(config)
    app.run()


if __name__ == "__main__":
    main()
