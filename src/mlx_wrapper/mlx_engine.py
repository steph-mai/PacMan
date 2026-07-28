"""
MLX-like pygame engine wrapper.

Provides a small wrapper around pygame to offer a MiniLibX-like API for
window creation, text rendering, pixel access, image loading/drawing, and
event hooks.
"""
from typing import Callable
import pygame
import time
import logging
import sys
import os

logger = logging.getLogger()


class MLXEngine:
    """Wrapper for pygame display and rendering operations.

    This class provides a minimal interface similar to the MiniLibX API
    for creating a window, rendering text, manipulating pixels, and handling
    events.
    """

    def __init__(self) -> None:
        """Initialize pygame and fonts (MLX-like fonts).

        Initializes the pygame library and creates three built-in fonts
        used by the convenience text rendering methods.

        Returns:
            None
        """
        pygame.init()
        self.titlefont = pygame.font.SysFont(None, 100)
        self.font = pygame.font.SysFont(None, 40)
        self.smallfont = pygame.font.SysFont(None, 24)
        self.last_time = time.time()

        self.key_hook_function: Callable[[int], None] | None = None
        self.close_hook_function: Callable[[], None] | None = None
        self.loop_hook_function: Callable[[float], None] | None = None

    def create_window(self, width: int, height: int, title: str) -> None:
        """Create a window with the given dimensions and title.

        Args:
            width: Window width in pixels.
            height: Window height in pixels.
            title: Window title to display in the window chrome.

        Returns:
            None
        """
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.background_image = pygame.Surface((width, height))
        self.background_image.fill((0, 0, 0))

    def put_string(self,
                   x: int,
                   y: int,
                   text: str,
                   color: tuple[int, int, int]) -> None:
        """Render a regular-sized string on screen.

        Args:
            x: X coordinate in pixels.
            y: Y coordinate in pixels.
            text: Text to render.
            color: RGB color tuple.

        Returns:
            None
        """
        text_to_image = self.font.render(text, True, color)
        self.screen.blit(text_to_image, (x, y))

    def put_title_string(self,
                         x: int,
                         y: int,
                         text: str,
                         color: tuple[int, int, int]) -> None:
        """Render a title-sized string on screen.

        Args:
            x: X coordinate in pixels.
            y: Y coordinate in pixels.
            text: Text to render.
            color: RGB color tuple.

        Returns:
            None
        """
        text_to_image = self.titlefont.render(text, True, color)
        self.screen.blit(text_to_image, (x, y))

    def put_small_string(self,
                         x: int,
                         y: int,
                         text: str,
                         color: tuple[int, int, int]) -> None:
        """Render small text at the specified screen coordinates.

        Args:
            x: X coordinate in pixels.
            y: Y coordinate in pixels.
            text: Text to render.
            color: RGB color tuple.

        Returns:
            None
        """
        text_to_image = self.smallfont.render(text, True, color)
        self.screen.blit(text_to_image, (x, y))

    def render_frame(self) -> None:
        """Present the current frame to the display.

        Calls pygame.display.flip() to update the full display surface.

        Returns:
            None
        """
        pygame.display.flip()

    def clear_screen(self) -> None:
        """Clear the screen using the configured background image.

        Blits the background image onto the screen surface at (0, 0).

        Returns:
            None
        """
        self.screen.blit(self.background_image, (0, 0))

    def load_image(self, filepath: str) -> pygame.Surface:
        """Load an image from disk or package data.

        If running from a bundled executable, the filepath is resolved
        relative to the PyInstaller _MEIPASS directory. On failure a
        magenta fallback surface is returned.

        Args:
            filepath: Path to the image file.

        Returns:
            A pygame.Surface with the loaded image or a fallback surface.
        """
        if hasattr(sys, '_MEIPASS'):
            filepath = os.path.join(sys._MEIPASS, filepath)
        if not filepath:
            logger.warning(f"Cannot load image from {filepath}. Invalid path.")
        try:
            image = pygame.image.load(filepath)
            return image
        except FileNotFoundError as e:
            logger.error(
                f"Failed to load image at {filepath}: {e}. Using fallback.")
            fallback_image: pygame.Surface = pygame.Surface((32, 32))
            fallback_image.fill((255, 0, 255))
            return fallback_image

    def draw_image(self, image: pygame.Surface, x: int, y: int) -> None:
        """Draw a surface onto the screen at the given coordinates.

        Args:
            image: Pygame Surface to draw.
            x: X coordinate in pixels.
            y: Y coordinate in pixels.

        Returns:
            None
        """
        self.screen.blit(image, (x, y))

    def mlx_key_hook(self, callback: Callable[[int], None]) -> None:
        """Register a key press callback.

        Args:
            callback: Callable receiving a single integer key code.

        Returns:
            None
        """
        self.key_hook_function = callback

    def mlx_close_hook(self, callback: Callable[[], None]) -> None:
        """Register a window close callback.

        Args:
            callback: Callable called when the window is closed.

        Returns:
            None
        """
        self.close_hook_function = callback

    def mlx_loop_hook(self, callback: Callable[[float], None]) -> None:
        """Register the per-frame loop callback.

        Args:
            callback: Callable receiving delta_time (seconds) since last frame.

        Returns:
            None
        """
        self.loop_hook_function = callback

    def mlx_loop(self, fps: int = 60) -> None:
        """Start the main loop, dispatching events and calling hooks.

        The loop enforces the target FPS by sleeping when necessary and
        computes delta_time passed to the loop hook.

        Args:
            fps: Target frames per second.

        Returns:
            None
        """
        while True:
            current_time = time.time()
            delta_time = current_time - self.last_time
            time_to_wait = (1 / fps) - delta_time

            if time_to_wait > 0:
                time.sleep(time_to_wait)
                current_time = time.time()
                delta_time = current_time - self.last_time

            self.last_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.close_hook_function:
                        self.close_hook_function()
                    else:
                        pygame.quit()
                        sys.exit(0)

                elif event.type == pygame.KEYDOWN:
                    if self.key_hook_function:
                        self.key_hook_function(event.key)
            if self.loop_hook_function:
                self.loop_hook_function(delta_time)
