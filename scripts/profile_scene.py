from __future__ import annotations

from aegissim.config import load_config


def main():
    cfg = load_config("config/default.toml")
    static_obstacle_count = 4 + cfg.simulation.shelf_rows * cfg.simulation.shelves_per_row
    print("AegisSim Scene Profile")
    print(f"warehouse_width={cfg.simulation.warehouse_width}")
    print(f"warehouse_depth={cfg.simulation.warehouse_depth}")
    print(f"shelf_rows={cfg.simulation.shelf_rows}")
    print(f"shelves_per_row={cfg.simulation.shelves_per_row}")
    print(f"static_obstacle_count={static_obstacle_count}")
    print(f"lidar_rays={cfg.sensors.lidar_rays}")


if __name__ == "__main__":
    main()
