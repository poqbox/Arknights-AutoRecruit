import cv2
import os
import time
import win32gui
import desktop_control as desktop
import screen_capture_tools
import recruitment_database_tools
# import AutoRecruit


arknights_name = "Arknights"
scr = screen_capture_tools.SourceWindow(arknights_name)
scr_w = 1920
scr_h = 1080

# # emulator startup testing
# emulator_path = r"C:\Program Files\Google\Play Games\Bootstrapper.exe"
# emulator_title = "Google Play Games beta"
# emu = screen_capture_tools.SourceWindow(emulator_title)
# AutoRecruit.start_AutoRecruit(emulator_path, emulator_title)
# pt1, pt2 = emu.get_window_position()
# min_search_pt = (350, 230)
# max_search_pt = (590, 260)
# search_w = 240
# emu.draw_rectangle_on_screen((min_search_pt[0] + pt1[0], min_search_pt[1] + pt1[1]), (min_search_pt[0] + search_w + pt1[0], max_search_pt[1] + pt1[1]))

# find_text = "Recruit"
# scr.show_window()
# scr.take_windowed_screenshot(screenshot_name="test")
# scr.take_bounded_screenshot((1395, 645), (1625, 715), screenshot_name="Recruitment Label")
# scr.find_text_in_window(find_text, print_detected_text=False, show_window=True, bound_text=True)
# scr.find_text_in_window(find_text, bound=((85, 325), (180, 385)), print_detected_text=True, show_window=True, bound_text=False)

# # find text in window
# find_text = "START"
# scr.find_text_in_window(find_text, bound=((799, 712), (1106, 814)), print_detected_text=True, show_window=True, bound_text=False)

# # setup path for reading and deskewing images
# directory = "Screenshots"
# image_name = "Recruitment Label.png"
# file_dir = os.path.dirname(__file__)
# file_dir = os.path.dirname(file_dir)
# image_path = os.path.join(file_dir, directory, image_name)
# image = cv2.imread(image_path)
# pts1 = ((0, 0), (0, 55), (230, 70))
# pts2 = ((0, 0), (0, 55), (235, 55))
# scr.skew_image(image, image_pts=pts1, output_pts=pts2, save_image=True, file_name="Recruitment Label [skewed]")

# # take screenshots
# screenshot_name = "Recruitment Setup Screen"
# time.sleep(1)
# img = scr.take_screenshot(save_screenshot=True, screenshot_name=screenshot_name)

# # draw points on image
# scr.find_points_on_image("Recruitment Label.png")
# scr.find_points_in_window("Screenshot 2024-12-10 174302.png")
screen_capture_tools.find_point_on_screen()

# # find text in image
# find_text = "START"
# scr.find_text_in_image(image, find_text, print_detected_text=True, show_image=True, bound_text=False)




# tag_positions_list = [[(563, 540), (778, 608)],
#                       [(813, 540),  (1028, 608)],
#                       [(1063, 540), (1278, 608)],
#                       [(563, 648),  (778, 716)],
#                       [(813, 648),  (1028, 716)]
#                       ]
# recruit_tools = recruitment_database_tools.Database()
# all_tags_list = recruit_tools.tag_dict.values()
# available_tags = []
# time.sleep(2)
# for pt1, pt2 in tag_positions_list:
#     tag_recognized = False
#     # tries to recognize the tag three times before returning and giving an error message
#     for tries in range(3):
#         img = scr.take_bounded_screenshot(pt1, pt2, save_screenshot=False)
#         detected_text, img = scr.detect_text_in_image(img)
#         for tag in all_tags_list:
#             if tag in detected_text:
#                 if tag in available_tags:
#                     print("Warning: recognized duplicate tag.\nContinuing with operation.")
#                 else:
#                     available_tags.append(tag)
#                 tag_recognized = True
#                 break
#         if tag_recognized:
#             break
#         time.sleep(1)
#     if not tag_recognized:
#         print("Error: Failed to recognize tag.")
#         # break
#         # return
# print(available_tags)
