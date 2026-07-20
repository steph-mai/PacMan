import arcade
import arcade.gui
# from arcade.gui.widgets import UISpriteWidget
from .game_view import GameView
from src.parsing.models import Config


class MenuView(arcade.View):
    """Main menu view for map selection."""

    def __init__(self, config: Config) -> None:
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.v_box = arcade.gui.UIBoxLayout()
        self.t_box = arcade.gui.UIBoxLayout()
        self.config = config
        # self.background = arcade.Sprite("inc/UI/background.png")
        # self.background_list: arcade.SpriteList[arcade.Sprite] = \
        #     arcade.SpriteList()
        # self.background_list.append(self.background)
        # logo_pacman = arcade.Sprite("inc/UI/logo_fly_in.png", scale=0.12)
        # logins = arcade.Sprite("inc/UI/user.png", scale=0.2)
        # pacman_button_style = {
        #     "normal": {
        #         "font_size": 14,
        #         "font_color": arcade.color.WHITE,
        #         "bg": (13, 20, 56, 120),
        #     },
        #     "hover": {
        #         "font_size": 15,
        #         "font_color": arcade.color.WHITE,
        #         "bg": (170, 123, 58, 120),
        #     },
        #     "press": {
        #         "font_size": 16,
        #         "font_color": arcade.color.WHITE,
        #         "bg": (170, 123, 58, 200),
        #     }
        # }

        # self.logo_widget = UISpriteWidget(sprite=logo_pacman,
        #                                   width=logo_pacman.width,
        #                                   height=logo_pacman.height)
        # self.t_box.add(self.logo_widget.with_padding(bottom=20))

        # self.login_widget = UISpriteWidget(sprite=logins,
        #                                    width=logins.width,
        #                                    height=logins.height)
        # self.t_box.add(self.login_widget.with_padding(bottom=20))

        game_btn = arcade.gui.\
            UIFlatButton(text="Launch Game",
                         width=300)  # , style=pacman_button_style
        self.v_box.add(game_btn.with_padding(bottom=15))

        quit_btn = arcade.gui.\
            UIFlatButton(text="Quit",
                         width=300)  # , style=pacman_button_style
        self.v_box.add(quit_btn)

        @game_btn.event("on_click")
        def on_click_game(event: arcade.gui.UIOnClickEvent) -> None:
            self.window.show_view(GameView(self.config))

        @quit_btn.event("on_click")
        def on_click_quit(event: arcade.gui.UIOnClickEvent) -> None:
            arcade.exit()

        anchor = arcade.gui.UIAnchorLayout()

        anchor.add(child=self.v_box,
                   anchor_x="left",
                   anchor_y="bottom",
                   align_x=self.width/2 - game_btn.width/2,
                   align_y=self.height/2 - (game_btn.height
                                            + quit_btn.height) / 2)

        # anchor.add(child=self.t_box,
        #            anchor_x="right",
        #            anchor_y="bottom",
        #            align_x=-300,
        #            align_y=200)

        self.manager.add(anchor)

    def on_show_view(self) -> None:
        """Handle view activation."""
        arcade.set_background_color(arcade.color.ASH_GREY)
        self.on_resize(self.window.width, self.window.height)
        self.manager.enable()

    def on_resize(self, width: int, height: int) -> None:
        """Handle window resizing.

        Args:
            width: The newly requested window width.
            height: The newly requested window height.
        """
        super().on_resize(width, height)

        # self.background.width = width
        # self.background.height = height
        # self.background.center_x = width / 2
        # self.background.center_y = height / 2

    def on_hide_view(self) -> None:
        """Disable interactions when view is hidden."""
        self.manager.disable()

    def on_draw(self) -> None:
        """Render the menu view elements."""
        self.clear()
        self.window.default_camera.use()
        # self.background_list.draw()
        self.manager.draw()
