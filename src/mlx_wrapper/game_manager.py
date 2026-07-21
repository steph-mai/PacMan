import pygame
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.base_view import BaseView
import logging
import sys

logger = logging.getLogger()

FPS = 60


class GameManager():
    def __init__(self, width: int, height: int, title: str):
        self.width = width
        self.height = height
        self.title = title
        self.engine = MLXEngine()
        self.window = self.engine.create_window(
            self.width, self.height, self.title)
        self.current_view: BaseView | None = None
        self.running: bool = True

    def set_view(self, view: BaseView) -> None:
        self.current_view = view

    def on_key_press(self, keycode: int) -> None:
        if self.current_view:
            self.current_view.on_key_press(keycode)

    def on_close(self) -> None:
        if self.current_view:
            logger.info("Game closed by user.")
            pygame.quit()
            sys.exit(0)

    def on_loop(self, delta_time: float) -> None:
        if self.current_view:
            self.current_view.on_update(delta_time)
            self.engine.clear_screen()
            self.current_view.on_draw()
            self.engine.render_frame()

    def run(self) -> None:
        self.engine.mlx_key_hook(self.on_key_press)
        self.engine.mlx_close_hook(self.on_close)
        self.engine.mlx_loop_hook(self.on_loop)

        self.engine.mlx_loop(fps=60)
