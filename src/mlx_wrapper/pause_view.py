import logging

import pygame
from src.mlx_wrapper.base_view import BaseView
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.game_manager import GameManager


logger = logging.getLogger("pacman")


class PauseView(BaseView):
    """
    View displayed when the game is paused.
    """

    def __init__(self, engine: MLXEngine, manager: GameManager,
                 previous_view: BaseView, config) -> None:
        """Initialize the pause menu with reference to the active game view."""
        super().__init__(engine)
        self.manager = manager
        self.previous_view = previous_view
        self.config = config
        self.options = ["Resume", "Return to Main Menu"]
        self.selected_index = 0

    def on_update(self, delta_time: float) -> None:
        """Do nothing during pause update."""
        pass

    def on_draw(self) -> None:
        """Render the pause overlay."""
        try:
            self.engine.clear_screen()
            center_x = self.manager.width // 2
            center_y = self.manager.height // 2

            self.engine.put_title_string(center_x - 140, center_y - 120,
                                         "PAUSED", (255, 255, 0))

            for i, option in enumerate(self.options):
                color = (255, 0, 0) if i == self.selected_index else (255,
                                                                      255,
                                                                      255)
                prefix = "> " if i == self.selected_index else "  "
                self.engine.put_string(center_x - 100, center_y + (i * 50),
                                       f"{prefix}{option}", color)
        except (AttributeError, TypeError, pygame.error):
            logger.exception("Failed to render pause view.")

    def _return_to_previous_view(self) -> None:
        """Safely restore the previous view."""
        try:
            self.manager.set_view(self.previous_view)
        except (AttributeError, TypeError):
            logger.exception("Failed to restore the previous view.")

    def on_key_press(self, keycode: int) -> None:
        """Handle menu navigation during pause."""
        try:
            if keycode in (pygame.K_UP, pygame.K_w):
                self.selected_index = ((self.selected_index - 1)
                                       % len(self.options))
            elif keycode in (pygame.K_DOWN, pygame.K_s):
                self.selected_index = ((self.selected_index + 1)
                                       % len(self.options))
            elif keycode == pygame.K_RETURN:
                if self.selected_index == 0:
                    self._return_to_previous_view()
                elif self.selected_index == 1:
                    from src.mlx_wrapper.menu_view import MenuView
                    self.manager.set_view(MenuView(self.engine, self.manager,
                                                   self.config))
            elif keycode in (pygame.K_ESCAPE, pygame.K_p):
                self._return_to_previous_view()
        except ImportError:
            logger.exception("Failed to import the main menu view.")
            self._return_to_previous_view()
        except (AttributeError, TypeError, pygame.error):
            logger.exception("Unexpected error while handling pause input.")
            self._return_to_previous_view()
