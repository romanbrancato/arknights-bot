from arknightsbot.bot.navigation import *
from arknightsbot.utils.stage_string_splitter import split_stage_string


def handle_stage_start(refill):
    """
    Attempts to start the stage through a series of clicks.

            Parameters:
                    refill (bool): True if refilling sanity, False if not refilling sanity

            Returns:
                    str: A string which holds the current sanity state
    """
    state = check_for_autodeploy_state()
    if state == "on":
        logger.log("Trying to start stage")
        # Clicks blue start button
        click_on_location((1206, 673), delay_after=1)
        if check_for_insufficient_sanity():
            if refill is True:
                logger.log("Refilling sanity")
                # Clicks Yes and then starts stage
                click_on_location((1089, 575))
                click_on_location((1206, 673), delay_before=2)
                click_on_location((1105, 525), delay_before=2)
            else:
                logger.log("Not refilling sanity")
                # Clicks X
                click_on_location((780, 575))
                return "no sanity"
        else:
            # Clicks mission start button
            click_on_location((1105, 525), delay_before=1)
    elif state == "off":
        logger.log("Turning on auto deploy")
        click_on_location((1066, 605))
        handle_stage_start(refill)
    else:
        logger.log("Auto deploy locked, cannot farm stage")
        return_to_main_menu()
        sys.exit()


def repeat_stage(stage_string=None, max_repeats=None, refill=False, target_material=None, target_needed=0):
    """
    Repeats a stage.

            Parameters:
                    stage_string (str): A string containing the full name of the stage,
                                        A value of None will indicate usage for unlisted stages
                    max_repeats (int): An int containing the desired number of repeats,
                                       A value of None will repeat the stage indefinitely
                    refill (bool): True if refilling sanity, False if not refilling sanity
    """
    if stage_string is not None:
        prefix, episode, stage = split_stage_string(stage_string)
        go_to_stage(prefix, episode, stage)
    repeats = 0
    total_drops = 0
    while max_repeats is None or repeats < max_repeats:
        if handle_stage_start(refill) == "no sanity":
            break
        check_for_stage_completion()
        if target_material is not None:
            total_drops += check_for_material_drops(target_material)
            if target_needed == total_drops:
                click_on_location((640, 360), delay_after=2)
                break
        # Click center of screen to return to stage screen
        click_on_location((640, 360), delay_after=2)
        repeats += 1

    logger.log(f"Stage repeated {repeats} times")
    return_to_main_menu()



"""Checkers"""


def check_for_autodeploy_state():
    """
    Checks the auto deploy state by looking at the autodeploy button.

            Returns:
                    state (str): A string containing the current stage of the auto deploy button
    """
    sleep(1)
    states = {"auto_deploy_on.png": "on",
              "auto_deploy_off.png": "off"}
    for image, state in states.items():
        if locate_image_on_screen(image):
            return state
    return "locked"


def check_for_stage_completion():
    """
    Checks for when the stage is complete by finding the exp drop

            Returns:
                    bool: True if stage is complete
    """
    logger.log("Waiting on stage completion...")
    while locate_image_on_screen("exp.png") is None:
        if locate_image_on_screen("level_up.png") is not None:
            click_on_location((640, 360), delay_after=1)
            break
        sleep(20)
    logger.log("Stage completed")
    return True


def check_for_material_drops(material):
    """
    Checks for drops of desired material on stage completion screen by locating the material image.

            Parameters:
                    material (str): A string containing the name of the material

            Returns:
                    number_of_drops (int): An int containing the number of times it found the material image
    """
    logger.log("Checking for drops")
    number_of_drops = 0
    if locate_image_on_screen(f"\\materials\\{material}.png") is not None:
        number_of_drops = 1
    return number_of_drops


def check_for_insufficient_sanity():
    """
    Checks if the user is out of sanity by locating the refill sanity screen.

            Returns:
                    bool: True if insufficient sanity, False if sufficient sanity
    """
    if locate_image_on_screen("refill_screen.png"):
        return True
    else:
        return False
