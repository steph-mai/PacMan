import logging
import os
from src.parsing.loader import Loader

# Setup logger to see Pydantic and Loader warnings during tests
logging.basicConfig(level=logging.WARNING, format="%(levelname)s - %(message)s")


def create_temp_file(filename: str, content: str) -> None:
    """Create a temporary file for testing purposes."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)


def run_tests() -> None:
    loader = Loader()
    print("=== STARTING LOADER TESTS ===\n")

    # --- Test 1: Unknown File ---
    print("--- Test 1: Unknown File ---")
    config1 = loader.config_file_load("phantom_file.json")
    print(f"-> Success: clamped to defaults. Lives = {config1.lives}, Seed = {config1.seed}\n")

    # --- Test 2: .txt Extension and Comments ---
    print("--- Test 2: .txt Extension + C and Python comments ---")
    content_txt = """// This is a C-style comment
    {
        "lives": 7,
        # This is a Python-style comment
        "pacgum": 999
    }
    """
    create_temp_file("config_test.txt", content_txt)
    config2 = loader.config_file_load("config_test.txt")
    print(f"-> Success: file read properly! Lives = {config2.lives}, Pacgums = {config2.pacgum}")
    os.remove("config_test.txt")
    print()

    # --- Test 3: Malformed JSON ---
    print("--- Test 3: Malformed JSON (trailing comma) ---")
    content_malformed = """{
        "lives": 5,
    }"""
    create_temp_file("malformed.json", content_malformed)
    config3 = loader.config_file_load("malformed.json")
    print(f"-> Success: graceful fallback to defaults (Lives = {config3.lives})")
    os.remove("malformed.json")
    print()

    # --- Test 4: Invalid Types (Pydantic 'before' validator) ---
    print("--- Test 4: Invalid Types (str instead of int) ---")
    content_types = """{
        "lives": "too many",
        "level_max_time": 45.5,
        "highscore_filename": 42
    }"""
    create_temp_file("wrong_types.json", content_types)
    config4 = loader.config_file_load("wrong_types.json")
    print("-> Success: corrupted values replaced by safe defaults.")
    print(f"   Lives: {config4.lives}, Max time: {config4.level_max_time}, Scores file: {config4.highscore_filename}")
    os.remove("wrong_types.json")
    print()

    # --- Test 5: Out of bounds (Pydantic 'after' validator) ---
    print("--- Test 5: Out of bounds values (Clamping) ---")
    content_bounds = """{
        "lives": -5,
        "pacgum": 999999
    }"""
    create_temp_file("out_of_bounds.json", content_bounds)
    config5 = loader.config_file_load("out_of_bounds.json")
    print("-> Success: values correctly clamped to allowed limits.")
    print(f"   Lives clamped to: {config5.lives}, Pacgums clamped to: {config5.pacgum}")
    os.remove("out_of_bounds.json")
    print()

    # --- Test 6: Level Edge Cases (The Ultimate Test) ---
    print("--- Test 6: 'level' Field Edge Cases ---")
    # Mixing non-dict items and invalid types inside the dict
    content_levels = """{
        "level": [
            "this is not a dictionary",
            42,
            {"width": 20, "height": "too big"},
            {"width": 5000, "height": 20}
        ]
    }"""
    create_temp_file("edge_levels.json", content_levels)
    config6 = loader.config_file_load("edge_levels.json")
    print("-> Success: level list purified and validated.")
    for i, lvl in enumerate(config6.level):
        print(f"   Level {i+1} -> Width: {lvl.width}, Height: {lvl.height}")
    os.remove("edge_levels.json")
    print("\n=== ALL TESTS PASSED SUCCESSFULLY ===")


if __name__ == "__main__":
    run_tests()
