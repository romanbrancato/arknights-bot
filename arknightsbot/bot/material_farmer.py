from arknightsbot.bot.navigation import *
from arknightsbot.utils.stage_string_splitter import split_stage_string
from arknightsbot.utils.material_dictionary import optimal_stage_for_material


def start_stage(refill):
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
        start_stage(refill)
    else:
        logger.log("Auto deploy locked, cannot farm stage")
        return_to_main_menu()
        sys.exit()


def repeat_stage(stage_string=None, max_repeats=None, refill=False):
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
    while max_repeats is None or repeats < max_repeats:
        if start_stage(refill) is not None:
            break
        check_for_stage_completion()
        # Click center of screen to return to stage screen
        click_on_location((640, 360), delay_after=2)
        repeats += 1

    logger.log(f"Stage repeated {repeats} times")
    return_to_main_menu()


def farm_material(material, number_needed, refill=False):
    """
    Repeats a stage.

            Parameters:
                    material (str): A string containing the full name of the desired material
                    number_needed (int): An int containing the desired number of material
                    refill (bool): True if refilling sanity, False if not refilling sanity
    """
    optimal_stages_list = optimal_stage_for_material(material)
    """REWORK TO ALLOW USER TO CHOOSE WHICH STAGE TO FARM, CURRENTLY JUST USING FIRST CHOICE"""
    prefix, episode, stage_number = split_stage_string(optimal_stages_list[0])
    go_to_stage(prefix, episode, stage_number)
    number = 0
    while number < number_needed:
        if start_stage(refill) is not None:
            break
        check_for_stage_completion()
        number += check_for_material_drops(material)
        # Click center of screen to return to stage screen
        click_on_location((640, 360), delay_after=2)
    logger.log(f"Farmed {number} {material}")
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
