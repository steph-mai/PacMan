import logging
from src.parsing.loader import Loader

logging.basicConfig(level=logging.WARNING, format="%(levelname)s - %(message)s")


def run_tests() -> None:
    print("Test 1 : valid file (config.json)\n")
    loader = Loader()

    config = loader.config_file_load("config.json")

    print("\n Test 1 : [SUCCESS] keys / values of the configuration file :")
    for key, value in config.model_dump().items():
        print(f" - {key}: {value}")

    print("\n\n")

    print("Test 2 : Unknown File\n")
    config_fallback = loader.config_file_load("unknown_file.json")

    print("\n Unknown file : clamped to default values")
    print(f" -> default lives  : {config_fallback.lives}")
    print(f" -> default seed : {config_fallback.seed}")


if __name__ == "__main__":
    run_tests()
