import logging
from pydantic import BaseModel, Field, field_validator
from typing import Any, List

logger = logging.getLogger("pacman")


class LevelConfig(BaseModel):
    width: int = Field(default=20)
    height: int = Field(default=20)

    @field_validator("width", "height", mode="after")
    @classmethod
    def clamp_dimension(cls, value: int) -> int:
        if value < 10:
            logger.warning(f"Maze dimension '{value}' is too small. "
                           f"Clamped to 20")
            return 20
        if value > 100:
            logger.warning(f"Maze dimension '{value}' is too big. "
                           f"Clamped to 20")
            return 20
        return value

class Config(BaseModel):
    level: list[LevelConfig] = Field(
        default_factory=lambda: [LevelConfig(width=20, height=20)])
    highscore_filename: str = Field(default="highscore.json")
    lives: int = Field(default=3)
    pacgum: int = Field(default=42)

    points_per_pacgum: int = Field(default=10)
    points_per_super_pacgum: int = Field(default=50)
    points_per_ghost: int = Field(default=200)
    seed: int = Field(default=42)
    level_max_time: int = Field(default=90)

    @field_validator("lives", mode="after")
    @classmethod
    def clamp_lives(cls, lives: int) -> int:
        if lives < 1:
            logger.warning("Number of lives can't be inferior to 1. "
                           "Clamped to 3")
            return 3

        if lives > 10:
            logger.warning("Number of lives can't be superior to 10. "
                           "Clamped to 3")
            return 3

        return lives
