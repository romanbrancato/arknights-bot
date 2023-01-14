from datetime import *

from arknightsbot.detection.image_rec import *
from arknightsbot.ldplayer.client import (
    scroll,
    restart_AK
)


def get_to_main_menu_after_startup():
    print("Trying to get to main menu after starting")
    click_image("initial_start_button.png", delay_before=10)
    click_image("login_start_button.png", delay_before=10)
    while not check_if_on_main_menu():
        sleep(15)


def return_to_main_menu():
    sleep(3)
    is_on_main_menu = check_if_on_main_menu()
    if not is_on_main_menu:
        if locate_image_on_screen("home_button.png", max_tries=0) is not None:
            print("Attempting to return to main menu")
            click_image("home_button.png")
            click_image("home_tab_button.png", delay_before=1)
            is_on_main_menu = True
        else:
            print("Failed to return to main menu, restarting Arknights")
            restart_AK()
            get_to_main_menu_after_startup()
            is_on_main_menu = True
    return is_on_main_menu


def open_terminal():
    print("Trying to open terminal")
    click_image("terminal_button.png", delay_before=1)


def open_main_theme_menu():
    is_on_main_menu = return_to_main_menu()
    if is_on_main_menu:
        print("Trying to open main theme menu")
        open_terminal()
        click_image("main_theme_button.png", delay_before=1)


def open_supplies_menu():
    is_on_main_menu = return_to_main_menu()
    if is_on_main_menu:
        print("Trying to open supplies menu")
        open_terminal()
        click_image("supplies_button.png", delay_before=1)


def go_to_supply_stage(stage_prefix):
    open_supplies_menu()
    click_image(f"{stage_prefix}.png", delay_before=1)


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
        click_on_location(click, delay_before=1)
    click_on_location((957, 360), delay_before=1)


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
        click_on_location((982, 663), delay_before=1)

    print("Scrolling to beginning of episode")
    for i in range(8):
        scroll("left")


def go_to_stage(stage_prefix="", episode_number=0, stage_number=0):
    if episode_number != 0:
        go_to_episode(episode_number)
    elif check_supply_stage_availability(stage_prefix):
        go_to_supply_stage(stage_prefix)

    for _ in range(10):
        if check_if_stage_on_screen(stage_prefix, episode_number, stage_number):
            break
        scroll("right")
        sleep(2)
    else:
        raise Exception(f"Could not find stage {stage_prefix}{episode_number}-{stage_number}")

    if episode_number != 0:
        image_path = f"stages\\{episode_number}\\{stage_prefix}{episode_number}-{stage_number}.png"
    else:
        image_path = f"stages\\{stage_prefix}\\{stage_prefix}{episode_number}-{stage_number}.png"

    click_image(image_path)


"""Checks"""


def check_if_on_main_menu():
    print("Checking if on main menu")
    if locate_image_on_screen("terminal_button.png", max_tries=0) is not None:
        print("ON main menu")
        return True
    else:
        print("NOT on main menu")
        return False


def check_supply_stage_availability(stage_prefix):
    print("Checking for supply stage availability")
    current_weekday = datetime.today().strftime("%A")
    availability = {
        "ls": {"Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"},
        "ap": {"Monday", "Thursday", "Saturday", "Sunday"},
        "ce": {"Tuesday", "Thursday", "Saturday", "Sunday"},
        "ca": {"Tuesday", "Wednesday", "Friday", "Sunday"},
        "sk": {"Monday", "Wednesday", "Friday", "Saturday"},
        "pra": {"Monday", "Thursday", "Friday", "Sunday"},
        "prb": {"Monday", "Tuesday", "Friday", "Saturday"},
        "prc": {"Wednesday", "Thursday", "Saturday", "Sunday"},
        "prd": {"Tuesday", "Wednesday", "Saturday", "Sunday"}
    }
    if current_weekday in availability[stage_prefix]:
        print(f"{stage_prefix.upper()} stages are open today")
        return True
    else:
        print(f"{stage_prefix.upper()} stages are not open today")
        return False


def check_if_stage_on_screen(stage_prefix, episode_number, stage_number):
    if episode_number != 0:
        image_path = f"stages\\{episode_number}\\{stage_prefix}{episode_number}-{stage_number}.png"
    else:
        image_path = f"stages\\{stage_prefix}\\{stage_prefix}{episode_number}-{stage_number}.png"
    if locate_image_on_screen(image_path, max_tries=0) is not None:
        print(f"Found stage {stage_prefix}{episode_number}-{stage_number}")
        return True
    else:
        return False
