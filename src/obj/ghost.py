import arcade
from enum import Enum, auto
from src.parsing.models import Config

RESPAWN_DELAY: float = 10.0

class GhostState(Enum):
    CHASING = auto()
    RUNNING_AWAY = auto()
    DEAD = auto()


class Ghost:
    def __init__(self, start_row: int, start_col: int, max_rows: int, max_cols: int) -> None:
        self.spawn_row: int = start_row
        self.spawn_col: int = start_col
        self.start_row: int = start_row
        self.start_col: int = start_col
        self.max_rows: int = max_rows
        self.max_cols: int = max_cols
        self.state: GhostState = GhostState.CHASING

        self.death_timer: float = 0.0
        self.respawn_delay = RESPAWN_DELAY

        self.current_direction = 0
        # au début le fantôme est immobile.
        # On ne bloque aucune direction
        # par le suite on l'empêche de faire 1/2 tour spontanément.

    #def update(self, delta_time: float, )





