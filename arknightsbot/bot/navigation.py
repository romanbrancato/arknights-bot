from time import sleep

from arknightsbot.detection.image_rec import click_image

path = "detection\\reference_images\\"
def get_to_main_menu_after_startup():
    click_image(path + "initial_start_button.png")
    sleep(10)
    click_image(path + "login_start_button.png")

#def return_to_main_menu():
#
# def open_terminal():
#
# def open_main_theme_menu():
#
# def go_to_act(act_number):
#
# def go_to_episode(episode_number):
#
# def go_to_stage(stage_number):
#
# #Checks
#
# def check_if_on_main_menu():
#
# def check_if_correct_stage():