from ldplayer.client import *
from detection.image_rec import *
from bot.navigation import get_to_main_menu_after_startup

def main():
    start_ld()
    sleep(20)
    capture_screen()
    get_to_main_menu_after_startup()


if __name__ == "__main__":
    main()
