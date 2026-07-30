"""
Logger setup utilities.

This module provides a helper to configure the root logger with a file
handler and a stream handler.
"""

import logging


def setup_logger() -> None:
    """Configure the root logger for the PacMan application.

    This sets the logging level to WARNING, defines a timestamped log
    format, writes logs to `pacman.log`, and also prints them to the
    console.

    Returns:
        None
    """
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
        handlers=[
            logging.FileHandler("pacman.log", mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )
