from typing import Callable
import pygame
import time
import logging
import sys

logger = logging.getLogger()


class MLXEngine:
    """Wrapper for pygame display and rendering operations.

    This class provides a minimal interface similar to the MiniLibX API
    for creating a window, rendering text, manipulating pixels, and handling
    events.
    """

    def __init__(self) -> None:
        """Initialize pygame and font (MLX-like font)."""
        pygame.init()
        self.font = pygame.font.SysFont(None, 24)
        self.last_time = time.time()

        self.key_hook_function: Callable[[int], None] | None = None
        self.close_hook_function: Callable[[], None] | None = None
        self.loop_hook_function: Callable[[float], None] | None = None

    def create_window(self, width: int, height: int, title: str) -> None:
        """Create a window with the given dimensions and title.

        Args:
            width: Width of the window in pixels.
            height: Height of the window in pixels.
            title: Window title.
        """
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

    def get_pixel_array(self) -> pygame.PixelArray:
        """Return a pixel array for direct pixel access.

        Returns:
            A pygame.PixelArray object for the current screen surface.
        """
        pxarray = pygame.PixelArray(self.screen)
        return pxarray

    def put_string(self,
                   x: int,
                   y: int,
                   text: str,
                   color: tuple[int, int, int]) -> None:
        """Render text at the specified screen coordinates.

        Args:
            x: X position in pixels.
            y: Y position in pixels.
            text: String to render.
            color: RGB color tuple for the text.
        """
        text_to_image = self.font.render(text, True, color)
        self.screen.blit(text_to_image, (x, y))

    def render_frame(self) -> None:
        """Update the display to show the rendered frame."""
        pygame.display.flip()

    def clear_screen(self,
                     color: tuple[int, int, int] = (255, 255, 255)
                     ) -> None:
        """Fill the screen with the specified background color.

        Args:
            color: RGB color tuple used to clear the screen.
        """
        self.screen.fill(color)

    def load_image(self, filepath: str) -> pygame.Surface:
        """Load an image from a file path and return a surface.

        Args:
            filepath: Path to the image file.

        Returns:
            A pygame Surface converted with alpha transparency.
        """
        if not filepath:
            logger.warning(f"Cannot load image from {filepath}. Invalid path.")
        try:
            image = pygame.image.load(filepath)
            return image.convert_alpha()
        except FileNotFoundError as e:
            logger.error(
                f"Failed to load image at {filepath}: {e}. Using fallback.")
            fallback_image: pygame.Surface = pygame.Surface((32, 32))
            fallback_image.fill((255, 0, 255))
            return fallback_image

    def draw_image(self, image: pygame.Surface, x: int, y: int) -> None:
        """Draw an image surface to the screen at the given coordinates.

        Args:
            image: Pygame surface to draw.
            x: X position in pixels.
            y: Y position in pixels.
        """
        self.screen.blit(image, (x, y))

    def mlx_key_hook(self, callback: Callable[[int], None]) -> None:
        self.key_hook_function = callback

    def mlx_close_hook(self, callback: Callable[[], None]) -> None:
        self.close_hook_function = callback

    def mlx_loop_hook(self, callback: Callable[[float], None]) -> None:
        self.loop_hook_function = callback

    def mlx_loop(self, fps: int = 60) -> None:
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
