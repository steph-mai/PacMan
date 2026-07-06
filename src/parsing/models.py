import logging
from pydantic import BaseModel, Field, field_validator, ValidationInfo

logger = logging.getLogger("pacman")


class LevelConfig(BaseModel):
    width: int = Field(default=21)
    height: int = Field(default=21)

    @field_validator("width", "height", mode="after")
    @classmethod
    def clamp_dimension(cls, value: int) -> int:
        if value < 10:
            logger.warning(f"Maze dimension '{value}' is too small. "
                           f"Clamped to 21.")
            return 21
        if value > 40:
            # si > 44 * 44 -> [!] An unexpected error occurred:
            # "maximum recursion depth exceeded"
            logger.warning(f"Maze dimension '{value}' is too big. "
                           f"Clamped to 21.")
            return 21
        return value


class Config(BaseModel):
    level: list[LevelConfig] = Field(
        default_factory=lambda: [LevelConfig(width=21, height=21)])
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
                           "Clamped to 3.")
            return 3

        if lives > 10:
            logger.warning("Number of lives can't be superior to 10. "
                           "Clamped to 3.")
            return 3

        return lives

    @field_validator("pacgum", mode="after")
    @classmethod
    def clamp_pacgum(cls, pacgum: int) -> int:
        if pacgum < 10:
            logger.warning(f"Pacgum count {pacgum} is too low. "
                           f"Clamped to 10.")
            return 10

        if pacgum > 1000:
            logger.warning(f"Pacgum count {pacgum} is too high. "
                           f"Clamped to 10.")
            return 10

        return pacgum

    @field_validator(
            "points_per_pacgum",
            "points_per_super_pacgum",
            "points_per_ghost", mode="after"
            )
    @classmethod
    def clamp_points(cls, points: int, info: ValidationInfo) -> int:
        if points < 0:
            logger.warning(f"{info.field_name} can not be negative. "
                           f"Clamped to 10.")
            return 10

        if points > 10000:
            logger.warning(f"{info.field_name} is too high. "
                           f"Clamped to 10.")
            return 10

        return points

    @field_validator("level_max_time", mode="after")
    @classmethod
    def clamp_level_max_time(cls, level_max_time: int) -> int:
        if level_max_time < 30:
            logger.warning(f"Level_max_time {level_max_time} is too low. "
                           f"Clamped to 30.")
            return 30

        if level_max_time > 300:
            logger.warning(f"Level_max_time {level_max_time} is too high. "
                           f"Clamped to 300.")
            return 300

        return level_max_time
