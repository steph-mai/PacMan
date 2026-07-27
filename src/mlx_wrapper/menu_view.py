import pygame
import sys
from src.mlx_wrapper.base_view import BaseView
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.game_manager import GameManager
from src.parsing.models import Config


class MenuView(BaseView):
    """
    Main menu view for map selection.

    Allows the player to start the game or quit using keyboard navigation.
    """

    def __init__(self,
                 engine: MLXEngine,
                 manager: GameManager,
                 config: Config) -> None:
        """
        Initialize the main menu view.

        Args:
            engine (MLXEngine): The MLX wrapper engine for rendering.
            manager (GameManager): The manager controlling view transitions.
            config (Config): The parsed configuration data.
        """
        super().__init__(engine)
        self.manager: GameManager = manager
        self.config: Config = config

        self.options: list[str] = ["Launch Game", "Quit"]
        self.selected_index: int = 0

    def on_update(self, delta_time: float) -> None:
        """
        Update the view state.

        Args:
            delta_time (float): Time elapsed since the last update in seconds.
        """
        pass

    def on_draw(self) -> None:
        """
        Render the menu view elements using the MLX engine text renderer.
        """
        self.engine.clear_screen((50, 50, 50))

        self.engine.put_string(550, 200, "PAC-MAN", (255, 255, 0))

        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_index \
                else (255, 255, 255)
            prefix = "> " if i == self.selected_index else "  "

            self.engine.put_string(550, 350 + (i * 50),
                                   f"{prefix}{option}",
                                   color)

    def on_key_press(self, keycode: int) -> None:
        """
        Handle keyboard inputs for menu navigation.

        Args:
            keycode (int): The integer code of the pressed key.
        """
        if keycode == pygame.K_UP:
            self.selected_index = (self.selected_index - 1) % len(self.options)
        elif keycode == pygame.K_DOWN:
            self.selected_index = (self.selected_index + 1) % len(self.options)
        elif keycode == pygame.K_RETURN:
            if self.selected_index == 0:
                from src.mlx_wrapper.game_view import GameView
                game_view = GameView(self.engine, self.config, self.manager)
                self.manager.set_view(game_view)
            elif self.selected_index == 1:
                pygame.quit()
                sys.exit(0)
