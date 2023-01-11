from time import sleep
import cv2
import numpy as np

from arknightsbot.ldplayer.client import *


def locate_image_on_screen(screenshot, reference):
    screen = cv2.imread(screenshot)

    # Load reference Image
    image = cv2.imread(reference)

    # Read dimensions of reference image
    h, w = image.shape[0], image.shape[1]

    # Matches the reference image to the screenshot
    result = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)

    """Testing purposes"""
    threshold = 0.8
    loc = np.where(result >= threshold)
    for pt in zip(*loc[::-1]):
        cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 2)

    cv2.imshow("result", screen)
    cv2.waitKey(5000)
    cv2.destroyAllWindows()
    """" """

    # Use minMaxLoc to find the position of the best match
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val < 0.8:
        print("Image not confidently (>0.8) found")
        exit()
    else:
        # Get the top-left and bottom-right coordinates of the rectangle
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)

        # Calculate the center point of the rectangle
        center = ((top_left[0] + bottom_right[0]) // 2, (top_left[1] + bottom_right[1]) // 2)

        return center


# Pass image as path
def click_image(image):
    click_on_location(
        locate_image_on_screen("detection\\reference_images\\temp\\ss.png",
                               image))
    # Update "screen" after clicking
    sleep(10)
    capture_screen()
