# Acceptance Test Plan

To ensure code reliability and prevent regressions during refactoring, we implemented an automated testing strategy using `pytest`.

## 1. Maze Generation (`tests/test_mazegen.py`)
*   **Features Tested:** Matrix sizing and dimensions, existence of entry/exit points, pathfinding validity (shortest path), and grid data type verification.
*   **Acceptance Criteria:** The generated maze must strictly match the requested grid dimensions, contain valid integer data for its cells, and guarantee a navigable path between defined entry and exit points.

## 2. Configuration Loader (`tests/test_loader.py`)
*   **Features Tested:** JSON parsing, validation of expected keys, handling of missing files, and injection of default fallback values.
*   **Acceptance Criteria:** The game must never crash due to a malformed or missing config file; it must log an error and use safe default parameters.

## 3. Highscore System (`tests/test-highscores.py`)
*   **Features Tested:** Adding new scores, sorting scores in descending order, limiting the saved list to the Top 10.
*   **Acceptance Criteria:** The system must accurately persist data and drop the 11th score to maintain the Top 10 constraint.

