import arcade
import arcade.gui
from ..utils.highscore import HighScoreManager


class GameOverView(arcade.View):
    """
    View displayed when the player loses all lives. Allows
    entering a name for highscores.
    """

    def __init__(self, final_score: int) -> None:
        """
        Initialize the game over screen with the player's final score.

        Args:
            final_score (int): The score achieved during the game.
        """
        super().__init__()
        self.final_score: int = final_score
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.BLACK)

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        game_over_label = arcade.gui.UILabel(
            text="GAME OVER",
            text_color=arcade.color.RED,
            font_size=40,
            bold=True
        )
        self.v_box.add(game_over_label)

        score_label = arcade.gui.UILabel(
            text=f"Final Score: {self.final_score}",
            text_color=arcade.color.WHITE,
            font_size=20
        )
        self.v_box.add(score_label)

        self.name_input = arcade.gui.UIInputText(
            color=arcade.color.BLACK,
            font_size=20,
            width=200,
            text="Enter Name"
        )
        self.name_input = arcade.gui.UIInputText(
            text_color=arcade.color.BLACK,
            font_size=20,
            width=200,
            text="Enter Name"
        )

        input_bg = self.name_input.with_background(color=arcade.color.WHITE)

        self.v_box.add(input_bg)

        save_btn = arcade.gui.UIFlatButton(text="Save & Return to Menu",
                                           width=250)
        self.v_box.add(save_btn)

        @save_btn.event("on_click")
        def on_click_save(event: arcade.gui.UIOnClickEvent) -> None:
            self.save_highscore_and_exit()

        self.manager.add(
            arcade.gui.UIAnchorLayout(
                child=self.v_box,
                anchor_x="center_x",
                anchor_y="center_y"
            )
        )

    def save_highscore_and_exit(self) -> None:
        """
        Process the inputted name, save the score,
        and switch back to the main menu.
        """
        player_name = self.name_input.text

        score_manager = HighScoreManager()
        score_manager.add_score(player_name, self.final_score)

        print(f"Score saved for {player_name}: {self.final_score}")

        self.manager.disable()

        from .menu import MenuView
        menu_view = MenuView()
        self.window.show_view(menu_view)

    def on_draw(self) -> None:
        """
        Render the UI elements.
        """
        self.clear()
        self.manager.draw()
