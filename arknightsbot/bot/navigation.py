import sys
from datetime import *
from arknightsbot.detection.image_rec import *
from arknightsbot.ldplayer.client import (
    scroll,
    restart_AK
)
from arknightsbot.utils.logger import logger


def get_to_main_menu_after_startup():
    """Attempts to get to main menu by pressing start and login buttons when it sees them"""
    logger.log("Trying to get to main menu after starting")
    click_image("initial_start_button.png", delay_before=10, max_tries=3)
    click_image("login_start_button.png", delay_before=10, max_tries=3)
    while not check_if_on_main_menu():
        sleep(15)


def return_to_main_menu():
    """Attempts to return main menu by locating the home button. If it cannot, restart."""
    is_on_main_menu = check_if_on_main_menu()
    if not is_on_main_menu:
        is_true, image_location = check_if_able_to_return_to_main_menu()
        if is_true:
            logger.log("Returning to main menu...")
            click_on_location(image_location)
            click_image("home_tab_button.png", delay_before=1)
            is_on_main_menu = True
        else:
            logger.log("Failed to return to main menu")
            restart_AK()
            get_to_main_menu_after_startup()
            is_on_main_menu = True
    return is_on_main_menu


def open_terminal():
    """Attempts to open the terminal by locating the terminal button."""
    logger.log("Trying to open terminal")
    click_image("terminal_button.png")
    # To make sure it can get around variable unstable connection pop-ups
    sleep(2)
    if check_if_in_terminal() is False:
        open_terminal()


def open_main_theme_menu():
    """Attempts to open the main theme menu by locating the main theme button."""
    is_on_main_menu = return_to_main_menu()
    if is_on_main_menu:
        open_terminal()
        click_image("main_theme_button.png", delay_before=1)


def open_supplies_menu():
    """Attempts to open the supply stage menu by locating the supply stage button."""
    is_on_main_menu = return_to_main_menu()
    if is_on_main_menu:
        open_terminal()
        click_image("supplies_button.png", delay_before=1)


def go_to_act(act_number):
    """
    Attempts to navigate to correct act through a specific series of clicks.

            Parameters:
                    act_number (int): A decimal integer
    """
    act_to_clicks = {
        0: [(65, 136), (65, 136)],
        1: [(65, 136)],
        2: []
    }
    open_main_theme_menu()
    clicks = act_to_clicks[act_number]
    logger.log(f"Going to act {act_number}")
    for click in clicks:
        click_on_location(click, delay_before=1)
    click_on_location((957, 360), delay_before=1)


def go_to_supply_stage(stage_prefix):
    """
    Attempts to navigate to correct supply stage category through a specific series of clicks.

              Parameters:
                      stage_prefix (str): A string containing any letters in stage name
    """
    open_supplies_menu()
    for i in range(1):
        scroll("left")

    for _ in range(5):
        sleep(2)
        is_true, image_location = check_menu_for_supply_stage(stage_prefix)
        if is_true:
            click_on_location(image_location)
            return
        scroll("right")
    else:
        logger.log(f"Could not find {stage_prefix} stages")
        return_to_main_menu()


def go_to_episode(episode_number):
    """
    Attempts to navigate to correct episode through a specific series of clicks.

            Parameters:
                    episode_number (int): A decimal integer
    """
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
        logger.log(f"Already in episode {episode_number}")
    else:
        logger.log(f"Going to episode {episode_number}")
    for i in range(clicks):
        click_on_location((982, 663), delay_before=1)

    for i in range(8):
        scroll("left")


def go_to_stage(stage_prefix="", episode_number=0, stage_number=0):
    """
    Attempts to navigate to correct stage.

            Parameters:
                    stage_prefix (str): A string containing any letters in stage name
                    episode_number (int): A decimal integer
                    stage_number (int): A decimal integer
    """
    if episode_number != 0:
        go_to_episode(episode_number)
    elif check_supply_stage_availability(stage_prefix):
        go_to_supply_stage(stage_prefix)
    else:
        return_to_main_menu()
        sys.exit()

    logger.log(f"Checking if stage {stage_prefix}{episode_number}-{stage_number} is on screen ")
    for _ in range(10):
        sleep(2)
        is_true, image_location = check_if_stage_on_screen(stage_prefix, episode_number, stage_number)
        if is_true:
            click_on_location(image_location)
            return
        scroll("right")
    else:
        logger.log(f"Could not find stage {stage_prefix}{episode_number}-{stage_number}")
        return_to_main_menu()


"""Checks"""


def check_if_on_main_menu():
    """
    Checks if the main menu is open by locating the terminal button.

            Returns:
                    bool: True if on main menu, False if not on main menu
    """
    logger.log("Checking if on main menu")
    if locate_image_on_screen("terminal_button.png") is not None:
        logger.log("On main menu")
        return True
    else:
        logger.log("Not on main menu")
        return False


def check_if_able_to_return_to_main_menu():
    """
    Checks if able to navigate back to main menu by locating the home button.

            Returns:
                bool: True if able to return to main menu, False if not able to return to main menu
                image_location: a tuple containing the x and y values of the center of the image (in that order)
                                as integers
    """
    logger.log("Checking if able to return to main menu")
    image_location = locate_image_on_screen("home_button.png")
    if image_location is not None:
        return True, image_location
    else:
        return False, None


def check_if_in_terminal():
    """
    Checks if currently in the terminal by locating the main theme button.

            Returns:
                    bool: True if in terminal, False if not in terminal
    """
    logger.log("Checking if in terminal")
    if locate_image_on_screen("main_theme_button.png") is not None:
        logger.log("In terminal")
        return True
    else:
        logger.log("Not in terminal")
        return False


def check_supply_stage_availability(stage_prefix):
    """
    Checks if a supply stage is available on the current day.

            Parameters:
                    stage_prefix (str): A string containing any letters in stage name

            Returns:
                    bool: True if stage is open today, False if stage is not open today
    """
    logger.log("Checking for supply stage availability")
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
        logger.log(f"{stage_prefix.upper()} stages are open today")
        return True
    else:
        logger.log(f"{stage_prefix.upper()} stages are not open today")
        return False


def check_if_stage_on_screen(stage_prefix, episode_number, stage_number):
    """
    Checks if the stage desired stage is currently on the screen.

            Parameters:
                    stage_prefix (str): A string containing any letters in stage name
                    episode_number (int): A decimal integer
                    stage_number (int): A decimal integer

            Returns:
                    bool: True if correct stage is currently on screen, False if correct stage is not currently on
                          screen
                    image_location: a tuple containing the x and y values of the center of the image (in that order)
                                    as integers
    """
    if episode_number == 0:
        image_path = f"stages\\{stage_prefix}\\{stage_prefix}{episode_number}-{stage_number}.png"
    else:
        image_path = f"stages\\{episode_number}\\{stage_prefix}{episode_number}-{stage_number}.png"

    image_location = locate_image_on_screen(image_path)
    if image_location is not None:
        logger.log(f"Found stage {stage_prefix}{episode_number}-{stage_number}")
        return True, image_location
    else:
        return False, None


def check_menu_for_supply_stage(stage_prefix):
    """
    Checks if the category of supply stages is currently on the screen.

            Parameters:
                    stage_prefix (str): A string containing any letters in stage name

            Returns:
                    bool: True if category of supply stages is currently on the screen,
                          False if category of supply stages is not currently on the screen
    """
    image_location = locate_image_on_screen(f"{stage_prefix}.png")
    if image_location is not None:
        return True, image_location
    else:
        return False, None
