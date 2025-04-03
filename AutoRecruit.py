from win32api import GetSystemMetrics
import cv2
import os
import subprocess
import time
import win32gui
from pynput.keyboard import Key, Listener
import desktop_control as desktop
import screen_capture_tools
import recruitment_database_tools as recruit_tools

# tested on Windows 11
# pytesseract manual:  https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc
# Notable sections:
#   --psm N
# binding events in tkinter info: https://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-widget
# does not account for:
#   not enough recruitment tickets
#   not enough expedited plans

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# Special recruitment rules:
#   - all 6-stars share the [Top Operator] tag (last checked: Il Siracusano event)
#   - all 5-stars share the [Senior Operator] tag (last checked: Il Siracusano event)
#   - all 2-stars share the [Starter] tag (last checked: Il Siracusano event)
#   - all 1-stars share the [Robot] tag (last checked: Il Siracusano event)
#   - 1-stars can be obtained without a [Robot] tag
#   - 6-stars can only be obtained with a [Top Operator] tag

auto_recruit_window_name = "Auto Recruit"
screen_res = (GetSystemMetrics(0), GetSystemMetrics(1))
scr_mdpt = (int(screen_res[0] / 2), int(screen_res[1] / 2))


def launch_from_GooglePlayGames(emulator_path, emulator_title):
    # open emulator and bring to foreground
    subprocess.run(emulator_path)
    emu_hdl = win32gui.FindWindow(None, emulator_title)
    time.sleep(1)
    try:
        win32gui.SetForegroundWindow(emu_hdl)
    except:
        time.sleep(10)
        subprocess.run(emulator_path)
        emu_hdl = win32gui.FindWindow(None, emulator_title)
        time.sleep(1)
        win32gui.SetForegroundWindow(emu_hdl)
    # 'win32gui.SetForegroundWindow(emu_hdl)' causes the following error if it runs too soon
    #   pywintypes.error: (1400, 'SetForegroundWindow', 'Invalid window handle.')
    # win32gui.SetFocus(emu_hdl)  # cannot bring to focus, window must be attached to the calling thread's message queue
    emu = screen_capture_tools.SourceWindow(emulator_title)
    pt1, pt2 = emu.get_window_position()

    # find and go to "Library" tab
    # sets a search bound and searches top-to-bottom, one row at a time with a search height of search_h
    min_search_pt = (25, 325)
    max_search_pt = (180, 535)
    search_h = 60
    button_size = (60, 60)
    desktop.move_mouse(pt1[0] + min_search_pt[0], pt1[1] + min_search_pt[1])
    for i in range(min_search_pt[1], max_search_pt[1] + 1 - search_h):
        bound = ((min_search_pt[0] + button_size[0], i), (max_search_pt[0], i + search_h))
        if emu.find_text_in_window("Library", bound=bound, bound_text=False, quick=True):
            desktop.left_click(pt1[0] + min_search_pt[0] + button_size[0]/2, pt1[1] + i + button_size[1]/2)
            break
        desktop.move_mouse_rel(0, 1)

    # find and open Arknights
    # y-distance stays the same regardless of window size
    min_search_pt = (350, 230)
    max_search_pt = (590, 260)
    search_w = 240
    desktop.move_mouse(pt1[0] + min_search_pt[0], pt1[1] + min_search_pt[1])
    loading_box_bound = ((scr_mdpt[0] - 500), (scr_mdpt[1] - 300)), ((scr_mdpt[0] + 500), (scr_mdpt[1] + 300))
    for i in range(min_search_pt[0], max_search_pt[0] + 1 - search_w):
        bound = ((i, min_search_pt[1]), (i + search_w, max_search_pt[1]))
        if emu.find_text_in_window("Arknights", bound=bound, bound_text=False, quick=True):
            # find and click the button to open Arknights
            for j in range(300, 381):
                desktop.left_click(pt2[0] - j, pt1[1] + min_search_pt[1] + 40)
                time.sleep(0.1)
                if emu.find_text_in_window("Get ready", bound=loading_box_bound, bound_text=False, quick=True):
                    return True
            break
    return False


