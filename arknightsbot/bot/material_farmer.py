from arknightsbot.detection.image_rec import *
from arknightsbot.bot.navigation import *


def start_stage():
    sleep(1)
    state = check_for_autodeploy_state()
    if state == "on":
        print("Trying to start stage")
        # Clicks blue start button
        click_on_location((1206, 673), 2)
        # Clicks mission start button
        click_on_location((1105, 525), 2)
    elif state == "off":
        print("Turning on auto deploy")
        click_on_location((1066, 605))
        start_stage()
    elif state == "locked":
        print("Auto deploy locked, cannot farm stage. Returning to main menu")
        return_to_main_menu()


def wait_for_stage_completion():
    while locate_image_on_screen("exp.png", max_tries=0) is None:
        print("Waiting on stage completion")
        sleep(20)
    print("Stage completed")
    click_on_location((1206, 673))
    sleep(5)


def refill_sanity(setting, refill_times):
    if setting == 0:
        print("Not refilling sanity")
    if setting == 1:
        print("Refilling sanity with potions")
    if setting == 2:
        print("Refilling sanity with Originite Prime")
    if setting == 3:
        print("Refilling sanity with all resources")


def farm_stage(stage_prefix="", episode_number=-1, stage_number=-1, max_repeats=0, refill=0):
    go_to_stage(stage_prefix, episode_number, stage_number)
    repeats = 0
    while repeats < max_repeats:
        start_stage()
        wait_for_stage_completion()
        repeats += 1

    print(f"Stage farmed {repeats} times, returning to menu")
    return_to_main_menu()


"""Checkers"""


def check_for_autodeploy_state():
    if locate_image_on_screen("auto_deploy_on.png", max_tries=0):
        return "on"
    elif locate_image_on_screen("auto_deploy_locked.png", max_tries=0):
        return "locked"
    elif locate_image_on_screen("auto_deploy_off.png", max_tries=0):
        return "off"
