import cv2
import os
import subprocess
import time
import win32gui
from pynput.keyboard import Key, Listener
import tkinter
from tkinter import font
from tkinter import scrolledtext
from tkinter import ttk
import tkinter_tools as tkTools
import desktop_control as desktop
import screen_capture_tools
import recruitment_database_tools as recruitTools

# tested on Windows 11
# pytesseract manual:  https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc
# Notable sections:
#   --psm N
# binding events in tkinter info: https://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-widget
# does not account for:
#   not enough recruitment tickets
#   not enough expedited plans

data = []
with open("data.txt", "r") as data_file:
    data = data_file.readlines()
# application version
overall_ver = data[0][:-1]
# recruitment database version
recruit_ver = data[1][:-1]
# path to Google Play Games
emulator_path = data[2][:-1]
# window title of Google Play Games
emulator_title = data[3][:-1]
AutoRecruit_ver = overall_ver + ".[" + recruit_ver + "]"
auto_recruit_window_name = "Auto Recruit"


def update_data():
    global overall_ver
    global recruit_ver
    global AutoRecruit_ver
    global emulator_path
    global emulator_title
    global data

    with open("data.txt", "r") as data_file:
        data = data_file.readlines()

    overall_ver = data[0][:-1]
    recruit_ver = data[1][:-1]
    AutoRecruit_ver = overall_ver + ".[" + recruit_ver + "]"
    # path to Google Play Games
    emulator_path = data[2][:-1]
    emulator_title = data[3][:-1]

# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# Arknights
# Screen resolution: 1920x1080, full-screen
#
# Arknights                     top_left     bot_left     bot_right
# Recruitment label position:   (1395, 645), (1395, 701), (1625, 715)
# Recruit button position:      (1389, 701), (1388, 811), (1628, 830)
# Start button:                 (799, 712),               (1106, 814)
#
# Recruit text position:        (219, 190),  (219, 228),  (328, 228)
# Recruit box 1:                (26, 273),   (26, 644),   (943, 644)
# Recruit box 2:                (973, 273),  (973, 644),  (1890, 644)
# Recruit box 3:                (26, 689),   (26, 1060),  (943, 1060)
# Recruit box 4:                (973, 689),  (973, 1060), (1890, 1060)
# Recruitment permits count:    (1248, 37),  (1248, 79),  (1338, 79)
# Expedite button:              (448, 522),  (448, 617),  (922, 617)
# Confirm expedite button:      (960, 704),  (960, 815),  (1919, 814)
# Hire recruit button:          (45, 525),   (45, 618),   (930, 618)
# Skip gacha animation:         (1762, 15),  (1762, 116), (1902, 116)
#
# tested in recruit box 1       top_left     bot_left     bot_right
# Recruitment time (hours):     (632, 299),  (632, 388),  (742, 388)
# Recruitment time (minutes):   (878, 299),  (878, 388),  (988, 388)
# Recruitment time (seconds):   (1121, 299), (1121, 388), (1231, 388)
# Hour up button:               (570, 189),  (570, 260),  (787, 260)
# Hour down button:             (567, 409),  (567, 481),  (782, 481)
# Minute up button:             (817, 190),  (817, 260),  (1034, 260)
# Minute down button:           (812, 409),  (812, 481),  (1030, 481)
# Recruitment tag 1:            (563, 540),  (563, 608),  (778, 608)
# Recruitment tag 2:            (813, 540),  (813, 608),  (1028, 608)
# Recruitment tag 3:            (1063, 540), (1063, 608), (1278, 608)
# Recruitment tag 4:            (563, 648),  (563, 716),  (778, 716)
# Recruitment tag 5:            (813, 648),  (813, 716),  (1028, 716)
# Refresh count:                (1289, 108), (1289, 142), (1413, 142)
# Refresh button:               (1405, 560), (1404, 657), (1502, 657)
# Confirm button:               (1331, 834), (1331, 908), (1604, 908)
# Cancel button:                (1331, 932), (1331, 1006),(1604, 1006)
#
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# Google Play Games
#
# Google Play Games             top_left     bot_right
# Library button w/ text:       (23, 474),   (178, 533)
# Library button position:      (23, 474),   (82, 533)
# Screen resolution: 1920x1080, maximised w/ no taskbar
#
# Google Play Games             top_left     bot_right
# Library button w/ text:       (18, 323),   (168, 382)
# Library button position:      (18, 323),   (77, 382)
# Screen resolution: 1920x1080, scaled to its smallest size of 1298x797
#
# Arknights play button         top_left     bot_right
# 1920x1080:                    (x-429, 241) (x-370, 300)
# 1920x1080, --> 1298x797:      (x-306, 241) (x-248, 300)
# x = rightmost pixel of the window
#
# Arknights text bounds         top_left     bot_right
# 1920x1080:                    (480, 230),  (590, 260)
# 1920x1080, --> 1298x797:      (350, 230),  (460, 260)
#
# Arknights button              left    top     bottom
# 1920x1080:                    399     230     310
# 1920x1080, --> 1298x797:      266     230     310
#
# Google Play Games             top_left     bot_right
# "Get Ready...Arknights" text: (460, 240),  (1460, 840)
# Notes: 1920x1080 monitor, cannot be moved from center
#
# Notes:
#   - Window sizes on Windows 11 seem to have 5 extra pixels on all sides
#   - Cannot find the "Recruit" button
#   - Can find the "Recruitment" label
#       - Cannot find it when full-screen and not deskewed
#       - Can find it when zoomed in on the label
#
# ------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------
# Special recruitment rules:
#   - all 6-stars share the [Top Operator] tag (last checked: Il Siracusano event)
#   - all 5-stars share the [Senior Operator] tag (last checked: Il Siracusano event)
#   - all 2-stars share the [Starter] tag (last checked: Il Siracusano event)
#   - all 1-stars share the [Robot] tag (last checked: Il Siracusano event)
#   - 1-stars can be obtained without a [Robot] tag
#   - 6-stars can only be obtained with a [Top Operator] tag


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
    emu = screen_capture_tools.Tools(emulator_title)
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


