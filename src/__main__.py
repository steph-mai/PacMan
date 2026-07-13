
from .arcade_views.menu import MenuView
from src.utils.logger_setup import setup_logger
from src.parsing.loader import Loader
import arcade
import sys
import pyglet
pyglet.options['audio'] = ('silent',)


def main() -> None:
    """Main function to run PacMan"""
    try:
        setup_logger()
        loader = Loader()
        if len(sys.argv) != 2:
            print("Usage: python3 pac-man.py <config_file.json>")
            sys.exit(1)
        config_file = sys.argv[1]
        config = loader.config_file_load(config_file)
        window = arcade.Window(1280, 720,
                               "PacMan",
                               resizable=True)
        menu = MenuView(config)
        window.show_view(menu)
        arcade.run()
    except KeyboardInterrupt:
        print("\n[!] Game aborted by user (Ctrl+C). "
              "Shutting down...")
        arcade.exit()
        sys.exit(130)
    except Exception as e:
        print(f"\n[!] An unexpected error occurred: {e}")
        arcade.exit()
        sys.exit(1)


if __name__ == "__main__":
    main()
