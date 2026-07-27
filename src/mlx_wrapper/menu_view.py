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

        screen_width = self.manager.width
        screen_height = self.manager.height

        center_x = screen_width // 2

        title_x = center_x - 120
        title_y = int(screen_height * 0.15)
        self.engine.put_title_string(title_x, title_y,
                                     "PAC-MAN",
                                     (255, 255, 0))

        start_menu_y = int(screen_height * 0.25)
        for i, option in enumerate(self.options):
            color = (255, 0, 0) if i == self.selected_index \
                else (255, 255, 255)
            prefix = "> " if i == self.selected_index else "  "
            text = f"{prefix}{option}"

            option_x = center_x - 80
            option_y = start_menu_y + (i * 60)
            self.engine.put_string(option_x, option_y, text, color)

        score_title_y = start_menu_y + 250
        self.engine.put_title_string(center_x - 220, score_title_y,
                                     "TOP 10 SCORES", (255, 255, 0))

        top_scores = self.score_manager.scores[:10]

        if not top_scores:
            self.engine.put_string(center_x - 60, score_title_y + 150,
                                   "No scores yet",
                                   (200, 200, 200))
        else:
            for rank, entry in enumerate(top_scores, start=1):
                row_text = f"{rank:>2}. {entry['name']:<10} {entry['score']}"
                row_y = score_title_y + 150 + (rank * 25)
                self.engine.put_string(center_x - 90, row_y, row_text,
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
