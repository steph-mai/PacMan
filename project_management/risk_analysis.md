# Risk Analysis and Mitigation Plan

## Introduction
This document identifies the technical, organizational, and architectural risks anticipated or encountered during the development of the Pac-Man project. For each risk, a criticality assessment (Probability × Impact) is defined, along with the mitigation strategies implemented to resolve or minimize it.

## Risk Matrix

| ID | Risk Name | Probability | Impact | Criticality |
|---|---|---|---|---|
| **R1** | Non-compliance with graphics library constraints (MLX Rule) | Medium | Critical | **High** |
| **R2** | Monolithic architecture ("God Object") and technical debt | High | Major | **High** |
| **R3** | CPU overload (Performance issues due to infinite loop) | High | Major | **High** |
| **R4** | Procedural maze generation failure | Low | Major | **Medium** |

---

## Risk Details and Mitigation Strategies

### R1: Non-compliance with graphics library constraints (MLX Rule)
*   **Description:** The project guidelines require an architecture strictly similar to MiniLibX (MLX). Using high-level Pygame functions (e.g., `pygame.draw.circle`, `pygame.time.Clock`, or event polling lists) would result in a direct evaluation failure.
*   **Mitigation:**
    1.  Created a strict wrapper (`MLXEngine`) that completely encapsulates and hides Pygame.
    2. Transitioned from a continuous event-checking loop (Polling) to a "Callbacks/Hooks" architecture (mlx_key_hook, mlx_loop_hook). Instead of constantly asking the system for inputs, functions are only executed when an event actually occurs, strictly mimicking how the MLX library operates.
    3.  Removed programmatic geometric drawing in favor of exclusive sprite rendering (simulating `mlx_put_image_to_window` via custom `draw_image`).

### R2: Monolithic architecture ("God Object") **# TODO**
*   **Description:** The main class (`GameView`) centralized business logic, level generation, collision handling, and rendering. This made the codebase increasingly difficult to maintain and debug.
*   **Mitigation:**
    1.  Applied the Single Responsibility Principle (SRP).
    2.  Scheduled refactoring to extract rendering logic into a dedicated class (`GameRenderer`) and isolate game data into a state object (`GameState`).

### R3: CPU overload and framerate issues
*   **Description:** Unlike the Arcade library, using a pure `while True` loop to simulate the `mlx_loop` behavior maxes out the CPU at 100%, causing hardware overheating and unpredictable game speeds.
*   **Mitigation:**
    1.  Implemented a manual FPS limiter based on Delta Time calculations using the native `time.time()` module.
    2.  Utilized `time.sleep()` to pause the process briefly when the frame calculation finishes ahead of the target frame rate.

### R4: Procedural maze generation failure
*   **Description:** The external `MazeGenerator` algorithm can crash due to an invalid seed or generate an unresolvable level, potentially blocking the game launch.
*   **Mitigation:**
    1.  Isolated the procedural generation process within a `try/except` block.
    2.  Implemented a fallback system that automatically loads hardcoded default levels if the generator fails, ensuring continuous playability.