def start_AutoRecruit(emulator_path: str, emulator_title: str, recruit_num: int=0, recruit_time: str="00:00", use_expedited_plans=False, prepare_recruitment=False, priority_tags=[], skip_emulator_launch=False):
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
            Arknights = screen_capture_tools.Tools("Arknights")
            ark_hdl = win32gui.FindWindow(None, "Arknights")
            win32gui.SetForegroundWindow(ark_hdl)
            time.sleep(0.5)
        else:
            time.sleep(10)
            Arknights = screen_capture_tools.Tools("Arknights")
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
                output_text("Starting number of recruitment permits: " + num_recruit_permits)
                tag_positions_list = [[(563, 540), (778, 608)],
                                      [(813, 540), (1028, 608)],
                                      [(1063, 540), (1278, 608)],
                                      [(563, 648), (778, 716)],
                                      [(813, 648), (1028, 716)]
                                      ]
                allTags_dict = recruit_tools.tag_dict
                allTag_valuesList = list(allTags_dict.values())
                allTag_keysList = list(allTags_dict.keys())
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
                                        output_text("Warning: recognized duplicate tag.\nContinuing with operation.\n")
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
                            output_text("Error: Failed to recognize tag.\n")
                            auto_hdl = win32gui.FindWindow(None, auto_recruit_window_name)
                            win32gui.SetForegroundWindow(auto_hdl)
                            return
                    # determine best tag combination
                    result = recruit_tools.find_best_tags(available_tags, priority_tags)
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
                        output_text("Stuck in operator introduction.\n")
                        auto_hdl = win32gui.FindWindow(None, auto_recruit_window_name)
                        win32gui.SetForegroundWindow(auto_hdl)
                        return
                output_text(f"Recruited {recruit_num} times. Ending AutoRecruit.\n")
                img = Arknights.take_bounded_screenshot((1248, 37), (1338, 79), save_screenshot=False)
                num_recruit_permits, img = Arknights.detect_text_in_image(img)
                output_text("Remaining number of recruitment permits: " + num_recruit_permits)
            else:
                output_text("Failed to enter Arknights' recruitment menu.\n")
        else:
            output_text("Failed to enter Arknights' home screen.\n")
    else:
        output_text("Failed to launch Arknights.\n")
    auto_hdl = win32gui.FindWindow(None, auto_recruit_window_name)
    win32gui.SetForegroundWindow(auto_hdl)

    # win32gui.CloseWindow(emu_hdl)




def swap_frame_grids(old_frame: ttk.Frame, new_frame: ttk.Frame):
    """
    Only works with frames with grids
    """
    old_frame.grid_remove()
    new_frame.grid()


screen_res = (1920, 1080)
scr_mdpt = (int(screen_res[0] / 2), int(screen_res[1] / 2))
recruit_tools = recruitTools.tools()

root = tkTools.MainWindow(auto_recruit_window_name, window_size=(992, 450), min_size=(500, 200))
tkTools.grid_setup(root,
                   [
                        [0, None, None, None, 1]
                    ],
                   [
                        [0, None, None, None, 1]
                    ]
                   )
root_frame = tkTools.Frame(root)
tkTools.grid_into(root_frame, column=0, row=0, sticky="NSEW")
root_frame.columnconfigure(0, weight=1)
root_frame.rowconfigure(0, weight=1)
# tag dictionaries and lists for creating tag listboxes
tagsQual_dict = {
    "ROB": "Robot",
    "STR": "Starter",
    "SEN": "Senior Operator",
    "TOP": "Top Operator"
}
tagsPos_dict = {
    "MEL": "Melee",
    "RNG": "Ranged"
}
tagsClass_dict = {
    "CAS": "Caster",
    "DEF": "Defender",
    "GUA": "Guard",
    "MED": "Medic",
    "SNI": "Sniper",
    "SPE": "Specialist",
    "SUP": "Supporter",
    "VAN": "Vanguard"
}
tagsSpec_dict = {
    "AOE": "AoE",
    "CDC": "Crowd-Control",
    "DBF": "Debuff",
    "DFS": "Defense",
    "DPR": "DP-Recovery",
    "DPS": "DPS",
    "FRD": "Fast-Redeploy",
    "HEA": "Healing",
    "NUK": "Nuker",
    "SFT": "Shift",
    "SLW": "Slow",
    "SMN": "Summon",
    "SPT": "Support",
    "SRV": "Survival"
}
tagsQual_keysList = list(tagsQual_dict.keys())
tagsQual_valuesList = list(tagsQual_dict.values())
tagsPos_keysList = list(tagsPos_dict.keys())
tagsPos_valuesList = list(tagsPos_dict.values())
tagsClass_keysList = list(tagsClass_dict.keys())
tagsClass_valuesList = list(tagsClass_dict.values())
tagsSpec_keysList = list(tagsSpec_dict.keys())
tagsSpec_valuesList = list(tagsSpec_dict.values())

