"""Parsing model definitions for PacMan configuration.

Defines default constants and Pydantic models for level and game configuration.
"""

import logging
from typing import Any
from pydantic import (
    BaseModel, Field, field_validator, ValidationInfo, model_validator)

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
    """Configuration for a single game level.

    Attributes:
        width: Level width in cells.
        height: Level height in cells.
    """
    width: int = Field(default=DEFAULT_WIDTH)
    height: int = Field(default=DEFAULT_HEIGHT)

    @model_validator(mode="before")
    @classmethod
    def pre_validate_level_types(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        dimensions = {"width": DEFAULT_WIDTH, "height": DEFAULT_HEIGHT}
        for field, default_val in dimensions.items():
            if field not in data:
                logger.warning(f"Level field '{field}' is missing. "
                               f"Clamped to {default_val}.")
                data[field] = default_val
            else:
                val = data[field]
                if type(val) is not int or isinstance(val, bool):
                    logger.warning(f"Level field '{field}' has invalid type "
                                   f"({type(val).__name__}). Expected int. "
                                   f"Clamped to {default_val}.")
                    data[field] = default_val
        return data

    @field_validator("width", "height", mode="after")
    @classmethod
    def clamp_dimension(cls, value: int) -> int:
        """Clamp maze dimensions to allowed limits.

        Args:
            value: Input dimension value.

        Returns:
            The clamped dimension value.
        """
        if value < DEFAULT_MIN_MAZE_SIZE:
            logger.warning(f"Maze dimension '{value}' is too small. "
                           f"Clamped to {DEFAULT_MIN_MAZE_SIZE}.")
            return DEFAULT_MIN_MAZE_SIZE
        if value > DEFAULT_MAX_MAZE_SIZE:
            logger.warning(f"Maze dimension '{value}' is too big. "
                           f"Clamped to {DEFAULT_MAX_MAZE_SIZE}.")
            return DEFAULT_MAX_MAZE_SIZE
        return value


def get_default_levels() -> list[LevelConfig]:
    """
    Provide default levels config and log a warning when field is missing.

    Returns:
        Ten default levels
    """
    logger.warning(f"Field 'level' is totally missing from config. "
                   f"Clamped to 10 default levels: "
                   f"{DEFAULT_WIDTH} * {DEFAULT_HEIGHT}")
    return [LevelConfig(
        width=DEFAULT_WIDTH, height=DEFAULT_HEIGHT
        ) for _ in range(10)]


class Config(BaseModel):
    """Game configuration model.

    Attributes:
        level: List of level configurations.
        highscore_filename: High score file name.
        lives: Number of player lives.
        pacgum: Number of pacgum items.
        points_per_pacgum: Points awarded per pacgum.
        points_per_super_pacgum: Points awarded per super pacgum.
        points_per_ghost: Points awarded per ghost.
        seed: Random seed for level generation.
        level_max_time: Maximum time for each level.
    """

    level: list[LevelConfig] = Field(default_factory=get_default_levels)
    highscore_filename: str = Field(default=DEFAULT_HIGH_SCORES_FILE_NAME)
    lives: int = Field(default=DEFAULT_LIVES)
    pacgum: int = Field(default=DEFAULT_PACGUM)

    points_per_pacgum: int = Field(default=DEFAULT_POINTS_PER_PACGUM)
    points_per_super_pacgum: int = Field(
        default=DEFAULT_POINTS_PER_SUPER_PACGUM)
    points_per_ghost: int = Field(default=DEFAULT_POINTS_PER_GHOST)
    seed: int = Field(default=DEFAULT_SEED)
    level_max_time: int = Field(default=DEFAULT_TIME)

    @model_validator(mode="before")
    @classmethod
    def pre_validate_types_and_missing(cls, data: Any) -> Any:
        """
        Intercepts the raw JSON to verify the existence of fields and
        their strict types before Pydantic gets involved.
        """
        if not isinstance(data, dict):
            return data

        if not data:
            data["level"] = [
                {
                    "width": DEFAULT_WIDTH, "height": DEFAULT_HEIGHT
                } for _ in range(10)
                ]
            return data

        int_fields = {
            "lives": DEFAULT_LIVES,
            "pacgum": DEFAULT_PACGUM,
            "points_per_pacgum": DEFAULT_POINTS_PER_PACGUM,
            "points_per_super_pacgum": DEFAULT_POINTS_PER_SUPER_PACGUM,
            "points_per_ghost": DEFAULT_POINTS_PER_GHOST,
            "seed": DEFAULT_SEED,
            "level_max_time": DEFAULT_TIME
        }

        for field, default_val in int_fields.items():
            if field not in data:
                logger.warning(f"Field '{field}' is missing. "
                               f"Clamped to default value: {default_val}")
                data[field] = default_val
            else:
                val = data[field]
                if type(val) is not int or isinstance(val, bool):
                    logger.warning(
                        f"Field '{field}' has invalid type "
                        f"({type(val).__name__}). "
                        f"Expected int. Clamped to default value: "
                        f"{default_val}"
                    )
                    data[field] = default_val

        if "highscore_filename" not in data:
            logger.warning(f"Field 'highscore_filename' is missing. "
                           f"Clamped to default value: "
                           f"{DEFAULT_HIGH_SCORES_FILE_NAME}")
            data["highscore_filename"] = DEFAULT_HIGH_SCORES_FILE_NAME
        elif (
            not isinstance(data["highscore_filename"], str)
            or not data["highscore_filename"].strip()
        ):
            logger.warning(f"Field 'highscore_filename' has invalid type "
                           f"({type(data['highscore_filename']).__name__}). "
                           f"Expected str. Clamped to default value: "
                           f"{DEFAULT_HIGH_SCORES_FILE_NAME}")
            data["highscore_filename"] = DEFAULT_HIGH_SCORES_FILE_NAME

        return data

    @field_validator("lives", mode="after")
    @classmethod
    def clamp_lives(cls, lives: int) -> int:
        """Clamp the number of lives to a valid range.

        Args:
            lives: Requested number of lives.

        Returns:
            The validated number of lives.
        """
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
        """Clamp the number of pacgum items to valid limits.

        Args:
            pacgum: Requested pacgum count.

        Returns:
            The validated pacgum count.
        """
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
        """Clamp point values to a valid range.

        Args:
            points: Requested points value.
            info: Validation metadata.

        Returns:
            The validated point value.
        """
        default_values = {
            "points_per_pacgum": DEFAULT_POINTS_PER_PACGUM,
            "points_per_super_pacgum": DEFAULT_POINTS_PER_SUPER_PACGUM,
            "points_per_ghost": DEFAULT_POINTS_PER_GHOST
        }

        if points < MIN_POINTS or points > MAX_POINTS:
            assert info.field_name is not None, (
                "field_name cannot be None in a field_validator")
            fallback_value = default_values[info.field_name]
            logger.warning(f"{info.field_name} is invalid ({points}). "
                           f"Clamped to {fallback_value}.")
            return fallback_value

        return points

    @field_validator("level_max_time", mode="after")
    @classmethod
    def clamp_level_max_time(cls, level_max_time: int) -> int:
        """Clamp the maximum level time to allowed limits.

        Args:
            level_max_time: Requested level time.

        Returns:
            The validated level time.
        """
        if level_max_time < DEFAULT_MIN_TIME:
            logger.warning(f"Level_max_time {level_max_time} is too low. "
                           f"Clamped to {DEFAULT_MIN_TIME}.")
            return DEFAULT_MIN_TIME

        if level_max_time > DEFAULT_MAX_TIME:
            logger.warning(f"Level_max_time {level_max_time} is too high. "
                           f"Clamped to {DEFAULT_MAX_TIME}.")
            return DEFAULT_MAX_TIME

        return level_max_time

    @field_validator("level", mode="before")
    @classmethod
    def get_validate_levels_value(cls, value: Any) -> list[dict[str, int]]:
        """
        Validate the level values.
        Ensures the list contains at least 10 levels to respect game rules.
        """
        valid_levels = []

        if not value or not isinstance(value, list):
            logger.warning(f"Invalid value for level field: {value}. "
                           f"Clamped to 10 default levels.")
        else:
            for item in value:
                if isinstance(item, dict):
                    valid_levels.append(item)
                else:
                    logger.warning(
                        f"Ignored invalid level item (expected dict, "
                        f"got {type(item).__name__}): {item}"
                    )

        if len(valid_levels) < 10:
            logger.warning(f"Only {len(valid_levels)} valid levels found. "
                           f"Padding with default levels to reach 10.")
            while len(valid_levels) < 10:
                valid_levels.append(
                    {"width": DEFAULT_WIDTH, "height": DEFAULT_HEIGHT})

        return valid_levels
