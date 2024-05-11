import os
import numpy
import pytesseract
import subprocess
import pyautogui
from time import sleep
from typing import Tuple, Any
from pygame import mixer
from Quartz import CGWindowListCopyWindowInfo, kCGNullWindowID, kCGWindowListOptionOnScreenOnly
from PIL import Image


MUTE_BUTTON_LOCATION = (1285, 750)
EMPTY_LOCATION = (MUTE_BUTTON_LOCATION[0]-200, MUTE_BUTTON_LOCATION[1])
big_ad = "ADVERTISEMENT"
music_ad = "Advertisement"
muted = False

# def get_mute_button_location(muted: bool=muted):
#     path = "spotify_" + ("muted" if muted else "mute") + ".png"
#     return pyautogui.locateCenterOnScreen(path)
# print(get_mute_button_location())

windowName = "Spotify"
windowId = None


def findWindowId() -> bool:
    global windowId, bottom_left
    window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)

    for window in window_list:
        owner_name = window.get('kCGWindowOwnerName')
        if owner_name == "Spotify":
            windowId = window.get('kCGWindowNumber')
            return True

    return False


def takeScreenshot() -> numpy.ndarray:
    if windowId is None:
        if findWindowId() is False:
            return

    imageFileName = 'screenshot.png'

    # -x mutes sound, -l specifies windowId, -R specifies region
    width, height = pyautogui.size()
    os.system(f'screencapture -x -l %s -R 0,{height},{2/3*width},{height} %s' % (windowId, imageFileName))
    img = Image.open(imageFileName)
    img = numpy.array(img)
    os.remove(imageFileName)
    return img


def ocr_on_screenshot(image_path: str) -> str:
    extracted_text = pytesseract.image_to_string(image_path)
    return extracted_text


def beep() -> bool:
    mixer.init()
    mixer.music.load('beep.mp3')
    mixer.music.play()
    return True


def bring_window_to_foreground(window_name: str) -> None:
    script = f'tell application "{window_name}" to activate'
    subprocess.run(['osascript', '-e', script])


def get_frontmost_application() -> Any:
    window_list = CGWindowListCopyWindowInfo(kCGWindowListOptionOnScreenOnly, kCGNullWindowID)
    frontmost_application = None

    for window in window_list:
        is_on_top = window.get('kCGWindowLayer', 0) == 0
        if is_on_top and (frontmost_application := window.get('kCGWindowOwnerName')).lower() not in {"window server"}:
            break

    return frontmost_application


def mute_toggle(pos: Tuple[int, int]) -> None:
    mouse_pos = pyautogui.position()
    original_active_window = get_frontmost_application()

    bring_window_to_foreground("Spotify")
    sleep(0.1)

    pyautogui.leftClick(pos)
    sleep(0.1)
    pyautogui.moveTo(mouse_pos)
    bring_window_to_foreground(original_active_window)


def main() -> None:
    global muted
    while True:
        img = takeScreenshot()
        print("working...", f"currently {'muted' if muted else 'unmuted'}")

        extracted_text = ocr_on_screenshot(img)

        if music_ad in extracted_text and not muted:
            beep()
            mute_toggle(MUTE_BUTTON_LOCATION)
            muted = not muted
            print("Muted")
        elif big_ad in extracted_text:
            mute_toggle(EMPTY_LOCATION)
        elif music_ad not in extracted_text and muted:
            mute_toggle(MUTE_BUTTON_LOCATION)
            muted = not muted
        # sleep(1)


if __name__ == "__main__":
    main()
