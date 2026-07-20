import pygame
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.base_view import BaseView

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

    def run(self) -> None:
        while self.running:
            delta_time = self.engine.tick(FPS)

            events = self.engine.get_events()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                    continue
                if self.current_view:
                    self.current_view.on_event(event)

            if self.current_view:
                self.current_view.on_update(delta_time)
                self.engine.clear_screen()
                self.current_view.on_draw()
                self.engine.render_frame()

        pygame.quit
