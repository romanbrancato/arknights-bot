import os
import sys
import cv2
import numpy as np
from arknightsbot.ldplayer.client import *


def locate_image_on_screen(reference):
    """Returns coordinate to the center of image on screen"""
    # Load the latest screenshot
    screenshot = "detection\\reference_images\\temp\\ss.png"
    screen = cv2.imread(screenshot)

    # Load reference image
    image = cv2.imread(reference)

    # Get dimensions of reference image
    h, w = image.shape[0], image.shape[1]

    # Matches the reference image to the screenshot
    result = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)

    """For Debug"""
    threshold = 0.8
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    cv2.imshow("result", screen)
    cv2.waitKey(2500)
    cv2.destroyAllWindows()
    """---------"""

    # Use minMaxLoc to find the position of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # If match with <80% confidence, return 0
    if max_val < 0.8:
        return 0
    else:
        # Get the top-left and bottom-right coordinates of the rectangle
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # Calculate the center point of the rectangle
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)

        return center


# Pass image as path
def click_image(image, tries=0, max_tries=3, delay=3):
    point = locate_image_on_screen(image)
    if point != 0:
        click_on_location(point)
        # Update "screen" after clicking
        sleep(5)
        capture_screen()
    elif tries < max_tries:
        print(os.path.basename(image) + " not found, retrying after " + str(delay) + " seconds")
        sleep(delay)
        capture_screen()
        click_image(image, tries + 1, max_tries, delay + 2)
    else:
        print("Could not find " + os.path.basename(image) + " after " +
              str(max_tries) + " tries, stuck on this screen:")
        screen = cv2.imread("detection\\reference_images\\temp\\ss.png")
        cv2.imshow("Stuck On", screen)
        cv2.waitKey(5000)
        sys.exit()