def start_AutoRecruit(emulator_path: str, emulator_title: str, recruit_num: int=0, recruit_time: str="00:00", use_expedited_plans=False, prepare_recruitment=False, priority_tags=[], skip_emulator_launch=False, output_box=None):
    """
    Valid starting screens for skip_emulator_launch:\n
    Arknights home screen\n
    Arknights recruitment menu
    """
    launched_Arknights = False
    entered_Arknights_home_page = False
    if skip_emulator_launch:
        launched_Arknights = True
        entered_Arknights_home_page = True
    else:
        launched_Arknights = launch_from_GooglePlayGames(emulator_path, emulator_title)
    if launched_Arknights:
        Arknights = None
        if skip_emulator_launch:
            Arknights = screen_capture_tools.SourceWindow("Arknights")
            ark_hdl = win32gui.FindWindow(None, "Arknights")
            win32gui.SetForegroundWindow(ark_hdl)
            time.sleep(0.5)
        else:
            time.sleep(10)
            Arknights = screen_capture_tools.SourceWindow("Arknights")
            desktop.left_click(scr_mdpt[0], scr_mdpt[1])
            time.sleep(5)
            entered_Arknights_home_page = False
            for i in range(4):
                if Arknights.find_text_in_window("START", bound=((799, 712), (1106, 814)), bound_text=False, quick=True):
                    desktop.left_click(950, 763)
                    time.sleep(5)
                    entered_Arknights_home_page = True
                    break
                desktop.left_click(scr_mdpt[0], scr_mdpt[1])
                time.sleep(5)

        # open recruit menu
        if entered_Arknights_home_page:
            in_recruit_menu = False
            # determine screen location
            if skip_emulator_launch:
                img = Arknights.take_bounded_screenshot((219, 190), (328, 228), save_screenshot=False)
                if Arknights.find_text_in_image(img, "Recruit"):
                    in_recruit_menu = True
            if not in_recruit_menu:
                # take screenshot of recruitment label and deskew it
                img = Arknights.take_bounded_screenshot((1395, 645), (1625, 715), save_screenshot=False)
                img = Arknights.skew_image(img, ((0, 0), (0, 55), (230, 70)), ((0, 0), (0, 55), (235, 55)), save_image=False)
                if Arknights.find_text_in_image(img, "Recruitment"):
                    # click the button to open recruit menu
                    desktop.left_click(1509, 755)
                    in_recruit_menu = True
                    time.sleep(2)
            if in_recruit_menu:
                img = Arknights.take_bounded_screenshot((1248, 37), (1338, 79), save_screenshot=False)
                num_recruit_permits, img = Arknights.detect_text_in_image(img)
                output_box("Starting number of recruitment permits: " + num_recruit_permits)
                tag_positions_list = [[(563, 540), (778, 608)],
                                      [(813, 540), (1028, 608)],
                                      [(1063, 540), (1278, 608)],
                                      [(563, 648), (778, 716)],
                                      [(813, 648), (1028, 716)]
                                      ]
                allTags_dict = recruit_tools.tag_dict
                allTag_valuesList = list(allTags_dict.values())
                allTag_keysList = list(allTags_dict.keys())
                recruitment_db = recruit_tools.Database()
                # begin recruitment loop
                for i in range(recruit_num):
                    # enter recruit setup
                    desktop.left_click(484, 458)
                    time.sleep(0.5)
                    available_tags = []
                    tagToPos_dict = {}
                    # find tags
                    for pt1, pt2 in tag_positions_list:
                        tag_recognized = False
                        # tries to recognize the tag three times before returning and giving an error message
                        for tries in range(3):
                            img = Arknights.take_bounded_screenshot(pt1, pt2, save_screenshot=False)
                            detected_text, img = Arknights.detect_text_in_image(img)
                            for tag in allTag_valuesList:
                                if tag in detected_text:
                                    if tag in available_tags:
                                        output_box("Warning: recognized duplicate tag.\nContinuing with operation.\n")
                                    else:
                                        tag_code = allTag_keysList[allTag_valuesList.index(tag)]
                                        available_tags.append(tag_code)
                                        tagToPos_dict[tag_code] = (pt1, pt2)
                                    tag_recognized = True
                                    break
                            if tag_recognized:
                                break
                            time.sleep(1)
                        if not tag_recognized:
                            output_box("Error: Failed to recognize tag.\n")
                            auto_hdl = win32gui.FindWindow(None, auto_recruit_window_name)
                            win32gui.SetForegroundWindow(auto_hdl)
                            return
                    # determine best tag combination
                    result = recruitment_db.find_best_tags(available_tags, priority_tags)
                    if result == None:
                        # adjust time
                        hours = int(recruit_time[0:2])
                        minutes = int(recruit_time[3:5])
                        for h in range(1, hours):
                            desktop.left_click(678, 224)
                            time.sleep(0.5)
                        for m in range(0, minutes, 10):
                            desktop.left_click(925, 225)
                            time.sleep(0.5)
                    else:
                        best_tags = result[0]
                        rarity = result[1]
                        # click on tags
                        for tag in best_tags:
                            pts = tagToPos_dict[tag]
                            desktop.left_click((pts[0][0] + pts[1][0])/2, (pts[0][1] + pts[1][1])/2)
                            time.sleep(0.5)
                        # adjust recruitment time
                        if rarity == 4 or rarity == 5 or rarity == 6:
                            desktop.left_click(674, 445)
                            time.sleep(0.5)
                    # confirm recruitment
                    time.sleep(0.5)
                    desktop.left_click(1467, 871)
                    time.sleep(1)
                    if use_expedited_plans:
                        time.sleep(0.5)
                        desktop.left_click(685, 569)
                        time.sleep(0.5)
                        desktop.left_click(1439, 759)
                        time.sleep(1)
                    # hire recruitment operator
                    desktop.left_click(487, 571)
                    time.sleep(1)
                    # contingency hire
                    desktop.left_click(487, 571)
                    time.sleep(1)
                    desktop.left_click(1832, 65)
                    # exit operator introduction
                    in_recruit_menu = False
                    for j in range(16):
                        desktop.left_click(484, 458)
                        time.sleep(1)
                        img = Arknights.take_bounded_screenshot((219, 190), (328, 228), save_screenshot=False)
                        # break when in recruit menu
                        if Arknights.find_text_in_image(img, "Recruit"):
                            in_recruit_menu = True
                            break
                    if not in_recruit_menu:
                        output_box("Stuck in operator introduction.\n")
                        auto_hdl = win32gui.FindWindow(None, auto_recruit_window_name)
                        win32gui.SetForegroundWindow(auto_hdl)
                        return
                output_box(f"Recruited {recruit_num} times. Ending AutoRecruit.\n")
                img = Arknights.take_bounded_screenshot((1248, 37), (1338, 79), save_screenshot=False)
                num_recruit_permits, img = Arknights.detect_text_in_image(img)
                output_box("Remaining number of recruitment permits: " + num_recruit_permits)
            else:
                output_box("Failed to enter Arknights' recruitment menu.\n")
        else:
            output_box("Failed to enter Arknights' home screen.\n")
    else:
        output_box("Failed to launch Arknights.\n")
    auto_hdl = win32gui.FindWindow(None, auto_recruit_window_name)
    win32gui.SetForegroundWindow(auto_hdl)

    # win32gui.CloseWindow(emu_hdl)
