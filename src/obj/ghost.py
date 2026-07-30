"""Ghost entity module.

This module defines the Ghost base class and ghost-related state definitions.
"""

import random
from src.obj.entity import Entity, NORTH, SOUTH, EAST, WEST
from src.obj.player import Player
from src.ai.states import GhostState
from abc import ABC, abstractmethod

RESPAWN_DELAY: float = 5.0
SCARED_DELAY: float = 10.0
MOVE_DELAY: float = 0.25
FLASH_DELAY: float = 3.0
SCATTER_DELAY: float = 3.0
CHASING_DELAY: float = 8.0


RGBcolor = tuple[int, int, int]


class Ghost(Entity, ABC):
    """Represent a ghost in the Pac-Man maze.

    This is a base class for concrete ghost implementations.
    """

    def __init__(
        self,
        start_row: int,
        start_col: int,
        max_rows: int,
        max_cols: int,
        color: RGBcolor,
    ) -> None:
        """Initialize a ghost instance.

        Args:
            start_row: The initial row position of the ghost.
            start_col: The initial column position of the ghost.
            max_rows: The total number of rows in the maze.
            max_cols: The total number of columns in the maze.
            color: The RGB color of the ghost.
        """

        super().__init__(start_row, start_col, MOVE_DELAY)
        self.spawn_row: int = start_row
        self.spawn_col: int = start_col
        self.max_rows: int = max_rows
        self.max_cols: int = max_cols
        self.state: GhostState = GhostState.CHASING
        self.color = color
        self.death_timer: float = 0.0
        self.scared_timer: float = 0.0
        self.scared_delay = SCARED_DELAY
        self.respawn_delay = RESPAWN_DELAY
        self.is_scatter_phase: bool = False

    @abstractmethod
    def _get_next_direction(
            self, maze: list[list[int]], player: Player) -> int:
        """Return the next direction for the ghost.

        Args:
            maze: A 2D grid representing the maze layout.
            player: The player entity used to determine the ghost behavior.

        Returns:
            The next movement direction to apply.
        """
        pass

    @staticmethod
    def _get_reverse_direction(direction: int) -> int:
        """Return the opposite maze direction for a given direction.

        Args:
            direction (int): One of NORTH, EAST, SOUTH, or WEST.

        Returns:
            int: The opposite direction constant, or 0 if the input is invalid.
        """
        if direction == NORTH:
            return SOUTH
        if direction == SOUTH:
            return NORTH
        if direction == EAST:
            return WEST
        if direction == WEST:
            return EAST
        return 0

    @staticmethod
    def _calculate_as_the_crow_flies_distance(
            row1: int, col1: int, row2: int, col2: int) -> int:
        """Calculate squared Euclidean distance between two grid positions.

        Using squared distance avoids the cost of a square root while
        preserving ordering comparisons.

        Args:
            row1: Row of first position.
            col1: Column of first position.
            row2: Row of second position.
            col2: Column of second position.

        Returns:
            int: Squared distance between the two positions.
        """
        return (row1 - row2)**2 + (col1 - col2)**2

    def _get_valid_directions(
            self,
            maze: list[list[int]]) -> list[int]:
        """Return valid movement directions from the ghost's current cell.

        The ghost may not move through walls, and it avoids reversing
        direction unless it has no other choice.

        Args:
            maze (list[list[int]]): The maze wall grid.

        Returns:
            list[int]: A list of valid direction constants.
        """
        current_walls = maze[self.row][self.col]

        valid_directions = []
        if not (current_walls & NORTH):
            valid_directions.append(NORTH)
        if not (current_walls & WEST):
            valid_directions.append(WEST)
        if not (current_walls & SOUTH):
            valid_directions.append(SOUTH)
        if not (current_walls & EAST):
            valid_directions.append(EAST)
        reverse_direction = self._get_reverse_direction(self.current_direction)
        if reverse_direction in valid_directions and len(valid_directions) > 1:
            valid_directions.remove(reverse_direction)

        return valid_directions

    def _get_direction_towards_target(
            self, maze: list[list[int]],
            target_row: int, target_col: int
            ) -> int:
        """Select the direction that moves the ghost closest to a target.

        The ghost evaluates all valid adjacent moves and chooses the one
        that minimizes the straight-line distance to the target position.

        Args:
            maze (list[list[int]]): The maze wall grid.
            target_row (int): Target row coordinate.
            target_col (int): Target column coordinate.

        Returns:
            int: The best direction constant to move toward the target, or 0.
        """
        valid_directions = self._get_valid_directions(maze)
        if not valid_directions:
            return 0

        best_direction = 0
        min_distance = float('inf')

        for direction in valid_directions:
            next_row = self.row
            next_col = self.col
            if direction == NORTH:
                next_row -= 1
            elif direction == EAST:
                next_col += 1
            elif direction == SOUTH:
                next_row += 1
            elif direction == WEST:
                next_col -= 1

            distance = self._calculate_as_the_crow_flies_distance(
                next_row,
                next_col,
                target_row,
                target_col)

            if distance < min_distance:
                min_distance = distance
                best_direction = direction

        return best_direction

    import random

    def _choose_direction(
        self,
        maze: list[list[int]],
        player: Player,
    ) -> None:
        """Choose and apply a movement direction based on the ghost state.

        Args:
            maze: A 2D grid representing the maze layout.
            player: The player entity used to determine the ghost behavior.
        """

        direction = 0

        if self.state == GhostState.RUNNING_AWAY:
            valid_directions = self._get_valid_directions(maze)
            if valid_directions:
                direction = random.choice(valid_directions)

        elif self.state == GhostState.DEAD:
            direction = 0

        elif self.state == GhostState.CHASING:
            if self.is_scatter_phase:
                valid_directions = self._get_valid_directions(maze)
                if valid_directions:
                    direction = random.choice(valid_directions)
            else:
                direction = self._get_next_direction(maze, player)

        if direction != 0:
            self.current_direction = direction
            self._apply_direction(direction)

    def reverse_course(self) -> None:
        """Force the ghost to reverse its current direction immediately."""

        reverse_dir = self._get_reverse_direction(self.current_direction)
        if reverse_dir != 0:
            self.current_direction = reverse_dir
            self._apply_direction(reverse_dir)

    def update_movement(
        self,
        delta_time: float,
        maze: list[list[int]],
        player: Player,
    ) -> None:
        """Update the ghost's movement state.

        Args:
            delta_time: The elapsed time since the previous update.
            maze: A 2D grid representing the maze layout.
            player: The player entity used to determine the ghost behavior.
        """

        if self.state == GhostState.DEAD:
            self.death_timer -= delta_time
            if self.death_timer <= 0:
                self.state = GhostState.CHASING
            return

        if self.state == GhostState.RUNNING_AWAY:
            self.scared_timer -= delta_time
            if self.scared_timer <= 0:
                self.state = GhostState.CHASING

        self.move_timer += delta_time
        if self.move_timer < self.move_delay:
            return
        self.move_timer = 0.0

        self._choose_direction(maze, player)

    def die(self) -> None:
        """Mark the ghost as dead and reset its position."""
        self.state = GhostState.DEAD
        self.death_timer = self.respawn_delay
        self.reset_position()

    def is_flashing(self) -> bool:
        """Return whether the ghost is in its scared state and flashing.

        Returns:
            True if the ghost is scared and its scare timer is below the flash
            threshold.
        """
        return self.state == GhostState.RUNNING_AWAY and\
            self.scared_timer <= FLASH_DELAY
