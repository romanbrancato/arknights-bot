from arknightsbot.utils.logger import *
from ldplayer.client import *
from detection.image_rec import *
from bot.navigation import *
from bot.material_farmer import *
from utils.stage_string_splitter import *
from utils.material_dictionary import *


# Bot assumes that LD instance is named "Arknights_Bot"
def main():
    farm_material("orirock_cube", number_needed=3)


if __name__ == "__main__":
    main()
