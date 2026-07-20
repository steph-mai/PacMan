from abc import ABC, abstractmethod
from typing import Any
from src.mlx_wrapper.mlx_engine import MLXEngine


class BaseView(ABC):
    """Abstract base class for view components.

    Provides a minimal interface for views that interact with the MLXEngine.
    Subclasses must implement lifecycle hooks for updating, drawing and
    handling events.

    Args:
        engine: An MLXEngine instance used to render and receive events.
    """

    def __init__(self, engine: MLXEngine) -> None:
        self.engine = engine

    @abstractmethod
    def on_update(self, delta_time: float) -> None:
        """Update the view state.

        Called each frame with the time elapsed since the previous frame.

        Args:
            delta_time: Time elapsed since the last update in seconds.
        """
        pass

    @abstractmethod
    def on_draw(self) -> None:
        """Draw the view.

        Render content to the engine's surface. Called once per frame after
        on_update.
        """
        pass

    @abstractmethod
    def on_event(self, event: Any) -> None:
        """Handle an incoming event.

        Args:
            event: An input event (typically a pygame.Event) to process.
        """
        pass
