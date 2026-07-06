import logging
from pydantic import BaseModel, Field, field_validator, ValidationInfo

logger = logging.getLogger("pacman")

DEFAULT_HIGH_SCORES_FILE_NAME = "highscore.json"
DEFAULT_LIVES = 3
DEFAULT_PACGUM = 42
DEFAULT_SEED = 42

DEFAULT_MIN_PACGUM = 10
DEFAULT_MAX_PACGUM = 10000

MIN_POINTS = 0
MAX_POINTS = 10000
DEFAULT_POINTS_PER_PACGUM = 10
DEFAULT_POINTS_PER_SUPER_PACGUM = 50
DEFAULT_POINTS_PER_GHOST = 200

DEFAULT_TIME = 90
DEFAULT_MIN_TIME = 30
DEFAULT_MAX_TIME = 300

DEFAULT_MIN_MAZE_SIZE = 15
DEFAULT_MAX_MAZE_SIZE = 43
DEFAULT_WIDTH = 21
DEFAULT_HEIGHT = 21


class LevelConfig(BaseModel):
    width: int = Field(default=DEFAULT_WIDTH)
    height: int = Field(default=DEFAULT_HEIGHT)

    @field_validator("width", "height", mode="after")
    @classmethod
    def clamp_dimension(cls, value: int) -> int:
        if value < DEFAULT_MIN_MAZE_SIZE:
            logger.warning(f"Maze dimension '{value}' is too small. "
                           f"Clamped to {DEFAULT_MIN_MAZE_SIZE}.")
            return DEFAULT_MIN_MAZE_SIZE
        if value > DEFAULT_MAX_MAZE_SIZE:
            logger.warning(f"Maze dimension '{value}' is too big. "
                           f"Clamped to {DEFAULT_MAX_MAZE_SIZE}.")
            return DEFAULT_MAX_MAZE_SIZE
        return value


class Config(BaseModel):
    level: list[LevelConfig] = Field(
        default_factory=lambda: [
            LevelConfig(width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT)]
    )
    highscore_filename: str = Field(default=DEFAULT_HIGH_SCORES_FILE_NAME)
    lives: int = Field(default=DEFAULT_LIVES)
    pacgum: int = Field(default=DEFAULT_PACGUM)

    points_per_pacgum: int = Field(default=DEFAULT_POINTS_PER_PACGUM)
    points_per_super_pacgum: int = Field(
        default=DEFAULT_POINTS_PER_SUPER_PACGUM)
    points_per_ghost: int = Field(default=DEFAULT_POINTS_PER_GHOST)
    seed: int = Field(default=DEFAULT_SEED)
    level_max_time: int = Field(default=DEFAULT_TIME)

    @field_validator("lives", mode="after")
    @classmethod
    def clamp_lives(cls, lives: int) -> int:
        if lives < 1:
            logger.warning(f"Number of lives can't be inferior to 1. "
                           f"Clamped to {DEFAULT_LIVES}.")
            return DEFAULT_LIVES

        if lives > 10:
            logger.warning(f"Number of lives can't be superior to 10. "
                           f"Clamped to {DEFAULT_LIVES}.")
            return DEFAULT_LIVES

        return lives

    @field_validator("pacgum", mode="after")
    @classmethod
    def clamp_pacgum(cls, pacgum: int) -> int:
        if pacgum < DEFAULT_MIN_PACGUM:
            logger.warning(f"Pacgum count {pacgum} is too low. "
                           f"Clamped to {DEFAULT_MIN_PACGUM}.")
            return DEFAULT_MIN_PACGUM

        if pacgum > DEFAULT_MAX_PACGUM:
            logger.warning(f"Pacgum count {pacgum} is too high. "
                           f"Clamped to {DEFAULT_MAX_PACGUM}.")
            return DEFAULT_MAX_PACGUM

        return pacgum

    @field_validator(
            "points_per_pacgum",
            "points_per_super_pacgum",
            "points_per_ghost", mode="after"
            )
    @classmethod
    def clamp_points(cls, points: int, info: ValidationInfo) -> int:
        default_values = {
            "points_per_pacgum": DEFAULT_POINTS_PER_PACGUM,
            "points_per_super_pacgum": DEFAULT_POINTS_PER_SUPER_PACGUM,
            "points_per_ghost": DEFAULT_POINTS_PER_GHOST
        }

        if points < MIN_POINTS or points > MAX_POINTS:
            fallback_value = default_values[info.field_name]
            logger.warning(f"{info.field_name} is invalid ({points}). "
                           f"Clamped to {fallback_value}.")
            return fallback_value

        return points

    @field_validator("level_max_time", mode="after")
    @classmethod
    def clamp_level_max_time(cls, level_max_time: int) -> int:
        if level_max_time < DEFAULT_MIN_TIME:
            logger.warning(f"Level_max_time {level_max_time} is too low. "
                           f"Clamped to {DEFAULT_MIN_TIME}.")
            return DEFAULT_MIN_TIME

        if level_max_time > DEFAULT_MAX_TIME:
            logger.warning(f"Level_max_time {level_max_time} is too high. "
                           f"Clamped to {DEFAULT_MAX_TIME}.")
            return DEFAULT_MAX_TIME

        return level_max_time
