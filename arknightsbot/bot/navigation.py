from arknightsbot.detection.image_rec import *

path = "detection\\reference_images\\"


def get_to_main_menu_after_startup():
    click_image(path + "initial_start_button.png")
    click_image(path + "login_start_button.png")


def return_to_main_menu():
    click_image(path + "home_button.png")
    click_image(path + "home_tab_button.png")


def open_terminal_from_main_menu():
    click_image(path + "terminal_button.png")


def open_main_theme_menu():
    if check_if_in_terminal_screen():
        click_image(path + "main_theme_button.png")
    elif check_if_on_main_menu():
        open_terminal_from_main_menu()
        click_image(path + "main_theme_button.png")
    # I'm fairly certain there is not a single menu without the home button
    else:
        return_to_main_menu()
        open_main_theme_menu()


def go_to_act(act_number):
    if act_number == 0:
        print("Going to act 0.")
        click_on_location((65, 136))
        sleep(2)
        click_on_location((65, 136))
    elif act_number == 1:
        print("Going to act 1.")
        click_on_location((65, 136))
    elif act_number == 2:
        print("Going to act 2.")
    sleep(2)
    click_on_location((957, 360))


def go_to_episode(episode_number):
    if episode_number in range(0, 3):
        go_to_act(0)
        if episode_number == 2:
            sleep(1)
            click_on_location((982, 663))
        if episode_number == 1:
            print("going to episode 0")
            sleep(1)
            click_on_location((982, 663))
            sleep(1)
            click_on_location((982, 663))

    if episode_number in range(4, 8):
        go_to_act(1)
        if episode_number == 7:
            sleep(1)
            click_on_location((982, 663))
        if episode_number == 6:
            sleep(1)
            click_on_location((982, 663))
            sleep(1)
            click_on_location((982, 663))
        if episode_number == 5:
            sleep(1)
            click_on_location((982, 663))
            sleep(1)
            click_on_location((982, 663))
            sleep(1)
            click_on_location((982, 663))
        if episode_number == 4:
            sleep(1)
            click_on_location((982, 663))
            sleep(1)
            click_on_location((982, 663))
            sleep(1)
            click_on_location((982, 663))
            sleep(1)
            click_on_location((982, 663))

    if episode_number in range(9, 10):
        go_to_act(2)
        if episode_number == 9:
            click_on_location((982, 663))

    for i in range(10):
        scroll("left")


# def go_to_stage(stage_number):
#
# #Checks
#
def check_if_on_main_menu():
    if locate_image_on_screen(path + "terminal_button.png") != 0:
        return True


def check_if_in_terminal_screen():
    if locate_image_on_screen(path + "main_theme_button.png") != 0:
        return True

#
# def check_if_correct_stage():
