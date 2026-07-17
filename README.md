*This project has been created as part of the 42 curriculum by qdecross, stmaire.*

<div align="center">
<br>
  <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQPzuYKu7n0cWUYa5Kbg0_LrlEQAIURWeo9A&s" alt="42 Logo" width="400" />
  <br>
</div>

# Pac-Man
![Language](https://img.shields.io/badge/Language-python-blue)
![Static Badge](https://img.shields.io/badge/Gaming-green)
![Static Badge](https://img.shields.io/badge/Maze-green)
![Static Badge](https://img.shields.io/badge/Group_&_interpersonal-pink)
![Static Badge](https://img.shields.io/badge/Algorithms_&_IA-pink)
![Static Badge](https://img.shields.io/badge/Object_oriented_programming-pink)
![Static Badge](https://img.shields.io/badge/Graphics-pink)

## 🔵 Description

### ✳️ Goal
The goal of this project is to recreate the classic 1980 arcade game, Pac-Man. It requires building a complete and playable game using Python 3.10 or later. The code is designed around Object-Oriented Programming (OOP) to ensure a modular and reusable architecture.

### ✳️ Overview
This project delivers a modern Pac-Man experience with the following core features:
- Dynamic Levels: The game mazes are generated using an external 'A-Maze-ing' package.
- Custom Configuration: Game parameters (like time, lives, and points) are loaded from a JSON configuration file. The program includes robust error handling to ensure the game never crashes, even if the file is faulty.
- Classic Gameplay: The player navigates the maze to eat pacgums (small dots) and super-pacgums (power pellets).
- Ghost AI: Four ghosts move autonomously through the corridors. They actively chase the player, but they will run away when the player eats a super-pacgum.
- User Interface: The game features a polished UI with a Main Menu, an in-game HUD (displaying score, lives, and time), a Pause Menu, and a Game Over screen.
- Highscores: A persistent highscore system saves and displays the top 10 player scores.
- Testing Tools: A special cheat mode (including invincibility, level skip, and ghost freeze) is included to make peer reviews and testing easier.
- Deployment: The final game is fully packaged and ready to be deployed on a public gaming platform like Steam or Itch.io. **TODO  precise platform**
- **TODO  graphical library**

## 🔵 Instructions

### ✳️ Prerequisites
- Python 3.10 or later
- uv (high-performance Python package manager)

### ✳️ Installation

The project uses uv for dependency management and isolation. To set up the environment and install necessary packages (pydantic, flake8, mypy, pytest) **TODO  graphical library**:

```bash
# Install dependencies and create virtual environment
uv sync
```

Or using the Makefile:

```bash
make install
```
### ✳️ Execution

**1. Run the Simulation (Recommended)**

```bash
make run
```

**2. Manual Execution via uv**
It takes exactly one argument: a configuration file. The filename file does
not matter, but the file must be a json file.

```bash
uv run python3 pac-man.py config.json
```
**3. Code Quality & Linting**

In accordance with the 42 curriculum standards, the project adheres to strict coding rules using flake8 and mypy for PEP 8 compliance and type safety.

```bash
# Standard linting
make lint

# Strict type checking
make lint-strict
```

**4. Debugging**

Run with Python debugger (pdb):

```bash
make debug
```

**5. Testing**

Run the test suite (not graded but verifies core logic):

```bash
make test
```

**6. Cleanup**

Remove cache and temporary files:

```bash
make clean
```
## 🔵 Configuration
### ✳️ Config file structure

The game uses a JSON configuration file to set the main gameplay parameters. The custom parser supports comments (lines starting with # or //), allowing to annotate settings easily.

The application uses Pydantic to strictly validate the data. If the file is missing, or if a key contains an invalid data type, the game will not crash. Instead, it will automatically clamp the faulty value to a safe default and record a warning in the logs.

The configuration file structure accepts the following keys:

* highscore_filename: The name of the file where top scores are saved (String).

* level: A list of objects defining the width and height of the mazes (List of dictionaries).

* lives: The starting number of lives for the player (Integer).

* pacgum: The target amount of pacgums to distribute in the maze (Integer).

* points_per_pacgum: The score awarded for eating a standard pacgum (Integer).

* points_per_super_pacgum: The score awarded for eating a power pellet (Integer).

* points_per_ghost: The score awarded for eating a scared ghost (Integer).

* seed: The random seed used to generate the very first level (Integer).

* level_max_time: The time limit in seconds to complete a single level (Integer).

### ✳️ Default values
To ensure stability, the configuration model enforces strict boundaries. If a value is omitted or falls outside the allowed limits, the system falls back to the following default values:

* highscore_filename: "highscore.json"

* level: [{"width": 21, "height": 21}] (Dimensions are clamped between 15 and 43).

* lives: 3 (Clamped between 1 and 10).

* pacgum: 42 (Clamped between 10 and 10000. It is also dynamically limited to 80% of the available maze cells).

* points_per_pacgum: 10

* points_per_super_pacgum: 50

* points_per_ghost: 200

* seed: 42

* level_max_time: 90 (Clamped between 30 and 300 seconds).

## 🔵 Visual Representation Features
**TODO  graphical library**:

## 🔵 Resources
**TODO  graphical library**:

## 🔵 Highscore

The game features a persistent highscore system designed with strict data validation and fault tolerance to ensure the leaderboard's integrity.

### ✳️ Storage and Persistence
Highscores are stored locally in a JSON file (the filename is defined dynamically via the main configuration file, defaulting to `highscore.json`).
- **Loading:** The leaderboard is read from the file and displayed directly on the Main Menu.
- **Saving:** When the game ends—whether the player wins or loses all their lives—they are prompted to enter their name on the GameOver screen. The new score is then merged, sorted, and immediately saved back to the file.

### ✳️ Game Rules & Data Validation
The highscore manager strictly enforces the project guidelines:
- **Top 10 Retention:** The system automatically sorts all entries in descending order and truncates the data to retain only the top 10 highest scores.
- **Name Constraints:** Player names are sanitized to accept a maximum of **10 characters**, restricted exclusively to **alphanumeric characters and spaces**.
- **Score Constraints:** Scores are validated as strictly non-negative integers.

### ✳️ Robustness and Error Handling
The parser is built to survive file manipulation and edge cases without crashing the game:
- **Missing File:** If the highscore file is deleted or missing, the game silently initializes a fresh, empty leaderboard.
- **Corrupted Data:** If the file contains malformed JSON or invalid data structures (e.g., manually editing a score to a string, or inserting random keys), the parser intercepts the errors. It logs a warning in the terminal for the developer, safely discards the corrupted entries while keeping the valid ones, and prevents any engine crashes without disrupting the player's experience.

## 🔵 Maze Generation

The game uses the `A-Maze-ing` package to create playable levels automatically.

### ✳️ Level Seeds and Fairness
To keep the highscores fair, the level creation follows strict rules:
- **Level 1:** The first level always uses the `seed` number from the configuration file. This ensures every player starts in the exact same maze.
- **Next Levels:** When the player beats a level, the game generates a random seed (between 1 and 9999999) to build a completely new and unique maze.

### ✳️ Maze Shape and Drawing Walls
The game translates the numbers from the maze generator into the walls on screen:
- **No Dead-Ends:** The maze is generated with the setting `perfect=False`. This removes all dead-ends. It creates a looping maze where Pac-Man can never be completely trapped.
- **Drawing the Walls:** The game reads the maze grid and uses simple math (checking `NORTH`, `EAST`, `SOUTH`, `WEST`) to know exactly where to draw the lines for the walls.
- **The "42" Center:** The code creates a solid block in the shape of the number "42" in the middle of the grid (using the cell value 15).

### ✳️ Placing Characters and Items Safely
The game is programmed to safely place items and characters without crashing:
- **Safe Spawns:** The game searches for a valid, empty space to place the player. The four ghosts are simply placed in the four corners of the map.
- **Smart Pacgum Placement:** When placing the small dots (pacgums), the game ignores the player's starting spot, the four corners (where Super Pacgums go), and the solid walls.
- **Overload Protection:** If the settings file asks for too many pacgums, the game forces a limit. It will only fill a maximum of 80% of the empty spaces. This prevents the game from freezing or crashing.

## 🔵 Implementation

The game is built using Python. It uses Object-Oriented Programming (OOP) to keep the code organized and easy to read.

### ✳️ Game Engine and Loop
- **#TODO - Graphical Engine:**

- **Time-Based Movement:** The game updates positions using `delta_time` (the exact time between frames). This ensures the player and ghosts move at the same speed on any computer, whether it is fast or slow.
- **Grid System:** The maze is a grid. Characters move exactly from one cell's center to another, making collisions very precise.

### ✳️ Data Management and Safety
- **Strict Configuration:** The game uses the `pydantic` library to load the settings file (`config.json`). This ensures all settings are valid (for example, checking that a level's maximum time is a number, not a word).
- **Crash Prevention:** If the configuration file or the highscore file is missing, broken, or hacked, the game does not crash. It silently ignores the bad data and loads safe default values.

### ✳️ Entity Logic and AI
- **Object-Oriented Design:** The player and the ghosts are separate objects. They have their own classes (`Player` and `Ghost`) that manage their specific speed, score, and position.
- **Ghost State Machine:** The ghosts use a "State Machine" to know how to behave. They smoothly switch between three states: `CHASING` (hunting the player), `RUNNING_AWAY` (moving away when a Super Pacgum is eaten), and `DEAD` (returning to their spawn point).
- **Historical AI Behaviors:** The targeting algorithms were built to closely approximate the historical rules of the original arcade game. Each ghost has its own specific strategy:
- **Shadow (Blinky / Red):** Directly targets the player's exact current cell.
- **Speedy (Pinky / Pink):** Tries to cut off the player by targeting the cell exactly **4 spaces ahead** of the player's current direction.
- **Bashful (Inky / Cyan):** Uses a flanking strategy by targeting the cell exactly **4 spaces behind** the player.
- **Pokey (Clyde / Orange):** Chases the player directly until it gets too close (within an **8-space radius**), then abandons the chase and retreats to its assigned corner.

## 🔵 General Software Architecture

The project is structured around a modular, Object-Oriented architecture. The codebase is divided into independent modules handling specific responsibilities, ensuring easy maintenance and scalability.

### ✳️ Core Modules and Relationships

*   **Configuration & Parsing (`src.parsing`):** The entry point of the data flow. The `Loader` class uses `pydantic` schemas to parse, validate, and sanitize the `config.json` file. It outputs a strictly typed `Config` object that dictates the game's rules (lives, points, timers).
*   **Level Generation (`mazegenerator`):** A standalone module provided as part of the project assignment. It is utilized without any internal modifications to procedurally generate a mathematically sound maze matrix (bitmasks) based on a configuration seed.
*   **Game Entities (`src.obj`):** Contains the core blueprints for the game objects. The `Level` class translates the raw maze matrix into navigable space. The `Player` and base `Ghost` classes manage their own coordinates, movement logic, and collision boundaries independently from the visual rendering.
*   **Artificial Intelligence (`src.ai`):** Decoupled from the base entity logic. It includes the `GhostState` machine (handling transitions between CHASING, RUNNING_AWAY, and DEAD) and specific behavior classes (`SpeedyGhost`, `ShadowGhost`, `BashfulGhost`, `PokeyGhost`) that inherit from the base `Ghost` to apply their unique targeting algorithms.
*   **Data Persistence (`src.utils`):** The `HighScoreManager` operates autonomously to read, sanitize, sort, and save player scores to a local JSON file, ensuring data integrity against corrupted or malicious inputs.
*   **Graphical Interface & Engine:**

`#TODO`

### ✳️ High-Level Data Flow

1. The game launches and the **Loader** secures the configuration.
2. The central **Game Engine** uses this configuration to initialize the **MazeGenerator** and build the **Level**.
3. The **Player** and **Ghosts** are spawned on the grid.
4. During the game loop, the engine delegates movement to the entities, while the **AI module** dictates the ghosts' specific pathfinding.
5. Upon game completion, the **HighScoreManager** is invoked to securely process and store the final score.

## 🔵 Project Management

This project was managed using a modular approach, focusing on writing independent components that are easy to test and maintain.

### ✳️ Methodology
- **Test-Driven Development (TDD):** We prioritized reliability by writing automated tests for the score management and configuration loading systems.
- **Continuous Improvement:** The architecture was designed to be decoupled, allowing for easy updates or replacements.

### ✳️ Project Tracking
All development progress, task tracking, and planning logs are organized in our dedicated project management directory. You can access individual documents below:

<details>
<summary>📂 Open Project Management Directory</summary>

- [Kanban Board](project_management/kanban.md)
- [Logbook & Progress](project_management/logbook.md)
- [Risk Analysis](project_management/risk_analysis.md)
- [Test Plan](project_management/test_plan.md)
- [Timeline](project_management/timeline.md)

</details>

## 🔵 Resources

### ✳️ References
To build this project, we relied on historical arcade design patterns and modern software development practices. The following resources were instrumental:

*   **Pac-Man Dossier (Jamey Pittman):** The definitive technical analysis of the original arcade game’s logic, ghost AI targeting, and maze topology. [https://www.gamedeveloper.com/design/the-pac-man-dossier]
*   **Python Documentation (Official):** Primary reference for standard libraries and type hinting. Special emphasis was placed on the **`logging` module**.

*   **# TODO** Graphical Library Documentation

### ✳️ AI Usage
Artificial Intelligence was used as a strategic support tool throughout the development lifecycle to enhance documentation and ensure code quality:

*   **Documentation:** AI was used to translate this README into English, ensuring professional syntax and clarity.
*   **Quality Assurance:** AI acted as a "pair programmer" during the design of the testing strategy, specifically helping to identify edge cases for `HighScoreManager` and the `Loader` configuration.
*   **Refactoring:** AI provided guidance on refactoring classes according to clean code principles.
*   **Code Review:** AI was consulted to verify the implementation of Pydantic validation schemas.