# home frame
home_frame = tkTools.Frame(root_frame)
tkTools.grid_into(home_frame, column=0, row=0, sticky="NSEW")
tkTools.grid_setup(home_frame,
                   [
                        [0, None, None, None, 1]
                    ],
                   [
                        [0, 60, None, None, 0],
                        [1, None, None, None, 10],
                        [2, None, None, None, 1]
                    ]
                   )
home_frame.grid_remove()

# AutoRecruit frame
auto_recruit_frame = tkTools.Frame(root_frame)
tkTools.grid_into(auto_recruit_frame, column=0, row=0, sticky="NSEW")
tkTools.grid_setup(auto_recruit_frame,
                   [
                        [0, 134, None, None, 0],
                        [1, 400, None, None, 1],
                        [2, 200, None, None, 0]
                    ],
                   [
                        [0, 50, None, None, 0],
                        [1, 340, None, None, 1]
                    ]
                   )
auto_recruit_frame.grid_remove()

# database_tools frame
database_tools_frame = tkTools.Frame(root_frame)
tkTools.grid_into(database_tools_frame, column=0, row=0, sticky="NSEW")
tkTools.grid_setup(database_tools_frame,
                   [
                        [0, 134, None, None, 0],
                        [1, 400, None, None, 1],
                        [2, 100, None, None, 0]
                    ],
                   [
                        [0, 40, None, None, 0],
                        [1, 340, None, None, 1],
                        [2, 50, None, None, 0]
                    ]
                   )
database_tools_frame.grid_remove()


# widgets for the frames
def home_frame_widgets():
    title = tkTools.Label(home_frame, display_text="Arknights AutoRecruit", font=("Helvetica", 16, "bold"), text_padding=10)
    title.grid(column=0, row=0, sticky="NW")
    menu = tkTools.Frame(home_frame)
    menu.grid(column=0, row=1, sticky="NSEW")
    tkTools.grid_setup(menu,
                       [
                            [0, None, None, None, 1]
                        ],
                       [
                            [0, 30, None, None, 0],
                            [1, 30, None, None, 0]
                        ]
                       )
    recruit_button = tkTools.Button(menu, display_text="Enter AutoRecruit",
                                    function_when_clicked=tkTools.swap_frame(home_frame, auto_recruit_frame))
    recruit_button.grid(column=0, row=0, sticky="NE")
    database_tools_button = tkTools.Button(menu, display_text="Database Tools",
                                           function_when_clicked=tkTools.swap_frame(home_frame, database_tools_frame))
    database_tools_button.grid(column=0, row=1, sticky="NE")
    database_tools_button.bind("<ButtonPress>", lambda e: recruit_tools.open_db())
    setup_button = tkTools.Button(home_frame, display_text="Setup", function_when_clicked=None)
    setup_button.grid(column=0, row=2, sticky="SE")


