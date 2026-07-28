"""
Game manager for the PacMan application using the MLXEngine wrapper.

This module provides GameManager, a simple runner that wires the MLXEngine
to a view (BaseView). It handles window creation, the main loop callbacks,
and delegates input, update and draw events to the current view.

"""
import pygame
from src.mlx_wrapper.mlx_engine import MLXEngine
from src.mlx_wrapper.base_view import BaseView
import logging
import sys

logger = logging.getLogger()

FPS = 60


class GameManager:
    """Manage the game window, event hooks and view lifecycle.

    The GameManager creates the MLX window, registers callbacks for key
    events, window close and the main loop, and delegates behavior to
    the currently set BaseView instance.

    Attributes:
        width (int): Window width in pixels.
        height (int): Window height in pixels.
        title (str): Window title.
        engine (MLXEngine): The MLX engine instance used for rendering.
        current_view (BaseView | None): Currently active view.
        running (bool): Whether the game loop should continue running.
    """

    def __init__(self, width: int, height: int, title: str):
        """Initialize the GameManager and create the MLX window.

        Args:
            width (int): Window width in pixels.
            height (int): Window height in pixels.
            title (str): Window title.

        Returns:
            None
        """
        self.width = width
        self.height = height
        self.title = title
        self.engine = MLXEngine()
        self.engine.create_window(
            self.width, self.height, self.title)
        self.current_view: BaseView | None = None
        self.running: bool = True

    def set_view(self, view: BaseView) -> None:
        """Set the active view to receive input, update and draw calls.

        Args:
            view (BaseView): The view to set as active.

        Returns:
            None
        """
        self.current_view = view

    def on_key_press(self, keycode: int) -> None:
        """Handle a key press event by delegating to the current view.

        Args:
            keycode (int): Numeric key code received from the engine.

        Returns:
            None
        """
        if self.current_view:
            self.current_view.on_key_press(keycode)

    def on_close(self) -> None:
        """Handle the window close event and terminate the application.

        Delegates to the current view if present, logs the closure,
        quits pygame and exits the process.

        Returns:
            None
        """
        if self.current_view:
            logger.info("Game closed by user.")
            pygame.quit()
            sys.exit(0)

    def on_loop(self, delta_time: float) -> None:
        """Per-frame loop callback: update, clear, draw and render.

        This is called by the MLX engine each frame with the elapsed
        time since the last call.

        Args:
            delta_time (float): Time elapsed since the last frame in seconds.

        Returns:
            None
        """
        if self.current_view:
            self.current_view.on_update(delta_time)
            self.engine.clear_screen()
            self.current_view.on_draw()
            self.engine.render_frame()

    def run(self) -> None:
        """Register engine hooks and start the engine main loop.

        The method wires the GameManager callbacks into the MLX engine and
        starts the engine loop at the configured FPS.

        Returns:
            None
        """
        self.engine.mlx_key_hook(self.on_key_press)
        self.engine.mlx_close_hook(self.on_close)
        self.engine.mlx_loop_hook(self.on_loop)

        self.engine.mlx_loop(fps=60)
