# Project Logbook

## Day 1

### qdecross

- Created a menu and a basic maze visualization.
- Created a `Level` class that stores the maze and calculates the nearest valid player spawn point close to the center.
- Created a `Player` class containing stats and basic player logic: lives, score, etc.
- Implemented player movement logic with the keys `W`, `A`, `S`, `D`.
- Implemented gum-related logic: distribution, pickup, score increase.
- Implemented life loss logic triggered by ghost contact.
- Current maze rendering is made using drawn lines, with future evolution planned toward a tile-based system.
- Distributed a number of gums equal to the value in the config, or 80% of available maze cells if the config value is too high, randomly across maze corridors.

### stmaire

- Created the configuration loading logic (`Loader`): comments (`#`, `//`) are ignored during JSON parsing and `OSError` exceptions are caught to prevent tracebacks.
- Created a `Config` class with Pydantic for business validation of data.
- Implemented clamping logic to silently bound and correct abnormal values (e.g. negative lives, inconsistent level times). In progress.
- Added an internal logging system that records configuration warnings to `pacman.log` and to the terminal, preserving a history of corrections applied by the program.

## Day 2

### stmaire


- Finished `loader.py`: connected the config file so its values are injected directly into `GameView`.
- Added a `Config` attribute to `MenuView`, `GameView`, and `Player`.
- Fixed `models.py` to define global variables and avoid magic numbers in the Pydantic class, and corrected fallback values in `models.py`.
- Initialized the player start position in `GameView.__init__` using `Level.find_valid_spawn_position`.
- Injected the logger into `main` in append mode so all logs accumulate in `pacman.log`. Need to assess whether to set a maximum log file size.

## Day 3

### qdecross

- Level victory condition: added a check in the game loop to detect when all pacgums have been eaten, triggering level completion.
- Player persistence: updated `GameView` and the `Player` class so the player object (and therefore their score and lives) is preserved when moving from one maze to another.
- Death refactor: clearly separated life loss (`lose_life`) from respawn at the center (`reset_position`) to make future ghost integration easier.
- Cheat mode basics: added attributes and methods in `Player` to manage invincibility and extra lives.

- Continuous movement and input buffering: completely redesigned the movement system. The player now moves continuously on their own through a timer, and key presses are buffered so they turn automatically and smoothly at the next intersection, like in real Pac-Man.

### stmaire

- Project management: created `kanban.md` with screenshots of Trello, to be completed throughout the project.
- Created `timeline.md` with Trello screenshots.
- Created `logbook.md` to record daily progress (moved to the correct folder after the push).
- Completed the integration of the `mazegen` package. `Perfect = False`.
- Seed management: the config file provides the seed for the first level, and a random seed is used afterward.
- Created the `Ghost` and `GhostState` classes: an enum listing the possible ghost states (`CHASING`, `RUNNING_AWAY`, `DEAD`). Added methods to update movement every frame and to update the object when a ghost dies.
- Arcade link: the `Ghost` class includes a `draw` method, and `GameView` sets up the ghosts. For now, the ghosts appear as colored circles (pink, red, purple, blue) in the four corners of the maze.

## Day 4

### qdecross

- `HighScoreManager`: created an independent class responsible for reading, sorting (while keeping the top 10), and writing scores to a local `highscores.json` file.
- Data security: the system handles corrupted files without crashing the game, and the player nickname is automatically filtered and limited to 10 alphanumeric characters.
- `GameOverView`: added a new interactive screen shown at the end of the game. It displays the final score and includes a text field for entering the player name.
- The transition from the game view to the game-over view, and then back to the main menu after saving, is almost working.

### stmaire

- Created an `ia` folder to group ghost intelligence.
- In this folder, `states.py` contains the `GhostState` enum with the different ghost states.
- The `personalities` file contains the `GhostPersonality` enum with individualized ghost personalities. Each personality will have its own movement algorithm, inspired as closely as possible by the original Pac-Man game.
- In the `obj` folder, the `Ghost` class and its `choose_direction` method will be used to update ghost positions.
- Updated `GameView` so ghost setup takes personality into account.

## Day 5

### qdecross

- First attempt at collision logic. Not functional yet.

### stmaire

- Restructured the `Ghost` and `Player` classes so they now inherit from the abstract `Entity` class.
- Connected `GameView`, the ghost classes, and `GhostPersonality` for testing. Ghosts currently move randomly in test mode.

## Day 6

### qdecross

- Finished the high score implementation. For now, it works like an arcade machine: all scores are stored in the JSON file, and the top 10 are displayed on the game-over screen.
- Implemented cheat mode.
- Press `C` to activate it, then:
  - `F1`: invincibility — `Player.toggle_invincibility()`
  - `F2`: skip level — directly calls `handle_level_complete()`, which already manages moving to the next level or reaching the final victory state
  - `F3`: freeze ghosts — new `self.ghosts_frozen` flag; `on_update` skips the `ghost.update_movement()` loop when active
  - `F4`: extra life — `Player.add_extra_life()`
  - `F5`: increased speed — new `Player.toggle_speed_boost()`; it divides `move_delay` by `SPEED_BOOST_MULTIPLIER` when active

### stmaire

- Ghost AI: Blinky's algorithm targets the player directly. It calculates the straight-line distance ("as the crow flies") to the player to determine the next direction (calculating the actual shortest path by accounting for maze walls would make the game too difficult).

- Cheat mode hotfix: Pressing 'C' again disables invincibility and other gameplay assists.

## Day 7

### stmaire
- Parsing: handled errors in the "level" field of the configuration file. If the value is an empty list, `null`, or a list containing items that are not dictionaries, a warning log message is recorded.
- Added log messages for missing fields and invalid field types in the configuration file.
- Added a log message when the number of pacgums exceeds 80% of the maze cells.
- Generated a test file with AI assistance to verify edge cases.

## Day 8

### stmaire

- Refactored ghost personalities by creating one class per ghost type: `SpeedyGhost`, `BashfulGhost`, `PokeyGhost`, `RandomGhost`, and `ShadowGhost`, all inheriting from `Ghost`.
- Implemented polymorphism with `_get_next_direction` in each child class.
- Important note: the new project brief is not arcade-based. Only equivalent functions from the MLX are allowed.

## Day 9

### stmaire

- Completed the implementation of ghost behavior:
  - Blinky targets the player directly.
  - Pinky targets four cells ahead of the player.
  - Inky targets four cells behind the player.
  - Clyde does not move closer than five cells to the player; when it gets too close, it turns around.
- Implemented edible mode for ghosts:
  - When Pacman collects a super pacgum, ghosts enter flee mode and can be eaten for 10 seconds.
  - They blink during the last 3 seconds before returning to `CHASING` mode.
- Updated the project management folder.


