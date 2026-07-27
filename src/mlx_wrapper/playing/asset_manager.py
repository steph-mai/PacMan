from src.mlx_wrapper.mlx_engine import MLXEngine
from src.obj.entity import NORTH, EAST, SOUTH, WEST


class AssetManager:
    """
    Manages the loading and caching of all visual assets for the game.
    """

    def __init__(self, engine: MLXEngine) -> None:
        """
        Initialize the asset manager and load all required sprites.

        Args:
            engine (MLXEngine): The rendering engine used to load images.
        """
        self.wall_h_img = engine.load_image(
            "inc/images/maze/horizontalwall.png")
        self.wall_v_img = engine.load_image(
            "inc/images/maze/verticalwall.png")

        self.player_images = {
            NORTH: [
                engine.load_image("inc/images/pacman/pacman-up/1.png"),
                engine.load_image("inc/images/pacman/pacman-up/2.png"),
                engine.load_image("inc/images/pacman/pacman-up/3.png")
            ],
            EAST: [
                engine.load_image("inc/images/pacman/pacman-right/1.png"),
                engine.load_image("inc/images/pacman/pacman-right/2.png"),
                engine.load_image("inc/images/pacman/pacman-right/3.png")
            ],
            SOUTH: [
                engine.load_image("inc/images/pacman/pacman-down/1.png"),
                engine.load_image("inc/images/pacman/pacman-down/2.png"),
                engine.load_image("inc/images/pacman/pacman-down/3.png")
            ],
            WEST: [
                engine.load_image("inc/images/pacman/pacman-left/1.png"),
                engine.load_image("inc/images/pacman/pacman-left/2.png"),
                engine.load_image("inc/images/pacman/pacman-left/3.png")
            ]
        }

        self.pacgum_img = engine.load_image("inc/images/maze/other/dot.png")
        self.super_pacgum_img = engine.load_image(
            "inc/images/maze/other/strawberry.png")

        self.blinky_img = engine.load_image("inc/images/ghosts/blinky.png")
        self.inky_img = engine.load_image("inc/images/ghosts/inky.png")
        self.pinky_img = engine.load_image("inc/images/ghosts/pinky.png")
        self.clyde_img = engine.load_image("inc/images/ghosts/clyde.png")

        self.ghost_scared_img = engine.load_image(
            "inc/images/ghosts/blue_ghost.png")
