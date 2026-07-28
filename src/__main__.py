import sys
import os
import pygame
from src.utils.logger_setup import setup_logger
from src.parsing.loader import Loader
from src.mlx_wrapper.game_manager import GameManager
from src.mlx_wrapper.menu_view import MenuView


def get_config_path(filename: str = "config.json") -> str | None:
    """
    Récupère le chemin absolu du fichier de configuration.
    Gère la compatibilité avec le dossier temporaire (_MEIPASS) de PyInstaller.
    """
    if len(sys.argv) == 2:
        return sys.argv[1]

    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, filename)

    return None


def main() -> None:
    """
    Main entry point for the Pac-Man game.
    Initializes the engine, loads the configuration, and starts the menu.
    """
    try:
        setup_logger()
        loader = Loader()

        config_file = get_config_path("config.json")
        if not config_file:
            print("Usage: python3 pac-man.py <config_file.json>")
            sys.exit(1)
        config = loader.config_file_load(config_file)

        pygame.display.init()
        info = pygame.display.Info()
        manager = GameManager(info.current_w, info.current_h, "PacMan")

        menu_view = MenuView(manager.engine, manager, config)
        manager.set_view(menu_view)

        manager.run()

    except KeyboardInterrupt:
        print("\n[!] Game aborted by user (Ctrl+C). Shutting down...")
        pygame.quit()
        sys.exit(130)
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
        pygame.quit()
        sys.exit(1)


if __name__ == "__main__":
    main()