def auto_recruit_widgets():
    back_button = tkTools.Button(auto_recruit_frame, display_text="Back",
                                 function_when_clicked=tkTools.swap_frame(auto_recruit_frame, home_frame))
    back_button.grid(column=0, row=0, sticky="NW")

    # output textbox
    global output_text
    global output_indented_text
    output_textbox = scrolledtext.ScrolledText(auto_recruit_frame, height=18)
    output_textbox.grid(column=1, row=1, sticky="NEW")
    output_text_font = font.nametofont(output_textbox.cget("font"))
    output_textbox.tag_configure("indent", lmargin1=output_text_font.measure("    "), lmargin2=output_text_font.measure("    "))
    output_textbox.configure(state="disabled")
    def output_text(text):
        output_textbox.configure(state="normal")
        output_textbox.insert("end", text)
        output_textbox.configure(state="disabled")
    def output_indented_text(text):
        output_textbox.configure(state="normal")
        output_textbox.insert("end", text, "indent")
        output_textbox.configure(state="disabled")

    # frame for packing buttons
    button_display_frame = tkTools.Frame(auto_recruit_frame)
    button_display_frame.grid(column=0, row=1, sticky="NSEW")
    get_window_titles_button = tkTools.Button(button_display_frame, display_text="Get opened\nwindow titles",
                                              function_when_clicked=lambda: [output_text("Window titles:\n"),
                                                                              output_indented_text(screen_capture_tools.get_window_titles()),
                                                                              output_text("\n")])
    get_window_titles_button.pack(side="top", anchor="nw")
    def open_help_window():
        help_window = tkTools.SubWindow(root, title="Instructions", window_size=(600, 400), background_color="white")
        # Text for [Using AutoRecruit]
        label1 = tkTools.Label(help_window, display_text="Using AutoRecruit", font=("Helvetica", 12, "bold"), background_color="white")
        label1.pack(side="top", anchor="nw", fill="x")
        help_textbox1 = tkTools.Text(help_window, wrap_on="word", font=("Segoe UI", 9), backdrop="flat", height=6)
        help_textbox1.pack(side="top", anchor="nw", fill="x")
        text1 = "To get the emulator's path, right click on the application and select [Copy as path].\n" \
                "To get the emulator's window title, try using the [Get opened window titles] button.\n" \
                "This button will output a list of presently open window titles, separated by curly brackets. " \
                "If the emulator is open, it's title will appear in the output box.\n" \
                "If the emulator is open, it's window title will appear in the output box.\n"
        help_textbox1.insert("end", text1)
        help_textbox1.configure(state="disabled")
        # Text for [Setup]
        label2 = tkTools.Label(help_window, display_text="Setup", font=("Helvetica", 12, "bold"), background_color="white")
        label2.pack(side="top", anchor="nw", fill="x")
        help_textbox2 = tkTools.Text(help_window, wrap_on="word", backdrop="flat", height=10)
        help_textbox2.pack(side="top", anchor="nw", fill="x")
        help_text_font2 = font.nametofont(help_textbox2.cget("font"))
        help_textbox2.tag_configure("indent", lmargin1=help_text_font2.measure("  "), lmargin2=help_text_font2.measure("  "))
        text2_1h = "[Recruitment permits]\n"
        text2_1p = "The number of recruitment permits to be used by AutoRecruit.\n"
        text2_2h = "[Priority Tags]\n"
        text2_2p = "Determines the tag combinations that AutoRecruit will prioritize (top-to-bottom).\n" \
                   "Drag and drop to reorder the list, use the swap button to add/remove priorities."\
                   "If no matching tags are found, AutoRecruit will recruit with no tags selected at the specified recruit time.\n"
        text2_3h = "[Expedited Plans]\n"
        text2_3p = "If checked, AutoRecruit will use expedited plans.\n"
        text2_4h = "[Save]\n"
        text2_4p = "Saves the current configuration.\n"
        text2_5h = "[Start]\n"
        text2_5p = "Starts AutoRecruit. It will continue to run until the specified number of recruitment permits have been used.\n"
        text2_6h = "[Force Stop]\n"
        text2_6p = "Stops AutoRecruit from running any further. Closing the application will also stop AutoRecruit."
        help_textbox2.insert("end", text2_1h)
        help_textbox2.insert("end", text2_1p, "indent")
        help_textbox2.insert("end", text2_2h)
        help_textbox2.insert("end", text2_2p, "indent")
        help_textbox2.insert("end", text2_3h)
        help_textbox2.insert("end", text2_3p, "indent")
        help_textbox2.insert("end", text2_4h)
        help_textbox2.insert("end", text2_4p, "indent")
        help_textbox2.insert("end", text2_5h)
        help_textbox2.insert("end", text2_5p, "indent")
        help_textbox2.insert("end", text2_6h)
        help_textbox2.insert("end", text2_6p, "indent")
        help_textbox2.configure(font=("Segoe UI", 9))
        help_textbox2.configure(state="disabled")
    help_button = tkTools.Button(button_display_frame, display_text="Help", function_when_clicked=lambda: open_help_window(), width=4)
    help_button.pack(side="top", anchor="nw")




    # settings frame setup --start--
    # frame containing the setup for AutoRecruit
    settings_frame = tkTools.Frame(auto_recruit_frame)
    settings_frame.grid(column=2, row=1, sticky="NSEW")
    skip_emulator_launch_Var = tkinter.BooleanVar()
    use_expedited_plans_Var = tkinter.BooleanVar()
    prep_recruitments_Var = tkinter.BooleanVar()
    operators_list = recruit_tools.get_operator_data(get=["name"], sort_order=[["name", "asc"]], reduce_nested_lists=True)
    priority_list = data[8][:-1].split("|")
    priority_extras_list = ["6-star", "5-star", "4-star"]
    priority_extras_list.extend(operators_list)
    priority_extras_list = [item for item in priority_extras_list if item not in priority_list]
    recruitment_times_list = []
    for hours in range(1, 10):
        if hours < 10:
            hours = f"0{hours}"
        for minutes in range(0, 60, 10):
            if minutes < 10:
                minutes = f"0{minutes}"
            recruitment_times_list.append(f"{hours}:{minutes}")
            if hours == f"09":
                break
    emulator_path_entry = tkTools.Entry(settings_frame, width=32)
    emulator_path_entry.pack(side="top", anchor="nw")
    emulator_path_entry.insert(0, emulator_path)
    emulator_title_entry = tkTools.Entry(settings_frame, width=32)
    emulator_title_entry.pack(side="top", anchor="nw")
    emulator_title_entry.insert(0, emulator_title)
    skip_emulator_checkbutton = tkTools.Checkbutton(settings_frame, display_text="Start from Arknights home screen", saveValueTo_variable=skip_emulator_launch_Var)
    skip_emulator_checkbutton.pack(side="top", anchor="nw")
    # frame for recruitment_permits widgets --start--
    recruitment_permits_frame = tkTools.Frame(settings_frame)
    recruitment_permits_frame.pack(side="top", anchor="nw")
    recruitment_permits_label = tkTools.Label(recruitment_permits_frame, display_text="Recruitment Permits:", text_alignment="left", width=20)
    recruitment_permits_label.pack(side="left", anchor="nw")
    recruitment_permits_entry = tkTools.Entry(recruitment_permits_frame, width=6)
    recruitment_permits_entry.pack(side="left", anchor="nw")
    recruitment_permits_entry.insert(0, data[4][:-1])
    # frame for recruitment_permits widgets --end--


    # frame for ordering tag priorities --start--
    priority_tags_frame = tkTools.Frame(settings_frame)
    priority_tags_frame.pack(side="top", anchor="nw")
    tkTools.grid_setup(priority_tags_frame,
                       [
                            [0, None, None, None, None],
                            [1, None, None, None, None],
                            [2, None, None, None, None],
                            [3, None, None, None, None],
                            [4, None, None, None, None]
                        ],
                       [
                            [0, None, None, None, None],
                            [1, None, None, None, None]
                        ]
                       )
    priority_label = tkTools.Label(priority_tags_frame, display_text="Priority Tags")
    priority_label.grid(column=0, row=0, columnspan=3, sticky="NW")
    priority_listbox = tkTools.Listbox_with_drag_drop(
        priority_tags_frame,
        list_variable=tkinter.StringVar(value=priority_list),
        select_mode="multiple",
        stay_selected_when_unfocused=True,
        backdrop="ridge",
        height=6,
        width=14
    )
    priority_listbox.grid(column=0, row=1, rowspan=4)
    priority_extras_listbox = tkTools.Listbox(
        priority_tags_frame,
        list_variable=tkinter.StringVar(value=priority_extras_list),
        select_mode="multiple",
        stay_selected_when_unfocused=True,
        backdrop="ridge",
        height=6,
        width=14
    )
    priority_extras_listbox.grid(column=2, row=1, rowspan=4)
    def add_remove_priority():
        selected_list = []
        while priority_listbox.curselection():
            i = priority_listbox.curselection()[0]
            selected_list.insert(0, priority_listbox.get(i))
            priority_listbox.delete(i)
        for item in selected_list:
            if item in operators_list:
                listbox_list = priority_extras_listbox.get(0, "end")
                i = operators_list.index(item)
                # if i == 0:
                #     i += 1
                #     next_operator = operators_list[i]
                #     while next_operator not in listbox_list:
                #         i += 1
                #         next_operator = operators_list[i]
                #     i = listbox_list.index(next_operator)
                # check below
                prev_operator = operators_list[i]
                while i > 0 and prev_operator not in listbox_list:
                    i -= 1
                    prev_operator = operators_list[i]
                # if none below, check above
                if i == 0:
                    i = operators_list.index(item)
                    i += 1
                    next_operator = operators_list[i]
                    while next_operator not in listbox_list:
                        i += 1
                        next_operator = operators_list[i]
                    i = listbox_list.index(next_operator)
                else:
                    i = listbox_list.index(prev_operator) + 1
                priority_extras_listbox.insert(i, item)
            else:
                priority_extras_listbox.insert(0, item)
        selected_list = []
        while priority_extras_listbox.curselection():
            i = priority_extras_listbox.curselection()[0]
            selected_list.insert(0, priority_extras_listbox.get(i))
            priority_extras_listbox.delete(i)
        for item in selected_list:
            priority_listbox.insert(0, item)
    def clear_selection():
        priority_listbox.selection_clear(0, "end")
        priority_extras_listbox.selection_clear(0, "end")
    add_remove_priority_button = tkTools.Button(priority_tags_frame, display_text="<->", width=4, function_when_clicked=lambda: add_remove_priority())
    add_remove_priority_button.grid(column=1, row=2)
    clear_selection_button = tkTools.Button(priority_tags_frame, display_text="Clr", width=4, function_when_clicked=lambda: clear_selection())
    clear_selection_button.grid(column=1, row=3)
    # frame for ordering tag priorities --end--


    recruitment_time_spinbox = tkTools.Spinbox(settings_frame, values=recruitment_times_list, width=8, state="readonly")
    recruitment_time_spinbox.pack(side="top", anchor="nw")
    recruitment_time_spinbox.set(data[5][:-1])
    expedited_plans_checkbutton = tkTools.Checkbutton(settings_frame, display_text="Use expedited plans", saveValueTo_variable=use_expedited_plans_Var)
    expedited_plans_checkbutton.pack(side="top", anchor="nw")
    if data[6][:-1] == "True":
        use_expedited_plans_Var.set(True)
    prepare_recruitments_checkbutton = tkTools.Checkbutton(settings_frame, display_text="Prepare recruitments afterwards", saveValueTo_variable=prep_recruitments_Var)
    prepare_recruitments_checkbutton.pack(side="top", anchor="nw")
    if data[7][:-1] == "True":
        prep_recruitments_Var.set(True)
    def update_data_file():
        data[2] = emulator_path_entry.get() + "\n"
        data[3] = emulator_title_entry.get() + "\n"
        data[4] = recruitment_permits_entry.get() + "\n"
        data[5] = recruitment_time_spinbox.get() + "\n"
        data[6] = str(use_expedited_plans_Var.get()) + "\n"
        data[7] = str(prep_recruitments_Var.get()) + "\n"
        data[8] = "|".join(priority_listbox.get(0, "end")) + "\n"
        with open("data.txt", "w") as data_file:
            data_file.writelines(data)
        update_data()
    save_button = tkTools.Button(settings_frame, display_text="Save", function_when_clicked=lambda: update_data_file())
    save_button.pack(side="top", anchor="nw")
    start_button = tkTools.Button(settings_frame, display_text="Start",
                                  function_when_clicked=lambda: start_AutoRecruit(
                                       emulator_path_entry.get(),
                                       emulator_title_entry.get(),
                                       int(recruitment_permits_entry.get()),
                                       recruitment_time_spinbox.get(),
                                       use_expedited_plans_Var.get(),
                                       prep_recruitments_Var.get(),
                                       priority_listbox.get(0, "end"),
                                       skip_emulator_launch=skip_emulator_launch_Var.get()
                                   ))
    start_button.pack(side="top", anchor="nw")

    # settings frame setup --end--




