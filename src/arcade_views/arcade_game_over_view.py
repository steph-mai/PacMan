import arcade
import arcade.gui
from ..utils.highscore import HighScoreManager
from src.parsing.models import Config


class GameOverView(arcade.View):
    """
    View displayed when the player loses all lives. Allows
    entering a name for highscores.
    """

    def __init__(self, final_score: int,
                 config: Config,
                 victory: bool = False) -> None:
        """
        Initialize the game over screen with the player's
        final score and config.
        """
        super().__init__()
        self.final_score: int = final_score
        self.config: Config = config
        self.victory: bool = victory
        self.manager = arcade.gui.UIManager()

        self.v_box = arcade.gui.UIBoxLayout(space_between=20)

        if self.victory:
            title_text = "YOU WIN!"
            title_color = arcade.color.GO_GREEN
        else:
            title_text = "GAME OVER"
            title_color = arcade.color.RED

        game_over_label = arcade.gui.UILabel(
            text=title_text,
            text_color=title_color,
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
            text_color=arcade.color.BLACK,
            font_size=20,
            width=200,
            height=25,
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

        self.score_manager = HighScoreManager()
        scores_box = arcade.gui.UIBoxLayout(space_between=5)

        scores_title = arcade.gui.UILabel(
            text="TOP 10 SCORES",
            text_color=arcade.color.YELLOW,
            font_size=22,
            bold=True
        )
        scores_box.add(scores_title)

        top_scores = self.score_manager.scores[:10]

        if not top_scores:
            empty_label = arcade.gui.UILabel(
                text="No scores yet",
                text_color=arcade.color.LIGHT_GRAY,
                font_size=14
            )
            scores_box.add(empty_label)
        else:
            for rank, entry in enumerate(top_scores, start=1):
                row_text = f"{rank:>2}. {entry['name']:<10} {entry['score']}"
                row_label = arcade.gui.UILabel(
                    text=row_text,
                    text_color=arcade.color.WHITE,
                    font_size=16
                )
                scores_box.add(row_label)

        h_box = arcade.gui.UIBoxLayout(vertical=False, space_between=60)
        h_box.add(self.v_box)
        h_box.add(scores_box)

        anchor = arcade.gui.UIAnchorLayout()
        anchor.add(
            child=h_box,
            anchor_x="center_x",
            anchor_y="center_y"
        )
        self.manager.add(anchor)

    def on_show_view(self) -> None:
        """
        Handle view activation. Set the background color and
        enable UI interactions.
        """
        arcade.set_background_color(arcade.color.GRAY)
        self.on_resize(self.window.width, self.window.height)
        self.manager.enable()

    def on_resize(self, width: int, height: int) -> None:
        super().on_resize(width, height)

    def on_hide_view(self) -> None:
        """
        Disable interactions when the view is hidden to prevent ghost inputs.
        """
        self.manager.disable()

    def save_highscore_and_exit(self) -> None:
        player_name = self.name_input.text
        self.score_manager.add_score(player_name, self.final_score)

        print(f"Score saved for {player_name}: {self.final_score}")
        self.manager.disable()

        from .menu import MenuView
        menu_view = MenuView(self.config)
        self.manager.set_view(menu_view)

    def on_draw(self) -> None:
        """
        Render the UI elements.
        """
        self.clear()
        self.window.default_camera.use()
        self.manager.draw()
