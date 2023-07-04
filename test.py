import cv2
import os
import win32gui
import DesktopControl as desktop
import ScreenCaptureTools


window_name = "Arknights"
find_text = "START"
scr = ScreenCaptureTools.Tools(window_name)
scr_w = 1920
scr_h = 1080

# scr.show_window()
# scr.take_windowed_screenshot(screenshot_name="test")
# scr.take_bounded_screenshot((1395, 645), (1625, 715), screenshot_name="Recruitment Label")
# scr.find_points_on_image("Recruitment Label.png")
# scr.find_text_in_window(find_text, print_detected_text=False, show_window=True, bound_text=True)
# scr.find_text_in_window(find_text, bound=((85, 325), (180, 385)), print_detected_text=True, show_window=True, bound_text=False)

# # path setup
# directory = "Screenshots"
# image_name = "Recruitment Label.png"
# file_dir = os.path.dirname(__file__)
# file_dir = os.path.dirname(file_dir)
# image_path = os.path.join(file_dir, directory, image_name)
# # deskew image
# image = cv2.imread(image_path)
# pts1 = ((0, 0), (0, 55), (230, 70))
# pts2 = ((0, 0), (0, 55), (235, 55))
# scr.skew_image(image, image_pts=pts1, output_pts=pts2, save_image=True, file_name="Recruitment Label [skewed]")

# directory = "Screenshots"
# image_name = "Recruitment Label [skewed].png"
# file_dir = os.path.dirname(__file__)
# file_dir = os.path.dirname(file_dir)
# image_path = os.path.join(file_dir, directory, image_name)
# image = cv2.imread(image_path)
# scr.find_text_in_image(image, find_text, print_detected_text=True, show_image=True, bound_text=False)

# # find interactable points
# win32gui.SetForegroundWindow(scr.window_handle)
# pt1, pt2 = scr.get_window_position()
# desktop.move_mouse(pt2[0] - 370, pt1[1] + 300)

# # Arknights stuff
# print(scr.get_window_position())
# scr.find_points_on_image()
# scr.find_text_in_window(find_text, bound=((799, 712), (1106, 814)), print_detected_text=True, show_window=True, bound_text=False)
