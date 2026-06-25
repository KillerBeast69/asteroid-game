# 🚀 Asteroids

![Asteroids Game Preview](https://github.com/user-attachments/assets/c91461a7-7e34-450a-aaae-5e8a701ed527)

> A classic Asteroids arcade game built with Python and Pygame.

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=flat&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2.6.1-00C851?style=flat)
![Status](https://img.shields.io/badge/status-active-brightgreen)

---

## Overview

A faithful recreation of the classic Asteroids arcade game using Python and Pygame. The player pilots a triangular ship on a 1280×720 canvas, navigating an ever-growing field of spawning asteroids. Shooting a large asteroid splits it into two smaller, faster fragments; asteroids below the minimum radius are destroyed outright. A collision between any asteroid and the player ends the game. All gameplay events and per-second state snapshots are written to JSONL log files for post-game analysis.

---

## Key Features

- 🚀 **Player Ship** — Triangle-shaped sprite rendered from computed vertex geometry; controlled with WASD for directional thrust and rotation, SPACE to shoot
- 💥 **Asteroid Splitting** — A shot asteroid splits into two fragments rotated ±20–50° from the parent's velocity vector and scaled by 1.2× speed; asteroids at `ASTEROID_MIN_RADIUS` (20px) are destroyed without splitting
- 🌀 **Continuous Spawning** — `AsteroidField` spawns one asteroid every 0.8 seconds from a randomly selected screen edge at a random speed (40–100 units/s) with a randomised direction offset (±30°)
- 🎯 **Sprite Groups** — Pygame sprite groups (`updatable`, `drawable`, `asteroids_group`, `shots_group`) cleanly separate update, draw, and collision logic
- 🛡️ **Shoot Cooldown** — Player cannot fire more than once per 0.3 seconds to prevent shot spam
- 📊 **JSONL Event Logging** — `log_event()` records discrete gameplay events (`asteroid_shot`, `asteroid_split`, `player_hit`) with timestamps, elapsed seconds, and frame count to `game_events.jsonl`
- 📈 **JSONL State Logging** — `log_state()` captures position, velocity, radius, and rotation for all sprites once per second (for up to 16 seconds) to `game_state.jsonl`
- 🧱 **OOP Architecture** — `CircleShape` base class provides shared position, velocity, radius fields, and a `collides_with()` method (Euclidean distance ≤ sum of radii) for all game objects

---

## Tech Stack

| Technology | Role |
|---|---|
| Python 3.13 | Primary language |
| `pygame 2.6.1` | Game loop, display, input handling, and sprite system |
| `pygame.Vector2` | 2D vector maths for position, velocity, and rotation |
| `json`, `inspect`, `datetime` | JSONL state and event logging |
| `random` | Asteroid spawn randomisation and split angles |

---

## Installation

**Prerequisites:** Python 3.13+, and either `uv` or `pip`

```bash
# 1. Clone the repository
git clone https://github.com/your-username/asteroids.git
cd asteroids/asteroids-game

# 2. Install dependencies with uv (recommended)
uv sync

# Or with pip
pip install pygame==2.6.1
```

---

## Usage

```bash
# Launch the game
python main.py
```

### Controls

| Key | Action |
|-----|--------|
| `W` | Thrust forward |
| `S` | Thrust backward |
| `A` | Rotate left |
| `D` | Rotate right |
| `SPACE` | Fire a shot |

The game runs at 60 FPS on a 1280×720 black canvas. It ends when an asteroid collides with the player, printing `"Game over!"` to stdout and exiting.

### Game Constants (`constants.py`)

| Constant | Value | Description |
|---|---|---|
| `SCREEN_WIDTH` / `SCREEN_HEIGHT` | 1280 / 720 | Display resolution |
| `PLAYER_RADIUS` | 20 | Collision radius of the ship |
| `PLAYER_SPEED` | 200 | Thrust speed (units/s) |
| `PLAYER_TURN_SPEED` | 300 | Rotation speed (degrees/s) |
| `PLAYER_SHOOT_SPEED` | 500 | Shot travel speed (units/s) |
| `PLAYER_SHOOT_COOLDOWN_SECONDS` | 0.3 | Minimum time between shots |
| `ASTEROID_MIN_RADIUS` | 20 | Smallest asteroid; destroyed without splitting |
| `ASTEROID_KINDS` | 3 | Number of asteroid size tiers |
| `ASTEROID_SPAWN_RATE_SECONDS` | 0.8 | Seconds between spawns |

### Log Files

After each run, two JSONL files are written to the working directory:

- **`game_events.jsonl`** — One JSON object per line for each discrete event:
  ```json
  {"timestamp": "14:32:11.456", "elapsed_s": 5, "frame": 312, "type": "asteroid_shot"}
  {"timestamp": "14:32:11.501", "elapsed_s": 5, "frame": 315, "type": "asteroid_split"}
  ```

- **`game_state.jsonl`** — One JSON object per second (up to 16s) with sprite positions, velocities, and radii:
  ```json
  {"timestamp": "14:32:12.000", "elapsed_s": 6, "frame": 360, "screen_size": [1280, 720], ...}
  ```

---

## Project Structure

```
asteroids-game/
├── main.py           # Game loop: init, sprite group setup, event polling, collision detection
├── player.py         # Player: triangle geometry, WASD movement, shoot cooldown, Shot spawning
├── asteroid.py       # Asteroid: circular sprite, update (drift), split() with fragment spawning
├── asteroidfield.py  # AsteroidField: edge-based spawner with timer and random parameters
├── shot.py           # Shot: circular projectile that drifts in a straight line each frame
├── circleshape.py    # Abstract base class: position, velocity, radius, collides_with()
├── constants.py      # All tuneable game constants in one place
├── logger.py         # log_state() + log_event(): JSONL writers with frame-count sampling
└── pyproject.toml    # Project metadata and pygame dependency
```

**Inheritance hierarchy:**
```
pygame.sprite.Sprite
    └── CircleShape
            ├── Player
            ├── Asteroid
            └── Shot
```

**Collision logic in `main.py`:**
- Each frame, all asteroids are checked against the player (`collides_with`) → game over on hit
- All asteroids are checked against all shots (`collides_with`) → `ast.split()` + `shot.kill()` on hit

---

## Contributing

New game entities should subclass `CircleShape` and be added to the appropriate sprite groups in `main.py`. Game balance values (speeds, radii, spawn rates, cooldowns) are centralised in `constants.py`. Pull requests introducing new mechanics should not alter the existing `split()` or `collides_with()` logic without updating both `asteroid.py` and the collision loop in `main.py`.

---
