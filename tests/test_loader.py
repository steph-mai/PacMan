from pathlib import Path
from src.parsing.loader import Loader
import pytest


# Pytest fixture to avoid re-instantiating the Loader for each test
@pytest.fixture
def loader() -> Loader:
    return Loader()


def test_unknown_file(tmp_path: Path, loader: Loader) -> None:
    """Test 1: Unknown File - Should clamp to defaults."""
    filepath = tmp_path / "phantom_file.json"
    config = loader.config_file_load(str(filepath))

    assert config.lives == 3
    assert config.seed is not None


def test_txt_extension_and_comments(tmp_path: Path, loader: Loader) -> None:
    """Test 2: .txt Extension + C and Python comments."""
    content = """// This is a C-style comment
    {
        "lives": 7,
        # This is a Python-style comment
        "pacgum": 999
    }
    """
    filepath = tmp_path / "config_test.txt"
    filepath.write_text(content, encoding="utf-8")

    config = loader.config_file_load(str(filepath))
    assert config.lives == 7
    assert config.pacgum == 999


def test_malformed_json(tmp_path: Path, loader: Loader) -> None:
    """
    Test 3: Malformed JSON (trailing comma) - Should fallback to defaults.
    """
    content = """{
        "lives": 5,
    }"""
    filepath = tmp_path / "malformed.json"
    filepath.write_text(content, encoding="utf-8")

    config = loader.config_file_load(str(filepath))
    assert config.lives != 5
    # It should have rejected the file and used defaults


def test_invalid_types(tmp_path: Path, loader: Loader) -> None:
    """
    Test 4: Invalid Types (str instead of int) - Pydantic 'before' validator.
    """
    content = """{
        "lives": "too many",
        "level_max_time": 45.5,
        "highscore_filename": 42
    }"""
    filepath = tmp_path / "wrong_types.json"
    filepath.write_text(content, encoding="utf-8")

    config = loader.config_file_load(str(filepath))
    # It should fallback to defaults for corrupted fields
    assert isinstance(config.lives, int)
    assert isinstance(config.level_max_time, int)
    assert isinstance(config.highscore_filename, str)


def test_out_of_bounds(tmp_path: Path, loader: Loader) -> None:
    """Test 5: Out of bounds values - Pydantic 'after' validator (Clamping)."""
    content = """{
        "lives": -5,
        "pacgum": 999999
    }"""
    filepath = tmp_path / "out_of_bounds.json"
    filepath.write_text(content, encoding="utf-8")

    config = loader.config_file_load(str(filepath))
    assert config.lives >= 0
    assert config.pacgum <= 10000


def test_level_edge_cases(tmp_path: Path, loader: Loader) -> None:
    """
    Test 6: 'level' Field Edge Cases - Filtering non-dicts and invalid types.
    """
    content = """{
        "level": [
            "this is not a dictionary",
            42,
            {"width": 20, "height": "too big"},
            {"width": 5000, "height": 20}
        ]
    }"""
    filepath = tmp_path / "edge_levels.json"
    filepath.write_text(content, encoding="utf-8")

    config = loader.config_file_load(str(filepath))
    assert isinstance(config.level, list)
    assert len(config.level) > 0
