import pygame
import sys
from src.mlx_wrapper.base_view import BaseView
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.game_manager import GameManager
from src.parsing.models import Config
from src.utils.highscore import HighScoreManager


class MenuView(BaseView):
    """
    Main menu view for map selection.

    Allows the player to start the game or quit using keyboard navigation,
    and displays the top 10 highscores.
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

        self.score_manager = HighScoreManager()

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

        self.engine.put_title_string(480, 200, "PAC-MAN", (255, 255, 0))

        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_index \
                else (255, 255, 255)
            prefix = "> " if i == self.selected_index else "  "

            self.engine.put_string(530, 350 + (i * 50),
                                   f"{prefix}{option}",
                                   color)

        self.engine.put_string(900, 150, "TOP 10 SCORES", (255, 255, 0))

        top_scores = self.score_manager.scores[:10]

        if not top_scores:
            self.engine.put_small_string(900, 220, "No scores yet",
                                         (200, 200, 200))
        else:
            for rank, entry in enumerate(top_scores, start=1):
                row_text = f"{rank:>2}. {entry['name']:<10} {entry['score']}"
                self.engine.put_small_string(900, 200 + (rank * 30), row_text,
                                             (255, 255, 255))

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
                from src.mlx_wrapper.playing.game_view import GameView
                game_view = GameView(self.engine, self.config, self.manager)
                self.manager.set_view(game_view)
            elif self.selected_index == 1:
                pygame.quit()
                sys.exit(0)
