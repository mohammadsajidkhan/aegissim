from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib  # Python 3.11+
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


@dataclass(frozen=True)
class WindowConfig:
    width: int
    height: int
    fullscreen: bool
    title: str


@dataclass(frozen=True)
class GraphicsConfig:
    vsync: bool
    show_fps: bool
    quality: str
    enable_debug_lidar: bool
    background_color: tuple[float, float, float, float]


@dataclass(frozen=True)
class SimulationConfig:
    fixed_dt: float
    max_episode_steps: int
    seed: int
    warehouse_width: float
    warehouse_depth: float
    shelf_rows: int
    shelves_per_row: int


@dataclass(frozen=True)
class DroneConfig:
    mass: float
    max_speed: float
    max_vertical_speed: float
    acceleration: float
    yaw_speed: float
    radius: float
    start_position: tuple[float, float, float]


@dataclass(frozen=True)
class SensorConfig:
    lidar_rays: int
    lidar_range: float
    lidar_height_offset: float


@dataclass(frozen=True)
class TrainingConfig:
    headless: bool
    domain_randomization: bool


@dataclass(frozen=True)
class AppConfig:
    window: WindowConfig
    graphics: GraphicsConfig
    simulation: SimulationConfig
    drone: DroneConfig
    sensors: SensorConfig
    training: TrainingConfig


def _as_tuple(values: list[float] | tuple[float, ...]) -> tuple[float, ...]:
    return tuple(float(v) for v in values)


def _load_toml(path: Path) -> dict[str, Any]:
    with path.open("rb") as f:
        return tomllib.load(f)


def load_config(path: str | Path) -> AppConfig:
    data = _load_toml(Path(path))

    return AppConfig(
        window=WindowConfig(**data["window"]),
        graphics=GraphicsConfig(
            **{
                **data["graphics"],
                "background_color": _as_tuple(data["graphics"]["background_color"]),
            }
        ),
        simulation=SimulationConfig(**data["simulation"]),
        drone=DroneConfig(
            **{
                **data["drone"],
                "start_position": _as_tuple(data["drone"]["start_position"]),
            }
        ),
        sensors=SensorConfig(**data["sensors"]),
        training=TrainingConfig(**data["training"]),
    )
