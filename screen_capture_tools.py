import numpy as np
import cv2
import os
import pytesseract
import time
import pyautogui
import win32con
import win32gui


# Uses pytesseract to recognize text in images
# Uses pyautogui to take screenshots
# Uses win32gui (from pywin32) to get window details
screen_cap_name = "Screen Capture"


def get_window_titles():
    """Returns a list of visible window titles"""
    def callback(win_handle, win_titles_list):
        if win32gui.IsWindowVisible(win_handle):
            window_title = win32gui.GetWindowText(win_handle)
            win_titles_list.append(window_title)
    win_titles_list = []
    win32gui.EnumWindows(callback, win_titles_list)
    return win_titles_list


def get_window_position(window_name):
    """Returns the top-left and bottom-right points of the window"""
    window_handle = win32gui.FindWindow(None, window_name)
    x1, y1, x2, y2 = win32gui.GetWindowRect(window_handle)
    return (x1, y1), (x2, y2)


def get_window_size(window_name):
    """Returns the width and height of the window"""
    window_handle = win32gui.FindWindow(None, window_name)
    x1, y1, x2, y2 = win32gui.GetWindowRect(window_handle)
    return x2 - x1, y2 - y1


def show_screen():
    """
    Show the screen in a feed\n
    Enter a keyboard input to exit the feed and the program
    """
    cv2.namedWindow(screen_cap_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(screen_cap_name, 0, 0)
    while True:
        image = pyautogui.screenshot()
        image = np.asarray(image)
        cv2.imshow(screen_cap_name, image)
        cv2.waitKey(1)


def detect_text(bound=None, bound_text=False, color_to_gray=False):
    img = pyautogui.screenshot()
    if bound is not None:
        img = img.crop((bound[0][0], bound[0][1], bound[1][0], bound[1][1]))
    detected_text, img = detect_text_in_image(img, bound_text, color_to_gray)
    return detected_text


def detect_text_in_image(image, bound_text=False, color_to_gray=False):
    """Returns the detected text and the image in a tuple"""
    # convert image to numpy array
    img = np.asarray(image)[:, :, ::-1]
    if color_to_gray:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    if not bound_text:
        return pytesseract.image_to_string(img), image
    else:
        # perform OTSU threshold
        ret, thresh1 = cv2.threshold(img, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
        # specify structure shape and kernel size
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
        # apply dilation
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        # find contours
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        # extract text in identified contours
        detected_text = ""
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            img_cropped = img[y:(y+h), x:(x+w)]
            detected_text += pytesseract.image_to_string(img_cropped)
        return detected_text, image


def find_text(text, bound=None, print_detected_text=False, show_window=True, bound_text=False, quick=False):
    """When quick==True, runs once and returns"""
    while True:
        was_text_found = False
        img = pyautogui.screenshot()
        if bound is not None:
            img = img.crop((bound[0][0], bound[0][1], bound[1][0], bound[1][1]))
        img = np.asarray(img)
        detected_text, img = detect_text_in_image(img, bound_text)
        if quick:
            return text in detected_text
        if show_window:
            cv2.namedWindow("OCR", cv2.WINDOW_NORMAL)
            cv2.imshow("OCR", img)
            cv2.waitKey(1)
        if print_detected_text:
            print("Detected Text:")
            print("  " + detected_text)
        text_found = text in detected_text
        if text_found:
            was_text_found = True
            print("--------------------------------")
            print("'" + text + "' detected")
            print("--------------------------------")
        if cv2.waitKey(1) & 0xFF == ord("q"):
            if was_text_found:
                print("--------------------------------")
                print("'" + text + "' was detected")
                print("--------------------------------")
            else:
                print("--------------------------------")
                print("'" + text + "' was not detected")
                print("--------------------------------")
            return text_found


def draw_rectangle_on_screen(pt1, pt2, border_thickness=2):
    """
    Preview the screen with a rectangle from pt1 to pt2\n
    Enter a keyboard input to exit the feed and the program
    """
    cv2.namedWindow(screen_cap_name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(screen_cap_name, 0, 0)
    while True:
        image = pyautogui.screenshot()
        image = np.asarray(image)
        image = cv2.rectangle(image, pt1, pt2, (0, 0, 255), border_thickness)
        cv2.imshow(screen_cap_name, image)
        cv2.waitKey(1)


def find_point_on_screen(quit_key: str="q"):
    """Prints the position of the mouse when the left-mouse-button is clicked"""
    from pynput.mouse import Button
    from pynput.mouse import Listener as MouseListener
    from pynput.keyboard import Key
    from pynput.keyboard import Listener as KeyboardListener

    def on_left_click(x, y, button, pressed):
        if pressed and button == Button.left:
            print(f"{x}, {y}")

    def on_quit_key_press(key):
        # used a try statement in case the pressed key is a special character
        try:
            if key.char == quit_key:
                m_listener.stop()
                return False
        except AttributeError:
            # used a try statement in case: quit_key and pressed_key are alphanumeric, but pressed_key != quit_key
            try:
                if key == getattr(Key, quit_key.lower()):
                    m_listener.stop()
                    return False
            except AttributeError:
                # the quit_key is alphanumeric, but raises an error when used with getattr(Key, *) since
                # 'Key' only has special keys as attributes (i.e., esc, shift, ctrl_l, etc.)
                # Reaching here ultimately means the quit_key was not pressed
                pass

    m_listener = MouseListener(on_click=on_left_click)
    m_listener.start()
    with KeyboardListener(on_press=on_quit_key_press) as k_listener:
        k_listener.join()


def open_image_file(path):
    return cv2.imread(path, 0)


class SourceWindow:
    def __init__(self, window_name="", preview_width=800, preview_height=450, pytesseract_directory=r'C:\Program Files\Tesseract-OCR\tesseract.exe'):
        # pytesseract directory
        pytesseract.pytesseract.tesseract_cmd = pytesseract_directory
        self.preview_width = preview_width
        self.preview_height = preview_height
        self.window_cap_name = "Capture: " + window_name
        self.window_handle = win32gui.FindWindow(None, window_name)
        self.file_dir = os.path.dirname(__file__)
        self.file_dir = os.path.dirname(self.file_dir)

    def get_window_handle(self):
        """Returns the window's handle"""
        return self.window_handle

    def show_window(self, print_position=False):
        """
        Preview the window for taking screenshots of it\n
        Enter a keyboard input to exit the feed and the program\n
        Notes:\n
        Issue: The window cannot be brought to foreground if it is minimized\n
        Fix: un-minimize the window before running\n
        Issue: The program crashes if the capture window is brought in front of the input window\n
        Fix: Try dragging or repositioning the capture window ahead of time
        """
        cv2.namedWindow(self.window_cap_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.window_cap_name, self.preview_width, self.preview_height)
        while True:
            win32gui.SetForegroundWindow(self.window_handle)
            image = pyautogui.screenshot()
            window_pos = self.get_window_position()
            if print_position:
                print(window_pos[0], window_pos[1])
            image = image.crop((window_pos[0][0], window_pos[0][1], window_pos[1][0], window_pos[1][1]))
            image = np.asarray(image)
            cv2.imshow(self.window_cap_name, image)
            cv2.waitKey(1)

    def get_window_position(self):
        """Returns the top-left and bottom-right points of the window"""
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.window_handle)
        return (x1, y1), (x2, y2)

    def get_window_size(self):
        """Returns the width and height of the window"""
        x1, y1, x2, y2 = win32gui.GetWindowRect(self.window_handle)
        return x2 - x1, y2 - y1

    def save_image(self, image, directory="Screenshots", file_name="image", file_type=".png"):
        # setup path
        path_base = os.path.join(self.file_dir, directory, file_name)
        # Account for saving images with a pre-existing file name
        path = path_base + file_type
        if not os.path.exists(path):
            image.save(path)
            return
        # append for duplicates
        for i in range(1, 100):
            path = path_base + "_(" + str(i) + ").png"
            if not os.path.exists(path):
                image.save(path)
                return
        print("Too many screenshots of the same name")
        print("Please delete some")

    def take_windowed_screenshot(self, save_screenshot=True, screenshot_dir="Screenshots", screenshot_name="screenshot"):
        """Takes a screenshot of the window"""
        win32gui.SetForegroundWindow(self.window_handle)
        img = pyautogui.screenshot()
        pt1, pt2 = self.get_window_position()
        img = img.crop((pt1[0], pt1[1], pt2[0], pt2[1]))
        if save_screenshot:
            self.save_image(img, screenshot_dir, screenshot_name, file_type=".png")
        return img

    def take_bounded_screenshot(self, pt1, pt2, save_screenshot=True, screenshot_dir="Screenshots", screenshot_name="screenshot"):
        """Takes a screenshot of the bounded area"""
        # pt1 is top-left
        # pt2 is bottom-right
        img = pyautogui.screenshot()
        img = img.crop((pt1[0], pt1[1], pt2[0], pt2[1]))
        if save_screenshot:
            self.save_image(img, screenshot_dir, screenshot_name, file_type=".png")
        return img

    def take_screenshot(self, save_screenshot=True, screenshot_dir="Screenshots", screenshot_name="screenshot"):
        """Takes a screenshot of the entire screen"""
        img = pyautogui.screenshot()
        if save_screenshot:
            self.save_image(img, screenshot_dir, screenshot_name, file_type=".png")
        return img

    def skew_image(self, image, image_pts, output_pts, save_image=False, folder_dir="Screenshots", file_name="deskewed", file_type=".png"):
        """
        image_pts are three corner points\n
        output_pts are the desired position after the transformation
        """
        img = np.asarray(image)
        rows, cols, ch = img.shape
        pts1 = np.float32(image_pts)
        pts2 = np.float32(output_pts)
        # apply affine transformation
        warp_mat = cv2.getAffineTransform(pts1, pts2)
        img_skewed = cv2.warpAffine(img, warp_mat, (cols, rows))
        if save_image:
            path = os.path.join(self.file_dir, folder_dir, file_name) + file_type
            cv2.imwrite(path, img_skewed)
        return img_skewed

    def find_text_in_window(self, find_text, bound=None, print_detected_text=False, show_window=True, bound_text=False, quick=False):
        """When quick==True, runs once and returns"""
        while True:
            was_text_found = False
            # get image of the window
            img = pyautogui.screenshot()
            pt1, pt2 = self.get_window_position()
            img = img.crop((pt1[0], pt1[1], pt2[0], pt2[1]))
            if bound is not None:
                img = img.crop((bound[0][0], bound[0][1], bound[1][0], bound[1][1]))
            img = np.asarray(img)
            detected_text, img = detect_text_in_image(img, bound_text)
            if quick:
                return find_text in detected_text
            if show_window:
                cv2.namedWindow(self.window_cap_name, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(self.window_cap_name, self.preview_width, self.preview_height)
                cv2.imshow(self.window_cap_name, img)
                cv2.waitKey(1)
            if print_detected_text:
                print("Detected Text:")
                print("  " + detected_text)
            text_found = find_text in detected_text
            if text_found:
                was_text_found = True
                print("--------------------------------")
                print("'" + find_text + "' detected")
                print("--------------------------------")
            if cv2.waitKey(1) & 0xFF == ord("q"):
                if was_text_found:
                    print("--------------------------------")
                    print("'" + find_text + "' was detected")
                    print("--------------------------------")
                else:
                    print("--------------------------------")
                    print("'" + find_text + "' was not detected")
                    print("--------------------------------")
                return text_found

    def find_text_in_image(self, image, find_text, print_detected_text=False, show_image=False, bound_text=False):
        """Enter a keyboard input to exit the feed and the program"""
        detected_text, img = detect_text_in_image(image, bound_text)
        if print_detected_text:
            print("Detected Text:")
            print("  " + detected_text)
            print("--------------------------------")
            print("--------------------------------")
        text_found = find_text in detected_text
        if text_found:
            print("'" + find_text + "' was detected")
        else:
            print("'" + find_text + "' was not detected")
        if show_image:
            cv2.namedWindow(self.window_cap_name, cv2.WINDOW_NORMAL)
            cv2.resizeWindow(self.window_cap_name, self.preview_width, self.preview_height)
            cv2.imshow(self.window_cap_name, img)
            cv2.waitKey(0)
        return text_found

    def draw_rectangle_on_window(self, pt1, pt2, border_thickness=1):
        """
        Preview the window with a rectangle from pt1 to pt2\n
        Enter a keyboard input to exit the feed and the program
        """
        window_handle = self.window_handle
        win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(window_handle)
        time.sleep(0.1)   # wait for window to be in foreground
        img = pyautogui.screenshot()
        img = img.crop((win32gui.GetWindowRect(window_handle)))
        img = np.ascontiguousarray(np.array(img)[:, :, ::-1])
        img = cv2.rectangle(img, pt1, pt2, (0, 0, 255), border_thickness)
        # move cv2 image to foreground
        cv2.imshow(self.window_cap_name, img)
        cv2.moveWindow(self.window_cap_name, 0, 80)
        time.sleep(0.2)
        win32gui.ShowWindow(window_handle, win32con.SW_MINIMIZE)
        cv2.waitKey(0)

    def find_points_in_window(self, window_name=None, quit_key="q", reset_key="r"):
        """
        Shows an image of the given window and returns three mouse click positions\n
        (0, 0) is the image's top-left pixel\n
        """
        def mouse_click_event(event, x, y, flags, params):
            if event == cv2.EVENT_LBUTTONDOWN:
                if len(pts_list) >= max_pts:
                    pts_list.clear()
                cv2.circle(img, (x, y), 1, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x, y), 10, (0, 0, 255), 2)
                pts_list.append([x, y])
                if len(pts_list) == max_pts:
                    print(pts_list)

        # take a screenshot of the window
        if window_name is None:
            window_handle = self.window_handle
        else:
            window_handle = win32gui.FindWindow(None, window_name)
        win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(window_handle)
        time.sleep(0.1)   # wait for window to be in foreground
        img_orig = pyautogui.screenshot()
        img_orig = img_orig.crop((win32gui.GetWindowRect(window_handle)))
        img_orig = np.array(img_orig)[:, :, ::-1]
        img = np.copy(img_orig)
        # move cv2 image to foreground
        cv2.imshow("OpenCV - imshow", img)
        cv2.moveWindow("OpenCV - imshow", 0, 80)
        time.sleep(0.2)
        win32gui.ShowWindow(window_handle, win32con.SW_MINIMIZE)

        pts_list = []
        max_pts = 3
        while True:
            cv2.imshow("OpenCV - imshow", img)
            cv2.setMouseCallback("OpenCV - imshow", mouse_click_event)
            # reset image and points list
            if cv2.waitKey(1) & 0xFF == ord(reset_key):
                img = np.copy(img_orig)
                pts_list.clear()
            # exit program with the quit_key
            if cv2.waitKey(1) & 0xFF == ord(quit_key):
                break

    def find_points_on_image(self, image_name=None, directory="Screenshots", quit_key="q", reset_key="r"):
        """
        Shows an image and returns three mouse click positions\n
        (0, 0) is the image's top-left pixel
        """
        def mouse_click_event(event, x, y, flags, params):
            if event == cv2.EVENT_LBUTTONDOWN:
                if len(pts_list) >= max_pts:
                    pts_list.clear()
                cv2.circle(img, (x, y), 1, (0, 0, 255), cv2.FILLED)
                cv2.circle(img, (x, y), 10, (0, 0, 255), 2)
                pts_list.append([x, y])
                if len(pts_list) == max_pts:
                    print(pts_list)

        image_path = os.path.join(self.file_dir, directory, image_name)
        img = cv2.imread(image_path)

        pts_list = []
        max_pts = 3
        while True:
            cv2.imshow("OpenCV - imshow", img)
            cv2.setMouseCallback("OpenCV - imshow", mouse_click_event)
            # reset image and points list
            if cv2.waitKey(1) & 0xFF == ord(reset_key):
                img = cv2.imread(image_path)
                pts_list.clear()
            # exit program with the quit_key
            if cv2.waitKey(1) & 0xFF == ord(quit_key):
                break
