
from arknightsbot.detection.image_rec import *
from arknightsbot.ldplayer.client import (
    scroll,
    restart_AK
)


def get_to_main_menu_after_startup():
    print("Trying to get to main menu after starting")
    click_image("initial_start_button.png", delay=10)
    click_image("login_start_button.png", delay=10)
    is_on_main_menu = False
    while not is_on_main_menu:
        sleep(15)
        is_on_main_menu = check_if_on_main_menu()


def return_to_main_menu():
    sleep(3)
    is_on_main_menu = check_if_on_main_menu()
    if not is_on_main_menu:
        if locate_image_on_screen("home_button.png", max_tries=0) is not None:
            print("Attempting to return to main menu")
            click_image("home_button.png")
            click_image("home_tab_button.png", delay=1)
            is_on_main_menu = True
        else:
            print("Failed to return to main menu, restarting Arknights")
            restart_AK()
            get_to_main_menu_after_startup()
            is_on_main_menu = True
    return is_on_main_menu


def open_terminal():
    print("Trying to open terminal")
    click_image("terminal_button.png")


def open_main_theme_menu():
    print("Trying to open main theme menu")
    is_on_main_menu = return_to_main_menu()
    if is_on_main_menu:
        open_terminal()
        click_image("main_theme_button.png", delay=1)


def go_to_act(act_number):
    act_to_clicks = {
        0: [(65, 136), (65, 136)],
        1: [(65, 136)],
        2: []
    }
    open_main_theme_menu()
    clicks = act_to_clicks[act_number]
    print(f"Going to act {act_number}")
    for click in clicks:
        click_on_location(click, delay=1)
    click_on_location((957, 360), delay=1)


def go_to_episode(episode_number):
    episode_to_clicks = {
        1: 2,
        2: 1,
        3: 0,
        4: 4,
        5: 3,
        6: 2,
        7: 1,
        8: 0,
        9: 1,
        10: 0
    }
    clicks = episode_to_clicks[episode_number]
    act = 0 if episode_number in [1, 2, 3] else (1 if episode_number in range(4, 9) else 2)
    go_to_act(act)
    if clicks == 0:
        print(f"Already in episode {episode_number}")
    else:
        print(f"Going to episode {episode_number}")
    for i in range(clicks):
        click_on_location((982, 663), delay=1)

    print("Scrolling to beginning of episode")
    for i in range(8):
        scroll("left")

"""STILL HAVE TO ACCOUNT FOR ROTATIONAL STAGES IE. CE-6"""
def go_to_stage(stage_prefix="", episode_number=0, stage_number=0):
    go_to_episode(episode_number)

    while check_if_stage_on_screen(stage_prefix, episode_number, stage_number) is not True:
        scroll("right")
        sleep(2)

    image_path = f"stages\\{episode_number}\\{stage_prefix}{episode_number}-{stage_number}.png"
    click_image(image_path, delay=2)


"""Checks"""


def check_if_on_main_menu():
    print("Checking if on main menu")
    if locate_image_on_screen("terminal_button.png", max_tries=0) is not None:
        print("ON main menu")
        return True
    else:
        print("NOT on main menu")
        return False


def check_if_stage_on_screen(stage_prefix, episode_number, stage_number):
    image_path = f"stages\\{episode_number}\\{stage_prefix}{episode_number}-{stage_number}.png"
    if locate_image_on_screen(image_path, max_tries=0) is not None:
        print(f"Found stage {stage_prefix}{episode_number}-{stage_number}")
        return True
    else:
        return False
