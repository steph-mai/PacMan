import json
from pathlib import Path
from src.parsing.models import Config


class Loader:
    def config_file_load(self, file_name: str) -> Config:
        path = Path(file_name)

        if (
            not path.exists() or
            not path.is_file() or
                path.suffix.lower() != ".json"
                ):
            print(f"Warning: Invalid or missing file '{file_name}'. "
                  f"Loading safe defaults.")
            return Config()

        try:
            with open(path, mode="r", encoding="utf-8") as f:
                lines = f.readlines()
        except OSError as e:
            print(f"Warning: Could not read '{file_name}' ({e})."
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
            print(f"Warning: file '{file_name}' is empty."
                  f"Loading safe defaults.")
            return Config()
        try:
            config_dict = json.loads(clean_json_str)
            return Config(**config_dict)

        except json.JSONDecodeError as e:
            print(f"Warning: Malformed JSON at line {e.lineno}, col {e.colno}."
                  f"Loading safe defaults.")
            return Config()

        except Exception as e:
            print(f"Warning: Configuration logic error ({e})."
                  f"Loading safe defaults.")
            return Config()
