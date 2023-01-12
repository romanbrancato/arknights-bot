from arknightsbot.detection.image_rec import *

path = "detection\\reference_images\\"


def get_to_main_menu_after_startup():
    print("Trying to get to main menu after starting")
    click_image(path + "initial_start_button.png")
    click_image(path + "login_start_button.png")


def return_to_main_menu():
    print("Trying to get to return to main menu")
    click_image(path + "home_button.png")
    click_image(path + "home_tab_button.png")

    if check_if_on_main_menu() is not True:
        print("Failed to return to main menu, trying again")
        return_to_main_menu()


def open_terminal():
    print("Trying to open terminal")
    click_image(path + "terminal_button.png")


def open_main_theme_menu():
    print("Trying to open main theme menu")
    if check_if_on_main_menu():
        open_terminal()
        click_image(path + "main_theme_button.png")
    # I'm fairly certain there is not a single menu without the home button
    else:
        return_to_main_menu()
        open_main_theme_menu()


def go_to_act(act_number):
    open_main_theme_menu()
    if act_number == 0:
        print("Going to act 0")
        click_on_location((65, 136))
        click_on_location((65, 136), 1)
    elif act_number == 1:
        print("Going to act 1")
        click_on_location((65, 136))
    elif act_number == 2:
        print("Going to act 2")
    sleep(2)
    click_on_location((957, 360))


def go_to_episode(episode_number):
    clicks = 0
    if episode_number in range(0, 4):
        go_to_act(0)
        if episode_number == 3:
            print("Already in episode 3")
        if episode_number == 2:
            print("Going to episode 2")
            clicks = 1
        if episode_number == 1:
            print("Going to episode 1")
            clicks = 2
        if episode_number == 0:
            print("Going to episode 0")
            clicks = 3

    if episode_number in range(4, 9):
        go_to_act(1)
        if episode_number == 8:
            print("Already in episode 8")
        if episode_number == 7:
            print("Going to episode 7")
            clicks = 1
        if episode_number == 6:
            print("Going to episode 6")
            clicks = 2
        if episode_number == 5:
            print("Going to episode 5")
            clicks = 3
        if episode_number == 4:
            print("Going to episode 4")
            clicks = 4

    if episode_number in range(9, 11):
        go_to_act(2)
        if episode_number == 9:
            clicks = 1

    for click in range(clicks):
        click_on_location((982, 663), 1)

    print("Scrolling to beginning of episode")
    for i in range(10):
        scroll("left")


# def go_to_stage(stage_number):

# #Checks
#
def check_if_on_main_menu():
    print("Checking if on main menu")
    if menu_check(path + "terminal_button.png") is not None:
        print("Is on main menu")
        return True
    else:
        print("Is not on main menu")
