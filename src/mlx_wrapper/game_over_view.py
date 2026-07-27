import pygame
from src.mlx_wrapper.base_view import BaseView
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.game_manager import GameManager
from src.utils.highscore import HighScoreManager
from src.parsing.models import Config


class GameOverView(BaseView):
    """
    View displayed when the game is over.

    Allows entering a name for highscores.
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
        Render the UI elements (titles and inputs).
        """
        self.engine.clear_screen((50, 50, 50))

        screen_width = self.manager.width
        screen_height = self.manager.height

        center_x = screen_width // 2

        title_y = int(screen_height * 0.25)
        if self.victory:
            self.engine.put_title_string(center_x - 140, title_y,
                                         "YOU WIN!", (0, 255, 0))
        else:
            self.engine.put_title_string(center_x - 180, title_y,
                                         "GAME OVER", (255, 0, 0))

        score_y = title_y + 110
        self.engine.put_string(center_x - 100, score_y,
                               f"Final Score: {self.final_score}",
                               (255, 255, 255))

        input_label_y = score_y + 70
        self.engine.put_string(center_x - 220, input_label_y,
                               "Enter Name (Press ENTER to save):",
                               (255, 255, 255))

        input_y = input_label_y + 50
        self.engine.put_string(center_x - 60, input_y,
                               self.player_name + "_", (255, 255, 0))

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
