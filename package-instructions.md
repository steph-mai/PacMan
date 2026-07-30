# 🕹️ Pac-Man - Installation & Gameplay Instructions

Welcome to this modern recreation of the classic 1980 arcade game, developed as part of the 42 curriculum! 

This game has been packaged as a standalone application **for Linux**. You do not need to install Python, Pygame, or any other dependencies to play. Everything is bundled inside the provided folder.

## 📥 Download & Installation

1. Download the provided archive `.zip` from the download section below.
2. Extract the archive to a location of your choice.
3. Open your terminal and navigate inside the extracted folder:
    
    ```bash
    cd <path/to/extracted/pac-man-folder>
    ```

4. Grant execution permissions to the main file (if not already set) by running:
    
    ```bash
    chmod +x pac-man
    ```

5. Launch the game directly from the terminal:
    
    ```bash
    ./pac-man
    ```

---

## ⚠️ Important Note

**Keep the files together:** The game uses the `config.json` file and the `inc/` assets directory provided in the folder `_internal`. Please do not move the `pac-man` executable outside of the root, otherwise, it will not be able to load the levels, textures, and settings.

---

## ⚙️ Configuration (`config.json`)

You can customize the game's behavior by opening and modifying the `config.json` file located in the same folder as the executable. It contains the following parameters:

* **`highscore_filename`**: The file where your top scores will be saved (default is `"highscores.json"`).
* **`lives`**: The starting number of lives for the player (default is `3`).
* **`points_per_pacgum`**: Points awarded for eating a small dot (default is `10`).
* **`points_per_super_pacgum`**: Points awarded for eating a power pellet (default is `50`).
* **`points_per_ghost`**: Points awarded for catching a scared ghost (default is `200`).
* **`level_max_time`**: The time limit in seconds to complete each level (default is `90`).
* **`seed`**: The random seed used to generate the very first level's maze (default is `42`).
* **`pacgum`**: The target amount of pacgums to spawn in the maze (default is `42`).
* **`level`**: A list of levels, each defining the maze dimensions (`width` and `height`). You can add or modify levels here to change the maze sizes as you progress.

---

## 🎮 How to Play

### Goal
Eat all the small pacgums in the maze to complete the level. Avoid the ghosts, or you will lose a life! If you eat a Super-Pacgum (the large pellets in the corners), the ghosts will turn blue and run away—chase them down for extra points!

### Controls
* **Movement:** `Arrow Keys` or `W`, `A`, `S`, `D`
* **Pause Game:** `P` or `ESCAPE`
* **Confirm / Select:** `ENTER`

### 🛠️ Cheat Mode (For Testing & Review)
A built-in cheat mode is available to help evaluate the game mechanics quickly. 
During gameplay, press **`C`** to toggle the Cheat Mode overlay, then use the following Function keys:

* **`F1`**: Toggle Invincibility
* **`F2`**: Instantly Win the Level
* **`F3`**: Freeze all Ghosts
* **`F4`**: Add an Extra Life
* **`F5`**: Toggle Speed Boost

---

*Thank you for playing! If you encounter any unexpected issues, please leave a comment on the itch.io page.*