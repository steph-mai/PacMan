"""
Configuration loader for the PacMan application.

This module provides a loader class that reads JSON configuration files
and returns a `Config` instance. It handles missing files, invalid JSON,
and ignores comments in the configuration file.
"""

import json
import logging
from pathlib import Path
from src.parsing.models import Config

logger = logging.getLogger("pacman")


class Loader:
    """Loader for JSON configuration files."""

    def config_file_load(self, file_name: str) -> Config:
        """Load configuration from a JSON file.

        The file is read and cleaned of blank lines and comment lines
        starting with `#` or `//`. If the file is missing, invalid,
        empty, or contains malformed JSON, a default `Config` instance
        is returned.

        Args:
            file_name: Path to the JSON configuration file.

        Returns:
            A `Config` object loaded from the file or a default
            `Config` instance on error.
        """
        path = Path(file_name)

        if (
            not path.exists() or
            not path.is_file() or
            path.suffix.lower() != ".json"
        ):
            logger.warning(f"Invalid or missing file '{file_name}'. "
                           f"Loading safe defaults.")
            return Config()

        try:
            with open(path, mode="r", encoding="utf-8") as f:
                lines = f.readlines()
        except OSError as e:
            logger.warning(f"Could not read '{file_name}' ({e}). "
                           f"Loading safe defaults.")
            return Config()

        clean_lines = []
        for line in lines:
            stripped_line = line.strip()
            if not stripped_line or stripped_line.startswith(("#", "//")):
                continue
            clean_lines.append(line)

        clean_json_str = "".join(clean_lines)

        if not clean_json_str.strip():
            logger.warning(f"file '{file_name}' is empty. "
                           f"Loading safe defaults.")
            return Config()
        try:
            config_dict = json.loads(clean_json_str)
            return Config(**config_dict)

        except json.JSONDecodeError as e:
            logger.warning(f"Malformed JSON at line "
                           f"{e.lineno}, col {e.colno}. "
                           f"Loading safe defaults.")
            return Config()

        except Exception as e:
            logger.warning(f"Configuration logic error ({e}). "
                           f"Loading safe defaults.")
            return Config()
