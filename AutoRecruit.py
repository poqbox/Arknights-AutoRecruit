import cv2
import os
import subprocess
import time
import win32gui
import tkinter
from tkinter import ttk
import DesktopControl as desktop
import ScreenCaptureTools
import recruitment_database_tools as setup_recruit

# tested on Windows 11
# pytesseract manual:  https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc
# Notable sections:
#   --psm N
# binding events in tkinter info: https://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-widget


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
# list of operators and their tag combination
# sort by rarity
#   1.  ignore class type
#   2.  if tag could be 6*, 5*, 4*, search tag combinations
#   3.  if no tag combination gives 6*, 5*, 4*, try next tag
#   4.  if no 6*, 5*, 4*, reshuffle and repeat
#   5.  if no 6*, 5*, 4*, search with lowest time and no tags


def launch_from_GooglePlayGames():
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
    emu = ScreenCaptureTools.Tools(emulator_title)
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
    search_w = 110
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


def start_AutoRecruit():
    launched_Arknights = launch_from_GooglePlayGames()
    if launched_Arknights:
        Arknights = ScreenCaptureTools.Tools("Arknights")
        time.sleep(10)
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

        # open Recruit menu
        if entered_Arknights_home_page:
            # take screenshot of recruitment label and deskew it
            img = Arknights.take_bounded_screenshot((1395, 645), (1625, 715), save_screenshot=False)
            img = Arknights.skew_image(img, ((0, 0), (0, 55), (230, 70)), ((0, 0), (0, 55), (235, 55)), save_image=False)
            # if Arknights.find_text_in_image(img, "Recruit"):
                # choose recruitment slot

                # get tags and find the best combination


        else:
            print("Failed to enter Arknights' home page")
    else:
        print("Failed to launch Arknights")

    # win32gui.CloseWindow(emu_hdl)


def raise_frame(frame):
    frame.tkraise()


# path to Google Play Games
emulator_title = "Google Play Games beta"
emulator_path = r'C:\Program Files\Google\Play Games\Bootstrapper.exe'
emu_hdl = None
screen_res = (1920, 1080)
scr_mdpt = (int(screen_res[0] / 2), int(screen_res[1] / 2))

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
    "AOE": "AOE",
    "CDC": "Crowd Control",
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

# padding=(all sides)
# padding=(left & right, top & bottom)
# padding=(left, top, right, bottom)

#
root = tkinter.Tk()
root.title("Auto Recruit")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("800x450")
root.minsize(400, 200)

# frames to switch between
mainframe = tkinter.ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky="NSEW")
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=0, minsize=60)
mainframe.rowconfigure(1, weight=10)
mainframe.rowconfigure(2, weight=1)
database_tools_frame = tkinter.ttk.Frame(root)
database_tools_frame.grid(column=0, row=0, sticky="NSEW")
database_tools_frame.columnconfigure(0, weight=0, minsize=150)
database_tools_frame.columnconfigure(1, weight=1, minsize=400)
database_tools_frame.rowconfigure(0, weight=0, minsize=50)
database_tools_frame.rowconfigure(1, weight=1, minsize=100)

# mainframe widgets
title = ttk.Label(mainframe, text="Arknights AutoRecruit", font=("Helvetica", 16, "bold"), padding=10)
title.grid(column=0, row=0, rowspan=20, sticky="NW")
ttk.Button(mainframe, text="Setup", command=None).grid(column=0, row=2, sticky="SE")
menu = tkinter.ttk.Frame(mainframe)
menu.grid(column=0, row=1, sticky="NSEW")
menu.columnconfigure(0, weight=1)
menu.rowconfigure(0, weight=0, minsize=30)
menu.rowconfigure(1, weight=0, minsize=30)
menu.rowconfigure(2, weight=0, minsize=30)
# mainframe --> menu widgets
ttk.Button(menu, text="Start AutoRecruit", command=None).grid(column=0, row=0, sticky="NE")
ttk.Button(menu, text="Database Tools", command=lambda:raise_frame(database_tools_frame)).grid(column=0, row=1, sticky="NE")
ttk.Button(menu, text="Update Recruitment Operators", command=None).grid(column=0, row=2, sticky="NE")

# database_tools_frame widgets
def insert_operator():
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
    print(operator_name, rarity, tags)
    nameVar.set("")
    rarityVar.set("")
    tagsQual_lbox.selection_clear(0, "end")
    tagsPos_lbox.selection_clear(0, "end")
    tagsClass_lbox.selection_clear(0, "end")
    tagsSpec_lbox.selection_clear(0, "end")

# def handle_focus_in():
#     operator_name_entry.configure(state="normal", foreground="black")
#     operator_name_entry.delete(0, "end")
#
# def handle_focus_out():
#     operator_name_entry.configure(state="normal", foreground="grey")
#     operator_name_entry.delete(0, "end")
#     operator_name_entry.insert(0, "Operator Name")

