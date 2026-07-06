"""
Logger setup utilities.

This module provides a helper to configure the root logger with a file
handler and a stream handler, and to silence lower-level logs from
the arcade library.
"""

import logging


def setup_logger() -> None:
    """Configure the root logger for the PacMan application.

    This sets the logging level to WARNING, defines a timestamped log
    format, writes logs to `pacman.log`, and also prints them to the
    console. It also ensures that the `arcade` logger only emits warning
    and more severe messages.

    Returns:
        None
    """
    logging.basicConfig(
        level=logging.WARNING,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        # -8s: force le levelname (niveau de sécurité) à occuper 8 caractères,
        # pour que les | soient alignés dans les logs.
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True,
        # si une autre lib(arcade, mazegen) a déjà appelé BasicConfig,
        # prendra en compte cette config
        handlers=[
            logging.FileHandler("pacman.log", mode="a", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    # pour ne pas afficher les messages d'info/de debug éventuels d'arcade
    logging.getLogger("arcade").setLevel(logging.WARNING)
