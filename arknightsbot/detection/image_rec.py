import os
import cv2
import numpy as np
from arknightsbot.ldplayer.client import *


def locate_image_on_screen(reference, tries=0, max_tries=3, delay=3):
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

    cv2.imshow("Detection Result", screen)
    cv2.waitKey(100)
    """---------"""

    # Use minMaxLoc to find the position of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.8:
        # Get the top-left and bottom-right coordinates of the rectangle
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # Calculate the center point of the rectangle
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)

        return center

    elif tries < max_tries:
        print(os.path.basename(reference) + " not found, retrying after " + str(delay) + " seconds")
        sleep(delay)
        capture_screen()
        locate_image_on_screen(reference, tries + 1, max_tries, delay + 2)
    else:
        print("Could not find " + os.path.basename(reference) + " after " +
              str(max_tries) + " tries")
        screen = cv2.imread("detection\\reference_images\\temp\\ss.png")
        cv2.imshow("Detection Failure", screen)
        cv2.waitKey(5000)
        return None


def menu_check(reference):
    screenshot = "detection\\reference_images\\temp\\ss.png"
    screen = cv2.imread(screenshot)

    image = cv2.imread(reference)
    h, w = image.shape[0], image.shape[1]

    result = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val > 0.8:
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)

        return center

    else:
        return None


def click_image(image):
    point = locate_image_on_screen(image)
    if point is not None:
        click_on_location(point)
        # Update "screen" after clicking
        sleep(5)
        capture_screen()
    else:
        click_image(image)
