from arknightsbot.bot.navigation import *
from arknightsbot.utils.stage_string_splitter import split_stage_string
from arknightsbot.utils.material_dictionary import optimal_stage_for_material


def start_stage(refill):
    state = check_for_autodeploy_state()
    if state == "on":
        logger.log("Trying to start stage")
        # Clicks blue start button
        click_on_location((1206, 673), delay_after=1)
        if check_for_insufficient_sanity():
            if refill is True:
                logger.log("Refilling sanity.")
                # Clicks Yes and then starts stage
                click_on_location((1089, 575))
                click_on_location((1206, 673), delay_before=2)
                click_on_location((1105, 525), delay_before=2)
            else:
                logger.log("Not refilling sanity.")
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
        logger.log("Auto deploy locked, cannot farm stage.")
        return_to_main_menu()
        sys.exit()


# If max repeats is None then infinitely farm stage till out of sanity
# leaving stage_string as none allows farming of event stages
def repeat_stage(stage_string=None, max_repeats=None, refill=False):
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

    logger.log(f"Stage repeated {repeats} times, returning to menu")
    return_to_main_menu()


# For farming unlisted stages such as event stages
def repeat_custom_stage(max_repeats=None, refill=False):
    repeats = 0
    while max_repeats is None or repeats < max_repeats:
        if start_stage(refill) is not None:
            break
        check_for_stage_completion()
        # Click center of screen to return to stage screen
        click_on_location((640, 360), delay_after=2)
        repeats += 1

    logger.log(f"Stage repeated {repeats} times, returning to menu")
    return_to_main_menu()


def farm_material(material, number_needed, refill=False):
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
    logger.log(f"Farmed {number} {material}. Returning to main menu")
    return_to_main_menu()


"""Checkers"""


def check_for_autodeploy_state():
    sleep(1)
    states = {"auto_deploy_on.png": "on",
              "auto_deploy_off.png": "off"}
    for image, state in states.items():
        if locate_image_on_screen(image, max_tries=0):
            return state
    return "locked"


def check_for_stage_completion():
    logger.log("Waiting on stage completion...")
    while locate_image_on_screen("exp.png", max_tries=0) is None:
        sleep(20)
    logger.log("Stage completed")
    return True


def check_for_material_drops(material):
    logger.log("Checking for drops...")
    number_of_drops = 0
    if locate_image_on_screen(f"\\materials\\{material}.png") is not None:
        number_of_drops += 1
    return number_of_drops


def check_for_insufficient_sanity():
    if locate_image_on_screen("refill_screen.png", max_tries=0):
        return True
    else:
        return False
