"""
Configuration loader for the PacMan application.

This module provides a loader class that reads JSON configuration files
and returns a `Config` instance. It handles missing files, invalid JSON,
and ignores comments in the configuration file.
"""

import json
import logging
import collections
from typing import Any
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
            not path.is_file()
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
            logger.warning("Configuration file is completely empty. "
                           "Loading safe defaults.")
            return Config()

        def _detect_duplicate_keys(
                list_of_pairs: list[tuple[str, Any]]) -> None:
            key_count = collections.Counter(k for k, v in list_of_pairs)
            duplicate_keys = ', '.join(
                k for k, v in key_count.items() if v > 1)

            if len(duplicate_keys) != 0:
                logging.warning("Duplicate keys in config file")

        def _validate_data(list_of_pairs: list[tuple[str, Any]]
                           ) -> dict[str, str | int]:
            _detect_duplicate_keys(list_of_pairs)
            return dict(list_of_pairs)

        try:
            config_dict = json.loads(
                clean_json_str, object_pairs_hook=_validate_data)

            if not isinstance(config_dict, dict):
                logger.warning(f"Configuration root must be a dictionary "
                               f"(got {type(config_dict).__name__}). "
                               f"Loading safe defaults.")
                return Config()

            if not config_dict:
                logger.warning("Configuration JSON is valid but empty {}. "
                               "Loading safe defaults.")
                return Config()

            return Config(**config_dict)

        except json.JSONDecodeError as e:
            logger.warning(f"Malformed JSON at line "
                           f"{e.lineno}, col {e.colno}. "
                           f"Loading safe defaults.")
            return Config()
