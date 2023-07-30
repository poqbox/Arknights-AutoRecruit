import pyautogui


def get_screen_size():
    return pyautogui.size()


def get_failsafe_points():
    return pyautogui.FAILSAFE_POINTS


def get_mouse_position():
    return pyautogui.position()


def move_mouse(x, y):
    pyautogui.moveTo(x, y, _pause=False)


def move_mouse_rel(x_incr, y_incr):
    pyautogui.moveRel(x_incr, y_incr, _pause=False)


def drag_left_click(x, y, duration):
    pyautogui.dragTo(x, y, duration=duration, button="left", _pause=False)


def drag_right_click(x, y, duration):
    pyautogui.dragTo(x, y, duration=duration, button="right", _pause=False)


def drag_middle_click(x, y, duration):
    pyautogui.dragTo(x, y, duration=duration, button="middle", _pause=False)


def left_click(x=None, y=None, duration=0):
    pyautogui.click(x=x, y=y, duration=duration, button="left", _pause=False)


def hold_left_click():
    pyautogui.mouseDown(button=left, _pause=False)


def release_left_click():
    pyautogui.mouseUp(button=left, _pause=False)


def right_click(x=None, y=None, duration=0):
    pyautogui.click(x=x, y=y, duration=duration, button="right", _pause=False)


def middle_click(x=None, y=None, duration=0):
    pyautogui.click(x=x, y=y, duration=duration, button="middle", _pause=False)


def scroll(increment):
    # positive = up
    pyautogui.vscroll(increment, _pause=False)


def horizontal_scroll(increment):
    # positive = right
    pyautogui.hscroll(increment, _pause=False)


def press_key(key):
    # for multiple key presses (in order), pass through a list of strings
    pyautogui.press(key, _pause=False)


def hold_key(key):
    pyautogui.keyDown(key, _pause=False)


def release_key(key):
    pyautogui.keyUp(key, _pause=False)


def write(text, interval_between_key_presses):
    pyautogui.write(text, interval=interval_between_key_presses, _pause=False)
