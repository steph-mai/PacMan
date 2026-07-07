# Project Logbook

## qdecross

### Day 1

- Created a menu and a basic maze visualization.
- Created a `Level` class that stores the maze and calculates the nearest valid player spawn point close to the center.
- Created a `Player` class containing stats and basic player logic: lives, score, etc.
- Implemented player movement logic with the keys `W`, `A`, `S`, `D`.
- Implemented gum-related logic: distribution, pickup, score increase.
- Implemented life loss logic triggered by ghost contact.
- Current maze rendering is made using drawn lines, with future evolution planned toward a tile-based system.
- Distributed a number of gums equal to the value in the config, or 80% of available maze cells if the config value is too high, randomly across maze corridors.

## stmaire

### Day 1

- Created the configuration loading logic (`Loader`): comments (`#`, `//`) are ignored during JSON parsing and `OSError` exceptions are caught to prevent tracebacks.
- Created a `Config` class with Pydantic for business validation of data.
- Implemented clamping logic to silently bound and correct abnormal values (e.g. negative lives, inconsistent level times). In progress.
- Added an internal logging system that records configuration warnings to `pacman.log` and to the terminal, preserving a history of corrections applied by the program.

### Day 2

- Finished `loader.py`: connected the config file so its values are injected directly into `GameView`.
- Added a `Config` attribute to `MenuView`, `GameView`, and `Player`.
- Fixed `models.py` to define global variables and avoid magic numbers in the Pydantic class, and corrected fallback values in `models.py`.
- Initialized the player start position in `GameView.__init__` using `Level.find_valid_spawn_position`.
- Injected the logger into `main` in append mode so all logs accumulate in `pacman.log`. Need to assess whether to set a maximum log file size.