ttk.Button(database_tools_frame, text="Back", command=lambda:raise_frame(mainframe)).grid(column=0, row=0, sticky="NW")
operator_form = ttk.Frame(database_tools_frame)
operator_form.grid(column=1, row=1, sticky="NSEW")
operator_form.columnconfigure(0, weight=0, minsize=150)
operator_form.rowconfigure(0, weight=0, minsize=30)
operator_form.rowconfigure(1, weight=0, minsize=30)
operator_form.rowconfigure(2, weight=0, minsize=150)
operator_form.rowconfigure(3, weight=0, minsize=30)
nameVar = tkinter.StringVar()
rarityVar = tkinter.StringVar()
operator_name_entry = ttk.Entry(operator_form, textvariable=nameVar)
operator_name_entry.grid(column=0, row=0, sticky="NW")
# operator_name_entry.bind("<FocusIn>", handle_focus_in())
# operator_name_entry.bind("<FocusOut>", handle_focus_out())
ttk.Combobox(operator_form, textvariable=rarityVar, width=2, values=(1, 2, 3, 4, 5, 6)).grid(column=0, row=1, sticky="NW")
# configure_AutoRecruit_frame --> tag_options
tag_options = ttk.Frame(operator_form)
tag_options.grid(column=0, row=2, sticky="NSEW")
tagsQual_lbox = tkinter.Listbox(
    tag_options,
    listvariable=tkinter.StringVar(value=tagsQual_valuesList),
    selectmode="multiple",
    exportselection=False,
    relief="ridge",
    height=6,
    width=14
)
tagsPos_lbox = tkinter.Listbox(
    tag_options,
    listvariable=tkinter.StringVar(value=tagsPos_valuesList),
    selectmode="multiple",
    exportselection=False,
    relief="ridge",
    height=6,
    width=7
)
tagsClass_lbox = tkinter.Listbox(
    tag_options,
    listvariable=tkinter.StringVar(value=tagsClass_valuesList),
    selectmode="multiple",
    exportselection=False,
    relief="ridge",
    height=6,
    width=9
)
tagsSpec_lbox = tkinter.Listbox(
    tag_options,
    listvariable=tkinter.StringVar(value=tagsSpec_valuesList),
    selectmode="multiple",
    exportselection=False,
    relief="ridge",
    height=6,
    width=12
)
tagsQual_lbox.pack(side="left", anchor="nw", padx=(0, 10))
tagsPos_lbox.pack(side="left", anchor="nw", padx=(0, 10))
tagsClass_lbox.pack(side="left", anchor="nw", padx=(0, 10))
tagsSpec_lbox.pack(side="left", anchor="nw", padx=(0, 10))
# tag_options = ttk.Frame(operator_form)
# tag_options.grid(column=1, row=2, sticky="NSEW")
# tag_options.columnconfigure(0, weight=1)
# tag_options.rowconfigure(0, weight=0, minsize=20)
# tag_options.rowconfigure(1, weight=0, minsize=20)
# tag_options.rowconfigure(2, weight=0, minsize=20)
# tag_options.rowconfigure(3, weight=0, minsize=20)
# # configure_AutoRecruit_frame --> tag_options widgets
# tag_row0 = ttk.Frame(tag_options)
# tag_row0.grid(column=0, row=0, sticky="NW")
# tag_row0.columnconfigure(0, weight=1)
# tag_row0.rowconfigure(0, weight=1)
#
# tag_row1 = ttk.Frame(tag_options)
# tag_row1.grid(column=0, row=1, sticky="NW")
# tag_row1.columnconfigure(0, weight=1)
# tag_row1.rowconfigure(0, weight=1)
#
# tag_row2 = ttk.Frame(tag_options)
# tag_row2.grid(column=0, row=2, sticky="NW")
# tag_row2.columnconfigure(0, weight=1)
# tag_row2.rowconfigure(0, weight=1)
#
# tag_row3 = ttk.Frame(tag_options)
# tag_row3.grid(column=0, row=3, sticky="NW")
# tag_row3.columnconfigure(0, weight=1)
# tag_row3.rowconfigure(0, weight=1)
#
# ttk.Checkbutton(tag_row0, text="Robot").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row0, text="Starter").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row0, text="Senior Operator").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row0, text="Top Operator").pack(side="left", anchor="nw", ipadx=10)
#
# ttk.Checkbutton(tag_row1, text="Melee").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row1, text="Ranged").pack(side="left", anchor="nw", ipadx=10)
#
# ttk.Checkbutton(tag_row2, text="Caster").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row2, text="Defender").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row2, text="Guard").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row2, text="Medic").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row3, text="Sniper").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row3, text="Specialist").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row3, text="Supporter").pack(side="left", anchor="nw", ipadx=10)
# ttk.Checkbutton(tag_row3, text="Vanguard").pack(side="left", anchor="nw", ipadx=10)

ttk.Button(operator_form, text="Add to Database", command=lambda:insert_operator()).grid(column=0, row=3, sticky="NW")

def add_operator_tab():
    operator_form.grid(column=1, row=1, sticky="NSEW")

def database_tables_tab():
    operator_form.grid_forget()

database_menu = ttk.Frame(database_tools_frame)
database_menu.grid(column=0, row=1, sticky="NSEW")
ttk.Button(database_menu, text="Add Operator", command=lambda:add_operator_tab()).pack(side="top", anchor="nw")
ttk.Button(database_menu, text="Database Tables", command=lambda:database_tables_tab()).pack(side="top", anchor="nw")
ttk.Label(database_menu, text="Tags").pack(side="top", anchor="nw")


raise_frame(mainframe)
root.mainloop()
#
