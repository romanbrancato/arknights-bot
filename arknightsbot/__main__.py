from utils.logger import *
from ldplayer.client import *
from detection.image_rec import *
from bot.navigation import *
from bot.material_farmer import *
from utils.stage_string_splitter import *
from utils.material_dictionary import *
from interface import gui

# Bot assumes that LD instance is named "Arknights_Bot" and Arknights is opened
def main():
    gui.start_gui()


if __name__ == "__main__":
    main()
