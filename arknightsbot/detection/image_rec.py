import os
from time import sleep
import cv2
import numpy as np


from arknightsbot.ldplayer.client import (
    click_on_location,
    capture_screen
)
from arknightsbot.utils.logger import logger


def locate_image_on_screen(reference, tries=0, max_tries=3, delay=3):
    """Returns coordinate to the center of image on screen"""
    # Take screenshot of screen and load the screenshot
    capture_screen()
    screenshot = "detection\\reference_images\\temp\\ss.png"
    screen = cv2.imread(screenshot)

    # Load reference image
    reference_path = "detection\\reference_images\\" + reference
    image = cv2.imread(reference_path)

    # Get dimensions of reference image
    try:
        h, w = image.shape[0], image.shape[1]
    except:
        raise Exception("Image not found in given path.")

    # Matches the reference image to the screenshot
    result = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)

    # """For Debug"""
    # threshold = 0.8
    # loc = np.where(result >= threshold)
    # for pt in zip(*loc[::-1]):
    #     cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)
    #
    # cv2.imshow("Detection Result", screen)
    # cv2.waitKey(3000)
    # """---------"""

    # Use minMaxLoc to find the position of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.90:
        # Get the top-left and bottom-right coordinates of the rectangle
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # Calculate the center point of the rectangle
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)

        return center

    elif tries < max_tries:
        logger.log(os.path.basename(reference) + " not found, retrying after " + str(delay) + " seconds")
        sleep(delay)
        locate_image_on_screen(reference, tries + 1, max_tries, delay + 2)
    else:
        logger.log("Could not find " + os.path.basename(reference) + " after " +
              str(max_tries) + " retries")
        return None


def click_image(image, delay_before=0):
    sleep(delay_before)
    point = locate_image_on_screen(image)
    if point is not None:
        click_on_location(point)
    else:
        click_image(image)
