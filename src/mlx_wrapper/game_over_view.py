import pygame
from src.mlx_wrapper.base_view import BaseView
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.game_manager import GameManager
from src.utils.highscore import HighScoreManager
from src.parsing.models import Config


class GameOverView(BaseView):
    """
    View displayed when the game is over.

    Allows entering a name for highscores and displays the leaderboard.
    """

    def __init__(self,
                 engine: MLXEngine,
                 manager: GameManager,
                 final_score: int,
                 config: Config,
                 victory: bool = False
                 ) -> None:
        """
        Initialize the game over screen.

        Args:
            engine (MLXEngine): The MLX wrapper engine for rendering.
            manager (GameManager): The manager controlling view transitions.
            final_score (int): The player's final score.
            config (Config): The parsed configuration data.
            victory (bool): True if the player won, False otherwise.
        """
        super().__init__(engine)
        self.manager: GameManager = manager
        self.final_score: int = final_score
        self.config: Config = config
        self.victory: bool = victory

        self.score_manager = HighScoreManager()
        self.player_name: str = ""

    def on_update(self, delta_time: float) -> None:
        """
        Update the view state.

        Args:
            delta_time (float): Time elapsed since the last update in seconds.
        """
        pass

    def on_draw(self) -> None:
        """
        Render the UI elements (titles, inputs, and highscores).
        """
        self.engine.clear_screen((50, 50, 50))

        if self.victory:
            self.engine.put_string(200, 150, "YOU WIN!", (0, 255, 0))
        else:
            self.engine.put_string(200, 150, "GAME OVER", (255, 0, 0))

        self.engine.put_string(200, 220, f"Final Score: {self.final_score}",
                               (255, 255, 255))

        self.engine.put_string(200, 350, "Enter Name (Press ENTER to save):",
                               (255, 255, 255))
        self.engine.put_string(200, 400, self.player_name + "_", (255, 255, 0))

        self.engine.put_string(700, 150, "TOP 10 SCORES", (255, 255, 0))

        top_scores = self.score_manager.scores[:10]

        if not top_scores:
            self.engine.put_string(700, 220, "No scores yet", (200, 200, 200))
        else:
            for rank, entry in enumerate(top_scores, start=1):
                row_text = f"{rank:>2}. {entry['name']:<10} {entry['score']}"
                self.engine.put_string(700, 200 + (rank * 30), row_text,
                                       (255, 255, 255))

    def on_key_press(self, keycode: int) -> None:
        """
        Handle typing inputs and validation.

        Args:
            keycode (int): The integer code of the pressed key.
        """
        if keycode == pygame.K_RETURN:
            self.save_highscore_and_exit()
        elif keycode == pygame.K_BACKSPACE:
            self.player_name = self.player_name[:-1]
        elif keycode == pygame.K_SPACE and len(self.player_name) < 10:
            self.player_name += " "
        else:
            if len(self.player_name) < 10:
                if pygame.K_a <= keycode <= pygame.K_z:
                    self.player_name += chr(keycode).upper()
                elif pygame.K_0 <= keycode <= pygame.K_9:
                    self.player_name += chr(keycode)

    def save_highscore_and_exit(self) -> None:
        """
        Process the inputted name, save the score, and switch back
        to the main menu.
        """
        name_to_save = self.player_name if self.player_name.strip()\
            else "Anonymous"

        self.score_manager.add_score(name_to_save, self.final_score)
        print(f"Score saved for {name_to_save}: {self.final_score}")

        from src.mlx_wrapper.menu_view import MenuView
        menu_view = MenuView(self.engine, self.manager, self.config)
        self.manager.set_view(menu_view)
