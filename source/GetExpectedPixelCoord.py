import cv2 as cv
from WindowCapture import WindowCapture
import keyboard
from PIL import Image
import itertools
import os.path

def make_screenshot(filename_all_img, filename_needle_img):
    full_img = cv.imread(filename_all_img, cv.IMREAD_UNCHANGED)
    needPart_img = cv.imread(filename_needle_img, cv.IMREAD_UNCHANGED)

    result_img = cv.matchTemplate(full_img, needPart_img, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result_img)

    # print("Best match top left position: %s" % str(max_loc))
    # print("Best match confidence: %s" % max_val)
    m1 = max_loc[0]
    m2 = max_loc[1]
    return m1, m2, max_val

def CheckCoordColor(NameHnwd):
    wincap = WindowCapture(NameHnwd)
    m = make_screenshot(os.path.abspath(os.curdir)[:-6] + 'data/end.jpg', os.path.abspath(os.curdir)[:-6] + 'data/logo.jpg')
    while True: 
        if keyboard.is_pressed('`'): break
        screen = wincap.get_screenshot()
        fr = Image.fromarray(screen)
        fr.save(os.path.abspath(os.curdir)[:-6] + 'data/end.jpg')
        BColor = fr.getpixel((651, 1014))
        print(" - ", BColor)            


