import logging

import pygame
from src.mlx_wrapper.base_view import BaseView
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.game_manager import GameManager
from src.parsing.models import Config


logger = logging.getLogger("pacman")


class InstructionsView(BaseView):
    """
    View displaying the game rules, controls, and cheat codes.

    Allows the player to read the instructions and return to the main menu
    by pressing ENTER or ESCAPE.
    """

    def __init__(self, engine: MLXEngine, manager: GameManager, config: Config
                 ) -> None:
        """
        Initialize the instructions view.

        Args:
            engine (MLXEngine): The MLX wrapper engine for rendering.
            manager (GameManager): The manager controlling view transitions.
            config (Config): The parsed configuration data.
        """
        super().__init__(engine)
        self.manager = manager
        self.config = config

    def on_update(self, delta_time: float) -> None:
        """
        Update the view state.

        Args:
            delta_time (float): Time elapsed since the last update in seconds.
        """
        pass

    def on_draw(self) -> None:
        """
        Render the instructions text on the screen.
        """
        self.engine.clear_screen()
        center_x = self.manager.width // 2

        self.engine.put_title_string(center_x - 250, 50, "INSTRUCTIONS",
                                     (255, 255, 0))

        self.engine.put_string(center_x - 250, 200, "RULES:", (255, 100, 100))
        self.engine.put_small_string(center_x - 200, 240,
                                     "- Eat all pacgums to win the level.",
                                     (255, 255, 255))
        self.engine.put_small_string(center_x - 200, 270,
                                     "- Avoid ghosts or you will lose a life.",
                                     (255, 255, 255))
        self.engine.put_small_string(center_x - 200, 300,
                                     "- Super-pacgums make ghosts edible.",
                                     (255, 255, 255))

        self.engine.put_string(center_x - 250, 370, "CONTROLS:",
                               (100, 255, 100))
        self.engine.put_small_string(center_x - 200, 410,
                                     "- Arrows / WASD : Move Pac-Man",
                                     (255, 255, 255))
        self.engine.put_small_string(center_x - 200, 440,
                                     "- P / ESC : Pause game",
                                     (255, 255, 255))

        self.engine.put_string(center_x - 250, 510,
                               "CHEAT MODE:", (100, 150, 255))
        self.engine.put_small_string(center_x - 200, 550,
                                     "- Press 'C' in-game "
                                     "to toggle Cheat Mode",
                                     (255, 255, 255))
        self.engine.put_small_string(center_x - 200, 580,
                                     "- F1: Invincible | F2: Skip Level "
                                     "| F3: Freeze Ghosts",
                                     (255, 255, 255))
        self.engine.put_small_string(center_x - 200, 610,
                                     "- F4: Extra Life | F5: Speed Boost",
                                     (255, 255, 255))

        self.engine.put_string(center_x - 150, self.manager.height - 150,
                               "Press ENTER to return", (255, 255, 0))

    def on_key_press(self, keycode: int) -> None:
        """
        Handle key presses to return to the main menu.

        Args:
            keycode (int): The integer code of the pressed key.
        """
        if keycode in (pygame.K_RETURN, pygame.K_ESCAPE):
            try:
                from src.mlx_wrapper.menu_view import MenuView
                menu_view = MenuView(self.engine, self.manager, self.config)
                self.manager.set_view(menu_view)
            except ImportError:
                logger.error("Failed to import MenuView.")
            except (AttributeError, TypeError):
                logger.error("Failed to create or set MenuView.")
