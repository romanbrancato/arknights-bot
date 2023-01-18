from arknightsbot.bot.material_farmer import repeat_stage
from arknightsbot.bot.navigation import return_to_main_menu
from utils.material_dictionary import *


# Bot assumes that LD instance is named "Arknights_Bot" and Arknights is opened
def main():
    print(optimal_stage_for_material(calculate_material_equivalency("orirock cube", 1)))


if __name__ == "__main__":
    main()
