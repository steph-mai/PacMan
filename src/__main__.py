
from .arcade_views.menu import MenuView
import arcade
import sys
import pyglet
pyglet.options['audio'] = ('silent',)


def main() -> None:
    """Main function to run PacMan"""
    try:
        window = arcade.Window(1280, 720,
                               "PacMan",
                               resizable=True)
        menu = MenuView()
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
