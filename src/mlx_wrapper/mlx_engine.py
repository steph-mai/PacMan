import pygame
import logging

logger = logging.getLogger()


class MLXEngine:
    """Wrapper for pygame display and rendering operations.

    This class provides a minimal interface similar to the MiniLibX API
    for creating a window, rendering text, manipulating pixels, and handling
    events.
    """

    def __init__(self) -> None:
        """Initialize pygame, font, and clock."""
        pygame.init()
        self.font = pygame.font.SysFont("monospace", 16)
        self.clock = pygame.time.Clock()

    def create_window(self, width: int, height: int, title: str):
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

    def put_string(self, x: int, y: int, text: str, color: tuple) -> None:
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

    def clear_screen(self, color=(255, 255, 255)) -> None:
        """Fill the screen with the specified background color.

        Args:
            color: RGB color tuple used to clear the screen.
        """
        self.screen.fill(color)

    def tick(self, fps: int = 60) -> float:
        """Advance the clock and return the elapsed time in seconds.

        Args:
            fps: Target frames per second.

        Returns:
            The time elapsed since the last call in seconds.
        """
        ms_passed = self.clock.tick(fps)
        delta_time = ms_passed / 1000
        return delta_time

    def get_events(self) -> list[pygame.event.Event]:
        """Return the list of pending pygame events.

        Returns:
            A list of pygame Event objects.
        """
        return pygame.event.get()

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

    # ADD FOR TEST ONLY
    def draw_rectangle(self, x: int, y: int, width: int, height: int, color: tuple[int, int, int]) -> None:
        pygame.draw.rect(self.screen, color, (x, y, width, height))

    def draw_circle(self, center_x: int, center_y: int, radius: int, color: tuple[int, int, int]) -> None:
        pygame.draw.circle(self.screen, color, (center_x, center_y), radius)

    def draw_line(self, start_x: int, start_y: int, end_x: int, end_y: int, color: tuple[int, int, int], thickness: int = 2) -> None:
        pygame.draw.line(self.screen, color, (start_x, start_y), (end_x, end_y), thickness)
