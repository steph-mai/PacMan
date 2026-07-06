
from .arcade_views.menu import MenuView
from src.parsing.loader import Loader
import arcade
import sys
import pyglet
pyglet.options['audio'] = ('silent',)


def main() -> None:
    """Main function to run PacMan"""
    try:
        loader = Loader()
        config_file = sys.argv[1] if len(sys.argv) == 2 else "config.json"
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
