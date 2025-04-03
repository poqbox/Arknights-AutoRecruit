import math

import numpy
import pyautogui
from numpy import random

# INFO
def get_screen_size():
    return pyautogui.size()


def get_mouse_position():
    return pyautogui.position()


def get_failsafe_points():
    return pyautogui.FAILSAFE_POINTS


# MOUSE CONTROL
def move_mouse(x: int, y: int, duration=0.0, speed_function=pyautogui.linear):
    pyautogui.moveTo(x, y, duration=duration, tween=speed_function, _pause=False)


def move_mouse_rel(x_incr: int, y_incr: int, duration=0.0, speed_function=pyautogui.linear):
    pyautogui.moveRel(x_incr, y_incr, duration=duration, tween=speed_function, _pause=False)


# MOUSE-BUTTON CLICK
def click(x: int = None, y: int = None, button="left"):
    pyautogui.click(x=x, y=y, button=button, _pause=False)


def left_click(x: int = None, y: int = None):
    pyautogui.click(x=x, y=y, button="left", _pause=False)


def right_click(x: int = None, y: int = None):
    pyautogui.click(x=x, y=y, button="right", _pause=False)


def middle_click(x: int = None, y: int = None):
    pyautogui.click(x=x, y=y, button="middle", _pause=False)


# MOUSE-BUTTON HOLD
def hold_button(button="left"):
    pyautogui.mouseDown(button=button, _pause=False)


def hold_left_click():
    pyautogui.mouseDown(button="left", _pause=False)


def hold_right_click():
    pyautogui.mouseDown(button="right", _pause=False)


def hold_middle_click():
    pyautogui.mouseDown(button="middle", _pause=False)


# MOUSE-BUTTON RELEASE
def release_button(button="left"):
    pyautogui.mouseUp(button=button, _pause=False)


def release_left_click():
    pyautogui.mouseUp(button="left", _pause=False)


def release_right_click():
    pyautogui.mouseUp(button="right", _pause=False)


def release_middle_click():
    pyautogui.mouseUp(button="middle", _pause=False)


# HOLD-DRAG-RELEASE
def drag_click(x: int, y: int, duration=0.0, speed_function=pyautogui.linear, button="left"):
    pyautogui.dragTo(x, y, duration=duration, tween=speed_function, button=button, _pause=False)


def drag_left_click(x: int, y: int, duration=0.0, speed_function=pyautogui.linear):
    pyautogui.dragTo(x, y, duration=duration, tween=speed_function, button="left", _pause=False)


def drag_right_click(x: int, y: int, duration=0.0, speed_function=pyautogui.linear):
    pyautogui.dragTo(x, y, duration=duration, tween=speed_function, button="right", _pause=False)


def drag_middle_click(x: int, y: int, duration=0.0, speed_function=pyautogui.linear):
    pyautogui.dragTo(x, y, duration=duration, tween=speed_function, button="middle", _pause=False)


# SCROLL
def scroll(increment: int):
    # positive = up
    pyautogui.vscroll(increment, _pause=False)


def horizontal_scroll(increment: int):
    # positive = right
    pyautogui.hscroll(increment, _pause=False)


v_scroll = vertical_scroll = scroll
h_scroll = horizontal_scroll


# KEYBOARD CONTROL
def press_key(*keys):
    pyautogui.press(list(keys), _pause=False)


def hold_key(key):
    """NOTE: key does not repeat"""
    pyautogui.keyDown(key, _pause=False)


def release_key(key):
    pyautogui.keyUp(key, _pause=False)


def press_hotkey(*keys):
    pyautogui.hotkey(*keys)


def write(text, interval_between_key_presses=0.0):
    pyautogui.write(text, interval=interval_between_key_presses, _pause=False)


# UTIL
class RandomNumberGenerator:
    def __init__(self):
        self.rng = random.default_rng()

    def __get_mean_and_sd(self, max_value):
        mean = max_value/2
        sd = max_value * 0.3
        return mean, sd

    def xy_normal_distribution_sample(self, bounding_box):
        """
        bounding_box should be a tuple with the top-left and bottom-right points
        bounding_box = (x1, y1), (x2, y2)
        """
        x_mean, x_sd = self.__get_mean_and_sd(bounding_box[1][0] - bounding_box[0][0])
        y_mean, y_sd = self.__get_mean_and_sd(bounding_box[1][1] - bounding_box[0][1])
        x = math.floor(self.rng.normal(x_mean, x_sd))
        y = math.floor(self.rng.normal(y_mean, y_sd))
        while x < 0:
            x = math.floor(self.rng.normal(x_mean, x_sd))
        while y < 0:
            y = math.floor(self.rng.normal(y_mean, y_sd))
        return x + bounding_box[0][0], y + bounding_box[0][1]

    def click_delay_sample(self, delay_range_in_sec=1, num_of_decimals=2):
        mean, sd = self.__get_mean_and_sd(delay_range_in_sec)
        delay = self.rng.normal(mean, sd)
        while delay < 0:
            delay = self.rng.normal(mean, sd)
        return numpy.round(delay, num_of_decimals)
