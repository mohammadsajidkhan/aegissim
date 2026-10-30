# AegisSim — Panda3D Warehouse Drone AI Simulator

AegisSim is a **local-first Panda3D project** for building a production-style 3D simulation environment for AI training. It focuses on a warehouse drone navigation task with procedural 3D environments, simulation logic, LiDAR-style sensing, episode management, reward shaping, telemetry, and a Gym-like Python API.

This repository is designed to help you build practical skills in:

- Designing and developing 3D simulations in **Panda3D**.
- Building AI-training-friendly simulation APIs.
- Writing advanced, modular Python.
- Understanding 3D scene structure, simulation loops, sensors, and reward logic.
- Optimizing environments for different hardware profiles.
- Maintaining cross-platform project structure for Windows, Linux, and macOS.

> Note: This project uses procedural geometry, so you can run it without downloading external 3D assets.

---

## 1. What You Will Build

You will run a warehouse simulation where a drone must navigate from a spawn point to a delivery goal while avoiding shelves and walls.

The project includes:

- Panda3D app shell.
- Procedural warehouse generation.
- Drone movement system.
- LiDAR-style ray sensor.
- Collision checks using sphere-vs-AABB logic.
- Reward and episode management.
- Human keyboard control.
- Random AI agent loop.
- Headless-friendly configuration.
- Telemetry CSV logging.
- Performance quality presets.
- Unit tests for core simulation logic.

---

## 2. Repository Structure

```text
aegissim-panda3d-ai-simulator/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── config/
│   ├── default.toml
│   ├── graphics_low.toml
│   ├── graphics_high.toml
│   └── training_headless.toml
├── scripts/
│   ├── run_sim.py
│   ├── run_training_loop.py
│   └── profile_scene.py
├── src/
│   └── aegissim/
│       ├── __init__.py
│       ├── main.py
│       ├── app.py
│       ├── config.py
│       ├── logging_setup.py
│       ├── ai/
│       ├── rendering/
│       ├── simulation/
│       ├── telemetry/
│       ├── utils/
│       └── world/
└── tests/
```

---

## 3. Prerequisites

Install:

- Python **3.10+**
- pip
- A GPU/graphics driver capable of running Panda3D locally

Recommended Python versions: 3.10, 3.11, or 3.12.

---

## 4. Getting Started

### Step 1 — Clone or unzip this repository

If you downloaded the ZIP, extract it and enter the project directory:

```bash
cd aegissim-panda3d-ai-simulator
```

### Step 2 — Create a virtual environment

#### Windows PowerShell

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

#### Windows CMD

```bash
python -m venv .venv
.venv\Scripts\activate.bat
```

#### Linux/macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3 — Upgrade pip

```bash
python -m pip install --upgrade pip
```

### Step 4 — Install the project

```bash
pip install -e .
```

This installs the local package and dependencies from `pyproject.toml`.

---

## 5. Run the 3D Simulator

```bash
python scripts/run_sim.py
```

Or:

```bash
python -m aegissim.main --config config/default.toml
```

### Controls

```text
W / S       move forward / backward
A / D       strafe left / right
E / Q       ascend / descend
Left/Right  yaw left / right
R           reset episode
L           toggle LiDAR debug lines
Esc         quit
```

---

## 6. Run with Graphics Presets

Low graphics mode:

```bash
python -m aegissim.main --config config/graphics_low.toml
```

High graphics mode:

```bash
python -m aegissim.main --config config/graphics_high.toml
```

Headless/offscreen training-style mode:

```bash
python scripts/run_training_loop.py --config config/training_headless.toml
```

> If offscreen mode does not work on your machine, use `config/default.toml` for visible-window training.

---

## 7. Run the Random AI Agent

```bash
python scripts/run_training_loop.py
```

This runs a simple random policy using a Gym-like environment interface:

```python
obs = env.reset()
obs, reward, done, info = env.step(action)
```

The observation includes:

```text
drone position
velocity
yaw
distance to goal
normalized LiDAR distances
```

The action is:

```text
[forward_thrust, strafe_thrust, vertical_thrust, yaw_rate]
```

Each action value should be in `[-1, 1]`.

---

## 8. Run Tests

```bash
pytest
```

Tests cover:

- Reward shaping.
- Math utilities.
- Configuration loading.
- Collision primitives.

---

## 9. Run Scene Profiler

```bash
python scripts/profile_scene.py
```

This prints basic scene metrics such as obstacle count and warehouse size.

---

## 10. Important Config Files

### `config/default.toml`

Main visible simulator configuration.

### `config/graphics_low.toml`

Lower render overhead:

- no vsync
- no debug LiDAR
- lower resolution

### `config/graphics_high.toml`

Higher visual quality:

- larger resolution
- debug LiDAR enabled
- antialiasing enabled

### `config/training_headless.toml`

Useful for AI training loops:

- offscreen mode
- debug visuals disabled
- fixed simulation timestep

---

## 11. Development Roadmap

Recommended implementation milestones:

### Phase 1 — Core Simulator

- Run Panda3D window.
- Generate warehouse.
- Move drone manually.
- Reset episodes.

### Phase 2 — Sensors and AI API

- LiDAR-style range sensor.
- Observation vector.
- Reward logic.
- Random agent.

### Phase 3 — Production Hardening

- Telemetry CSV recording.
- Test coverage.
- Config profiles.
- Logging.
- Performance presets.

### Phase 4 — Advanced Extensions

- Gymnasium integration.
- Render-to-texture camera observations.
- Moving obstacles.
- Domain randomization.
- Scenario files.
- Optimized glTF assets.
- LOD and batching.

---

## 12. Asset Optimization Guidelines

When replacing procedural boxes with real assets:

```text
Shelf:
  triangles: < 1,000
  texture: 512x512 or 1024x1024
  collision: simple AABB or low-poly proxy

Drone:
  triangles: < 5,000
  texture: 1024x1024
  collision: sphere or capsule proxy

Warehouse floor/walls:
  use simple geometry
  prefer tiled textures
  avoid unnecessary subdivisions

Repeated props:
  instance or batch when possible
  keep materials shared
```

Performance priorities:

1. Keep collision meshes simple.
2. Disable debug drawing during training.
3. Use low graphics preset for weaker hardware.
4. Avoid high-resolution textures unless required.
5. Batch repeated static geometry where possible.

---

## 13. Troubleshooting

### Panda3D window does not open

Try:

```bash
python -m pip install --upgrade panda3d
```

Also update your GPU drivers.

### Import error for `aegissim`

Install the package in editable mode:

```bash
pip install -e .
```

### Offscreen/headless mode fails

Use visible mode instead:

```bash
python scripts/run_training_loop.py --config config/default.toml
```

### Simulation is slow

Use low graphics:

```bash
python -m aegissim.main --config config/graphics_low.toml
```

---

## 14. Portfolio Description

You can describe this project as:

> Built AegisSim, a Panda3D-based 3D warehouse drone simulation platform for AI training. Designed a modular Python architecture with procedural environment generation, real-time drone movement, LiDAR-style sensing, collision detection, reward shaping, telemetry logging, cross-platform configuration, graphics quality presets, and a Gym-like reinforcement learning interface.

---

## 15. License

MIT License. See `LICENSE`.
