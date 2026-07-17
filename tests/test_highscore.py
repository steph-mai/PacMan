import json
import logging
from pathlib import Path
from typing import Any
from pytest import LogCaptureFixture

from src.utils.highscore import HighScoreManager


def test_missing_file_returns_empty(tmp_path: Path) -> None:
    """Edge Case: The file does not exist yet."""
    filepath: Path = tmp_path / "missing.json"
    manager = HighScoreManager(str(filepath))

    assert manager.scores == []


def test_malformed_json_returns_empty(
    tmp_path: Path, caplog: LogCaptureFixture
) -> None:
    """Edge Case: The file contains text that is not valid JSON."""
    filepath: Path = tmp_path / "corrupted.json"
    filepath.write_text("This is not JSON !!!", encoding="utf-8")

    with caplog.at_level(logging.WARNING, logger="pacman"):
        manager = HighScoreManager(str(filepath))

    assert manager.scores == []
    assert "Highscore file is corrupted" in caplog.text


def test_wrong_json_root_returns_empty(
    tmp_path: Path, caplog: LogCaptureFixture
) -> None:
    """
    Edge Case: The JSON is valid, but the root is a dictionary, not a list.
    """
    filepath: Path = tmp_path / "wrong_root.json"
    filepath.write_text('{"name": "Steph", "score": 100}', encoding="utf-8")

    with caplog.at_level(logging.WARNING, logger="pacman"):
        manager = HighScoreManager(str(filepath))

    assert manager.scores == []
    assert "Highscore root is not a list" in caplog.text


def test_silent_filter_ignores_bad_rows(tmp_path: Path) -> None:
    """Edge Case: Silent filtering of missing keys and invalid data types."""
    filepath: Path = tmp_path / "mixed.json"
    bad_data: list[dict[str, Any]] = [
        {"foo": "invalid"},                       # Missing keys
        {"name": "Steph", "score": "text_data"},  # Score is not a number
        {"name": "Valid", "score": 500}           # Only valid row
    ]
    filepath.write_text(json.dumps(bad_data), encoding="utf-8")

    manager = HighScoreManager(str(filepath))

    assert len(manager.scores) == 1
    assert manager.scores[0]["name"] == "Valid"


def test_negative_scores_are_rejected(
    tmp_path: Path, caplog: LogCaptureFixture
) -> None:
    """Edge Case: A negative score inside the file must be rejected."""
    filepath: Path = tmp_path / "negative.json"
    bad_data: list[dict[str, Any]] = [{"name": "Cheater", "score": -500}]
    filepath.write_text(json.dumps(bad_data), encoding="utf-8")

    with caplog.at_level(logging.WARNING, logger="pacman"):
        manager = HighScoreManager(str(filepath))

    assert manager.scores == []
    assert "negative score" in caplog.text


def test_name_sanitization_from_file(
    tmp_path: Path, caplog: LogCaptureFixture
) -> None:
    """
    Edge Case: Illegal characters in names loaded from the file are sanitized.
    """
    filepath: Path = tmp_path / "dirty_names.json"
    dirty_data: list[dict[str, Any]] = [
        {"name": "H@cker_!!!_99", "score": 100},  # Symbols
        {"name": "  ", "score": 200}              # Only spaces
    ]
    filepath.write_text(json.dumps(dirty_data), encoding="utf-8")

    with caplog.at_level(logging.WARNING, logger="pacman"):
        manager = HighScoreManager(str(filepath))

    assert manager.scores[0]["name"] == "Hcker99"
    assert manager.scores[1]["name"] == "Anonymous"
    assert "Highscore sanitized" in caplog.text


def test_add_score_logic(tmp_path: Path) -> None:
    """
    Edge Case: add_score() enforces sorting,
    the 10-score limit, and engine safety.
    """
    filepath: Path = tmp_path / "save_test.json"
    manager = HighScoreManager(str(filepath))

    manager.add_score("B@d N@me!!!", -999)
    assert len(manager.scores) == 1
    assert manager.scores[0]["name"] == "Bd Nme"
    assert manager.scores[0]["score"] == 0  # max(0, -999)

    for i in range(1, 12):
        manager.add_score(f"Player{i}", i * 10)

    assert len(manager.scores) == 10
    assert manager.scores[0]["score"] == 110
    assert manager.scores[-1]["score"] == 20