def database_tools_widgets():
    back_button = tkTools.Button(database_tools_frame, display_text="Back",
                                 function_when_clicked=lambda: [tkTools.swap_frame(database_tools_frame, home_frame, _use_with_lambda_function=True), recruit_tools.calculate()])
    back_button.grid(column=0, row=0, sticky="NW")




    # initial operator form setup --start--

    # frame containing the settings to add an operator to the database
    operator_form = tkTools.Frame(database_tools_frame)
    operator_form.grid(column=2, row=1, rowspan=2, sticky="NSEW")
    tkTools.grid_setup(operator_form,
                       [
                            [0, 150, None, None, 0]
                        ],
                       [
                            [0, 30, None, None, 0],
                            [1, 30, None, None, 0],
                            [2, 150, None, None, 0],
                            [3, 30, None, None, 0],
                            [4, 30, None, None, 0],
                            [5, 30, None, None, 0],
                            [6, 30, None, None, 1],
                            [7, 30, None, None, 0]
                        ]
                       )

    # global variables and widgets for extra access
    nameVar = tkinter.StringVar()
    rarityVar = tkinter.StringVar()
    idVar = tkinter.StringVar()
    name_entry = tkTools.Entry(operator_form, saveValueTo_variable=nameVar)
    name_entry.grid(column=0, row=0, sticky="NW")
    # frame for packing tag options inside a gridded frame
    tag_options = tkTools.Frame(operator_form)
    tag_options.grid(column=0, row=2, sticky="NSEW")
    tags_label = tkTools.Label(tag_options, display_text="Tags")
    tags_label.pack(side="top", anchor="nw")
    tagsQual_lbox = tkTools.Listbox(
        tag_options,
        list_variable=tkinter.StringVar(value=tagsQual_valuesList),
        select_mode="multiple",
        stay_selected_when_unfocused=True,
        backdrop="ridge",
        height=6,
        width=14
    )
    tagsPos_lbox = tkTools.Listbox(
        tag_options,
        list_variable=tkinter.StringVar(value=tagsPos_valuesList),
        select_mode="multiple",
        stay_selected_when_unfocused=True,
        backdrop="ridge",
        height=6,
        width=7
    )
    tagsClass_lbox = tkTools.Listbox(
        tag_options,
        list_variable=tkinter.StringVar(value=tagsClass_valuesList),
        select_mode="multiple",
        stay_selected_when_unfocused=True,
        backdrop="ridge",
        height=6,
        width=9
    )
    tagsSpec_lbox = tkTools.Listbox(
        tag_options,
        list_variable=tkinter.StringVar(value=tagsSpec_valuesList),
        select_mode="multiple",
        stay_selected_when_unfocused=True,
        backdrop="ridge",
        height=6,
        width=12
    )
    tagsQual_lbox.pack(side="left", anchor="nw", padx=(0, 0))
    tagsPos_lbox.pack(side="left", anchor="nw", padx=(0, 0))
    tagsClass_lbox.pack(side="left", anchor="nw", padx=(0, 0))
    tagsSpec_lbox.pack(side="left", anchor="nw", padx=(0, 0))

    # initial operator form setup --end--




    # table setups --start--

    # table of recruitable operators
    operator_table = tkTools.Frame_with_scrollbar(database_tools_frame, sticky_scrollframe="NSEW",
                                                  sticky_content="NSEW", height=360, width=520,
                                                  grid_row=1, grid_column=1)
    tkTools.grid_setup(operator_table,
                       [
                            [0, 40, None, None, 0],
                            [1, 10, None, None, 0],
                            [2, 200, None, None, 0],
                            [3, 100, None, None, 0]
                        ],
                       []
                       )
    # configure operator_table
    def configure_operator_table():
        operator_list = recruit_tools.get_operator_data(get=["all"])

        # method for filling the operator form by selecting a row in the operator table
        def fill_operator_form_with_table_row(row, cols):
            tagsQual_lbox.selection_clear(0, "end")
            tagsPos_lbox.selection_clear(0, "end")
            tagsClass_lbox.selection_clear(0, "end")
            tagsSpec_lbox.selection_clear(0, "end")
            name_entry.configure(foreground="black")
            idVar.set(operator_list[row][0])
            rarityVar.set(operator_list[row][1])
            nameVar.set(operator_list[row][2])
            tags_list = recruit_tools.split_tags(operator_list[row][3])
            for tag in tags_list:
                if tagsQual_dict.get(tag):
                    tagsQual_lbox.selection_set(tagsQual_keysList.index(tag))
                if tagsPos_dict.get(tag):
                    tagsPos_lbox.selection_set(tagsPos_keysList.index(tag))
                if tagsClass_dict.get(tag):
                    tagsClass_lbox.selection_set(tagsClass_keysList.index(tag))
                if tagsSpec_dict.get(tag):
                    tagsSpec_lbox.selection_set(tagsSpec_keysList.index(tag))

        num_rows = len(operator_list)
        num_cols = len(operator_list[0])
        table = [[ttk.Entry() for col in range(num_cols)] for row in range(num_rows)]
        for r in range(num_rows):
            operator_table.rowconfigure(r, weight=0)
            for c in range(num_cols):
                if c == 0:
                    table[r][c] = tkTools.Entry(operator_table, width=5)
                if c == 1:
                    table[r][c] = tkTools.Entry(operator_table, width=2, text_color="grey")
                if c == 2:
                    table[r][c] = tkTools.Entry(operator_table, width=25)
                if c == 3:
                    table[r][c] = tkTools.Entry(operator_table, width=25)
                table[r][c].grid(column=c, row=r)
                table[r][c].insert(0, operator_list[r][c])
                table[r][c].configure(state="readonly")
                table[r][c].bind("<FocusIn>", lambda event, row=r, cols=num_cols: fill_operator_form_with_table_row(row, cols))
        operator_table.finish_scrollbar_frame_setup()
    configure_operator_table()
    operator_table.grid_remove()

    # table of tag combinations
    raw_tag_combos_text = scrolledtext.ScrolledText(database_tools_frame, height=18)
    raw_tag_combos_text.grid(column=1, row=1, sticky="NEW")
    def configure_tag_combinations_table():
        raw_tag_combos_text.delete(1.0, "end")
        tag_combinations_txt = [recruit_tools.non_dist_combos,
                                recruit_tools.r4_tag_combos_dist,
                                recruit_tools.r5_tag_combos_dist,
                                recruit_tools.r6_tag_combos_dist
                                ]
        for i, rarity_row in enumerate(tag_combinations_txt):
            if i == 0:
                raw_tag_combos_text.insert("end", "rarity 3-4\n")
            else:
                raw_tag_combos_text.insert("end", "\nrarity")
                raw_tag_combos_text.insert("end", str(i+3))
                raw_tag_combos_text.insert("end", "\n")
            for combo_count_row in rarity_row:
                for combo in combo_count_row:
                    raw_tag_combos_text.insert("end", ",".join(combo) + "|")
                raw_tag_combos_text.insert("end", "\n")
        raw_tag_combos_text.configure(state="disabled")
    configure_tag_combinations_table()
    raw_tag_combos_text.grid_remove()
    operator_table.grid()

    # method for swapping tables
    class table_tool:
        current_id = 0
        table_frame_id = {}
    table_control = table_tool
    table_control.current_id = 1
    table_control.table_frame_id[1] = operator_table
    table_control.table_frame_id[2] = raw_tag_combos_text

    def swap_table_frame_grids(new_table_frame_id: int):
        """
        Refer to the table_frame_dict for table_frame ids
        """
        if new_table_frame_id != table_control.current_id:
            table_control.table_frame_id[table_control.current_id].grid_remove()
            table_control.table_frame_id[new_table_frame_id].grid()
            table_control.current_id = new_table_frame_id

    # method for updating the current table after updating the recruitment database
    def configure_tables():
        configure_operator_table()
        configure_tag_combinations_table()

    # table setups --end--




    # buttons to change the displayed data
    button_display_frame = tkTools.Frame(database_tools_frame)
    button_display_frame.grid(column=0, row=1, sticky="NSEW")
    operator_table_button = tkTools.Button(button_display_frame, display_text="Operator Table", function_when_clicked=lambda: swap_table_frame_grids(1))
    operator_table_button.pack(side="top", anchor="nw")
    tag_combinations_table_button = tkTools.Button(button_display_frame, display_text="Tag Combinations", function_when_clicked=lambda: swap_table_frame_grids(2))
    tag_combinations_table_button.pack(side="top", anchor="nw")
    recalculate_button = tkTools.Button(button_display_frame, display_text="Recalculate\nTag Combinations", function_when_clicked=lambda: [recruit_tools.calculate(), configure_tables()])
    recalculate_button.pack(side="top", anchor="nw")
    def open_help_window():
        help_window = tkTools.SubWindow(root, title="Instructions", window_size="400x300")
        text1 = "Using the database"
        text2 = "Updating an operator:\n" \
                "        Requires name, tags\n" \
                "Adding a new operator:\n" \
                "        Requires name, rarity, tags\n" \
                "Deleting an operator:\n" \
                "        Requires operator ID"
        label1 = tkTools.Label(help_window, display_text=text1, font=("Helvetica", 12, "bold"))
        label1.pack(side="top", anchor="nw")
        label2 = tkTools.Label(help_window, display_text=text2)
        label2.pack(side="top", anchor="nw")
        label2.configure(wraplength=400)
    help_button = tkTools.Button(button_display_frame, display_text="Help", function_when_clicked=lambda: open_help_window(), width=4)
    help_button.pack(side="top", anchor="nw")

    # version frame
    version_frame = tkTools.Frame(database_tools_frame)
    version_frame.grid(column=0, row=2, columnspan=2, sticky="NSEW")
    version_label = tkTools.Label(version_frame, display_text="ver. " + AutoRecruit_ver, font=("Courier", 8))
    version_label.configure(foreground="grey")
    version_label.pack(side="bottom", anchor="sw")
    def open_update_version_window():
        version_window = tkinter.Toplevel(root)
        version_window.title("Update recruitment version")
        version_window.geometry("400x110")
        version_textbox = tkTools.Text(version_window, width=20, height=2)
        version_textbox.pack(side="top", anchor="nw")
        version_textbox.insert("end", recruit_ver)
        def update_version():
            data[1] = version_textbox.get("1.0", "end")
            with open("data.txt", "w") as data_file:
                data_file.writelines(data)
            update_data()
            version_label.configure(text="ver. " + AutoRecruit_ver)
        update_version_button = tkTools.Button(version_window, display_text="Update recruitment version",
                                               function_when_clicked=lambda: [update_version(), version_window.destroy(), version_window.update()])
        update_version_button.pack(side="top", anchor="nw")
        cancel_button = tkTools.Button(version_window, display_text="CANCEL", width=7,
                                       function_when_clicked=lambda: [version_window.destroy(), version_window.update()])
        cancel_button.pack(side="top", anchor="nw")
    recruit_version_button = tkTools.Button(version_frame, display_text="Update Version", function_when_clicked=lambda: open_update_version_window())
    recruit_version_button.pack(side="bottom", anchor="sw")




    # remaining operator form setup --start--

    def operator_form_widgets():
        # methods for implementing a default value in the name_entry widget
        def name_entry_default():
            name_entry.configure(foreground="grey")
            name_entry.insert(0, "Operator Name")
        def name_entry_Focus(focus_type: str):
            name = nameVar.get()
            if focus_type.lower() == "in":
                if name.lower() == "operator name":
                    name_entry.configure(foreground="black")
                    name_entry.delete(0, "end")
            if focus_type.lower() == "out":
                if not name or name.lower() == "operator name":
                    name_entry.configure(foreground="grey")
                    name_entry.delete(0, "end")
                    name_entry.insert(0, "Operator Name")
        name_entry_default()
        name_entry.bind("<FocusIn>", lambda e: name_entry_Focus("in"))
        name_entry.bind("<FocusOut>", lambda e: name_entry_Focus("out"))
        rarity_box = tkTools.Spinbox(operator_form, 1, 6, saveValueTo_variable=rarityVar, width=4)
        rarity_box.grid(column=0, row=1, sticky="NW")
        # buttons to update the table
        def update_recruit_db(statement_type: str):
            if statement_type == "insert" or statement_type == "update" or statement_type == "delete":
                operator_id = idVar.get()
                if statement_type == "delete":
                    delete_operator_window = tkinter.Toplevel(root)
                    delete_operator_window.title("Warning: Deleting Operator")
                    delete_operator_window.geometry("400x200")
                    delete_operator_window.grab_set()
                    delete_operator_window.bind("<FocusOut>", lambda e: [delete_operator_window.bell(), delete_operator_window.focus_force()])
                    operator_data = recruit_tools.get_operator_data(get=["all"], where=["id=" + operator_id])
                    if operator_data == None:
                        # error label
                        error_label = tkTools.Label(delete_operator_window, display_text="Error: operator_id_" + operator_id + " not found")
                        error_label.pack(side="top")
                    else:
                        # warning label
                        warning_label = tkTools.Label(delete_operator_window, display_text="Are you sure you want to delete the following operator:")
                        warning_label.pack(side="top")
                        # operator data
                        operator_data_str = "id:\t" + str(operator_data[0]) + "\nrarity:\t" + str(operator_data[1]) + "\nname:\t" + operator_data[2] + "\ntags:\t" + operator_data[3]
                        operator_data_label = tkTools.Label(delete_operator_window, display_text=operator_data_str, width=200)
                        operator_data_label.pack(side="top")
                        confirm_button = tkTools.Button(delete_operator_window, display_text="CONFIRM",
                                                        function_when_clicked=lambda: [recruit_tools.delete_operator(id=int(operator_id)), delete_operator_window.destroy(), delete_operator_window.update(), recruit_tools.calculate(), configure_tables()])
                        confirm_button.pack(side="top")
                    cancel_button = tkTools.Button(delete_operator_window, display_text="CANCEL", function_when_clicked=lambda: [delete_operator_window.destroy(), delete_operator_window.update()])
                    cancel_button.pack(side="top")
                else:
                    operator_name = nameVar.get()
                    rarity = rarityVar.get()
                    TQidx = tagsQual_lbox.curselection()
                    TPidx = tagsPos_lbox.curselection()
                    TCidx = tagsClass_lbox.curselection()
                    TSidx = tagsSpec_lbox.curselection()
                    tags = []
                    if TQidx:
                        for i in TQidx:
                            tags.append(tagsQual_keysList[i])
                    if TPidx:
                        for i in TPidx:
                            tags.append(tagsPos_keysList[i])
                    if TCidx:
                        for i in TCidx:
                            tags.append(tagsClass_keysList[i])
                    if TSidx:
                        for i in TSidx:
                            tags.append(tagsSpec_keysList[i])
                    if statement_type == "update":
                        recruit_tools.update_operator(orig_name=operator_name, new_tags=tags)
                        recruit_tools.calculate()
                    if statement_type == "insert":
                        recruit_tools.insert_new_operator(operator_name=operator_name, rarity=rarity, tag_list=tags)
                    recruit_tools.calculate()
                nameVar.set("")
                rarityVar.set("")
                idVar.set("")
                tagsQual_lbox.selection_clear(0, "end")
                tagsPos_lbox.selection_clear(0, "end")
                tagsClass_lbox.selection_clear(0, "end")
                tagsSpec_lbox.selection_clear(0, "end")
                name_entry_default()
                configure_tables()
        add_operator_button = tkTools.Button(operator_form, display_text="Add to Database", function_when_clicked=lambda: update_recruit_db("insert"))
        add_operator_button.grid(column=0, row=3, sticky="NW")
        update_operator_button = tkTools.Button(operator_form, display_text="Update Database", function_when_clicked=lambda: update_recruit_db("update"))
        update_operator_button.grid(column=0, row=4, sticky="NW")
        # undo_button = ttkTools.button_setup(operator_form, display_text="Undo", function=None, width=5)
        # undo_button.grid(column=0, row=5, sticky="NW")
        # delete operator options
        operator_id_entry = tkTools.Entry(operator_form, saveValueTo_variable=idVar, width=6)
        operator_id_entry.grid(column=0, row=6, sticky="SE")
        delete_operator_button = tkTools.Button(operator_form, display_text="Delete Operator", function_when_clicked=lambda: update_recruit_db("delete"))
        delete_operator_button.grid(column=0, row=7, sticky="SE")

    # remaining operator form setup --end--




    operator_form_widgets()

home_frame_widgets()
auto_recruit_widgets()
database_tools_widgets()
home_frame.grid()


root.mainloop()
