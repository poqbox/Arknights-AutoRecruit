import cv2
import os
import subprocess
import time
import win32gui
import tkinter
from tkinter import ttk
from tkinter import scrolledtext as tk_scrolledtext
import tkinter_ttk_tools as ttkTools
import desktop_control as desktop
import screen_capture_tools
import recruitment_database_tools as recruitTools

# tested on Windows 11
# pytesseract manual:  https://github.com/tesseract-ocr/tesseract/blob/main/doc/tesseract.1.asc
# Notable sections:
#   --psm N
# binding events in tkinter info: https://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-widget

overall_ver = "1.0.0"
recruit_ver = "Il Siracusano"
AutoRecruit_ver = overall_ver + ".[" + recruit_ver + "]"

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
        Arknights = screen_capture_tools.Tools("Arknights")
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




# path to Google Play Games
emulator_title = "Google Play Games beta"
emulator_path = r'C:\Program Files\Google\Play Games\Bootstrapper.exe'
emu_hdl = None
screen_res = (1920, 1080)
scr_mdpt = (int(screen_res[0] / 2), int(screen_res[1] / 2))
recruit_tools = recruitTools.tools()

def swap_frame_grids(old_frame: ttk.Frame, new_frame: ttk.Frame):
    """
    Only works with frames with grids
    """
    old_frame.grid_remove()
    new_frame.grid()

root = ttkTools.setup("Auto Recruit", window_size=(1024, 450), min_size=(400, 200))
ttkTools.configure_grid(root,
                        [
                            [0, None, None, None, 1]
                        ],
                        [
                            [0, None, None, None, 1]
                        ]
                        )
root_frame = ttkTools.frame_setup(root)
ttkTools.grid(root_frame, column=0, row=0, sticky="NSEW")
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

# home frame
home_frame = ttkTools.frame_setup(root_frame)
ttkTools.grid(home_frame, column=0, row=0, sticky="NSEW")
ttkTools.configure_grid(home_frame,
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

# database_tools frame
database_tools_frame = ttkTools.frame_setup(root_frame)
ttkTools.grid(database_tools_frame, column=0, row=0, sticky="NSEW")
ttkTools.configure_grid(database_tools_frame,
                        [
                            [0, 160, None, None, 0],
                            [1, 200, None, None, 1],
                            [2, 100, None, None, 0]
                        ],
                        [
                            [0, 50, None, None, 0],
                            [1, 340, None, None, 1]
                        ]
                        )
database_tools_frame.grid_remove()

# widgets for the frames
def home_frame_widgets():
    title = ttkTools.label_setup(home_frame, display_text="Arknights AutoRecruit", font=("Helvetica", 16, "bold"), text_padding=10)
    title.grid(column=0, row=0, sticky="NW")
    menu = ttkTools.frame_setup(home_frame)
    menu.grid(column=0, row=1, sticky="NSEW")
    ttkTools.configure_grid(menu,
                            [
                                [0, None, None, None, 1]
                            ],
                            [
                                [0, 30, None, None, 0],
                                [1, 30, None, None, 0]
                            ]
                            )
    recruit_button = ttkTools.button_setup(menu, display_text="Enter AutoRecruit", function=None)
    recruit_button.grid(column=0, row=0, sticky="NE")
    database_tools_button = ttkTools.button_setup(menu, display_text="Database Tools",
                                    function=lambda: swap_frame_grids(home_frame, database_tools_frame))
    database_tools_button.grid(column=0, row=1, sticky="NE")
    database_tools_button.bind("<ButtonPress>", lambda e: recruit_tools.open_db())
    setup_button = ttkTools.button_setup(home_frame, display_text="Setup", function=None)
    setup_button.grid(column=0, row=2, sticky="SE")

def database_tools_widgets():
    back_button = ttkTools.button_setup(database_tools_frame, display_text="Back",
                                        function=lambda: [swap_frame_grids(database_tools_frame, home_frame),
                                                          recruit_tools.calculate(),
                                                          recruit_tools.close_db()
                                                          ])
    back_button.grid(column=0, row=0, sticky="NW")




    # initial operator form setup --start--

    # frame containing the settings to add an operator to the database
    operator_form = ttk.Frame(database_tools_frame)
    operator_form.grid(column=2, row=1, sticky="NSEW")
    ttkTools.configure_grid(operator_form,
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
    name_entry = ttkTools.entry_setup(operator_form, saveTo_variable=nameVar)
    name_entry.grid(column=0, row=0, sticky="NW")
    # frame for packing tag options inside a gridded frame
    tag_options = ttkTools.frame_setup(operator_form)
    tag_options.grid(column=0, row=2, sticky="NSEW")
    tags_label = ttkTools.label_setup(tag_options, display_text="Tags")
    tags_label.pack(side="top", anchor="nw")
    tagsQual_lbox = ttkTools.listbox_setup(
        tag_options,
        list_variable=tkinter.StringVar(value=tagsQual_valuesList),
        select_mode="multiple",
        stay_selected_when_unfocused=True,
        backdrop="ridge",
        height=6,
        width=14
    )
    tagsPos_lbox = ttkTools.listbox_setup(
        tag_options,
        list_variable=tkinter.StringVar(value=tagsPos_valuesList),
        select_mode="multiple",
        stay_selected_when_unfocused=False,
        backdrop="ridge",
        height=6,
        width=7
    )
    tagsClass_lbox = ttkTools.listbox_setup(
        tag_options,
        list_variable=tkinter.StringVar(value=tagsClass_valuesList),
        select_mode="multiple",
        stay_selected_when_unfocused=False,
        backdrop="ridge",
        height=6,
        width=9
    )
    tagsSpec_lbox = ttkTools.listbox_setup(
        tag_options,
        list_variable=tkinter.StringVar(value=tagsSpec_valuesList),
        select_mode="multiple",
        stay_selected_when_unfocused=False,
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
    table_frame_1, scroll_canvas_1, operator_table = ttkTools.scrollbar_frame_setup(database_tools_frame,
                                                                                    sticky_scrollframe="NEW",
                                                                                    sticky_content="NSEW",
                                                                                    height=360, width=520)
    table_frame_1.grid(column=1, row=1)
    ttkTools.configure_grid(operator_table,
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
        operator_list = recruit_tools.select_all_from_Operators()

        # method for filling the operator form by selecting a row in the operator table
        def fill_operator_form_with_table_row(row, num_cols):
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
        table = [[ttk.Entry() for j in range(num_cols)] for i in range(num_rows)]
        for r in range(num_rows):
            operator_table.rowconfigure(r, weight=0)
            for c in range(num_cols):
                if c == 0:
                    table[r][c] = ttkTools.entry_setup(operator_table, width=5)
                if c == 1:
                    table[r][c] = ttkTools.entry_setup(operator_table, width=2, foreground="grey")
                if c == 2:
                    table[r][c] = ttkTools.entry_setup(operator_table, width=25)
                if c == 3:
                    table[r][c] = ttkTools.entry_setup(operator_table, width=28)
                table[r][c].grid(column=c, row=r)
                table[r][c].insert(0, operator_list[r][c])
                table[r][c].configure(state="readonly")
                table[r][c].bind("<FocusIn>", lambda event, row=r, num_cols=num_cols: fill_operator_form_with_table_row(row, num_cols))
        table_frame_1.update_idletasks()
        scroll_canvas_1.configure(scrollregion=scroll_canvas_1.bbox("all"))
    configure_operator_table()
    table_frame_1.grid_remove()

    # table of tag combinations
    table_frame_2 = tk_scrolledtext.ScrolledText(database_tools_frame, height=18)
    table_frame_2.grid(column=1, row=1, sticky="NEW")
    def configure_tag_combinations_table():
        tag_combinations_txt = [recruit_tools.non_dist_combos,
                                recruit_tools.r4_tag_combos_dist,
                                recruit_tools.r5_tag_combos_dist,
                                recruit_tools.r6_tag_combos_dist
                                ]
        for i, rarity_row in enumerate(tag_combinations_txt):
            if i == 0:
                table_frame_2.insert(tkinter.END, "rarity 3-4\n")
            else:
                table_frame_2.insert(tkinter.END, "\nrarity")
                table_frame_2.insert(tkinter.END, i+3)
                table_frame_2.insert(tkinter.END, "\n")
            for combo_count_row in rarity_row:
                for combo in combo_count_row:
                    table_frame_2.insert(tkinter.END, ",".join(combo) + "|")
                table_frame_2.insert(tkinter.END, "\n")
        table_frame_2.configure(state="disabled")
    configure_tag_combinations_table()
    table_frame_2.grid_remove()
    table_frame_1.grid()

    # method for swapping tables
    class table_tool:
        current_id = 0
        table_frame_id = {}
    table_control = table_tool
    table_control.current_id = 1
    table_control.table_frame_id[1] = table_frame_1
    table_control.table_frame_id[2] = table_frame_2

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
    button_display_frame = ttkTools.frame_setup(database_tools_frame)
    button_display_frame.grid(column=0, row=1, sticky="NSEW")
    operator_table_button = ttkTools.button_setup(button_display_frame, display_text="Operator Table", function=lambda: swap_table_frame_grids(1))
    operator_table_button.pack(side="top", anchor="nw")
    tag_combinations_table_button = ttkTools.button_setup(button_display_frame, display_text="Tag Combinations", function=lambda: swap_table_frame_grids(2))
    tag_combinations_table_button.pack(side="top", anchor="nw")
    recalculate_button = ttkTools.button_setup(button_display_frame, display_text="Recalculate\nTag Combinations", function=lambda: [recruit_tools.calculate(), configure_tables()])
    recalculate_button.pack(side="top", anchor="nw")
    def open_help_window():
        help_window = tkinter.Toplevel(root)
        help_window.title("Instructions")
        help_window.geometry("400x300")
        text1 = "Using the database"
        text2 = "Updating an operator:\n" \
                "        Requires name, tags\n" \
                "Adding a new operator:\n" \
                "        Requires name, rarity, tags\n" \
                "Deleting an operator:\n" \
                "        Requires operator ID"
        label1 = ttkTools.label_setup(help_window, display_text=text1, font=("Helvetica", 12, "bold"))
        label1.pack(side="top", anchor="nw")
        label2 = ttkTools.label_setup(help_window, display_text=text2)
        label2.pack(side="top", anchor="nw")
    help_button = ttkTools.button_setup(button_display_frame, display_text="Help", function=lambda: open_help_window(), width=4)
    help_button.pack(side="top", anchor="nw")
    version_label = ttkTools.label_setup(button_display_frame, display_text="ver. " + AutoRecruit_ver, font=("Courier", 8))
    version_label.configure(foreground="grey")
    version_label.pack(side="bottom", anchor="sw")




    # remaining operator form setup --start--

    def operator_form_widgets():
        # methods for implementing a default value in the name_entry widget
        def name_entry_setup():
            name_entry.configure(foreground="grey")
            name_entry.insert(0, "Operator Name")
        def name_entry_FocusIn():
            name = nameVar.get()
            if not name or name.lower() == "operator name":
                name_entry.configure(foreground="black")
                name_entry.delete(0, "end")
        def name_entry_FocusOut():
            name = nameVar.get()
            if not name or name.lower() == "operator name":
                name_entry.configure(foreground="grey")
                name_entry.delete(0, "end")
                name_entry.insert(0, "Operator Name")
        name_entry_setup()
        name_entry.bind("<FocusIn>", lambda e: name_entry_FocusIn())
        name_entry.bind("<FocusOut>", lambda e: name_entry_FocusOut())
        rarity_box = ttkTools.spinbox_setup(operator_form, 1, 6, saveTo_variable=rarityVar, width=4)
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
                    operator_data = recruit_tools.select_operator_by_id(operator_id)
                    if operator_data == None:
                        # error label
                        error_label = ttkTools.label_setup(delete_operator_window, display_text="Error: operator_id_" + operator_id + " not found")
                        error_label.pack(side="top")
                    else:
                        # warning label
                        warning_label = ttkTools.label_setup(delete_operator_window, display_text="Are you sure you want to delete the following operator:")
                        warning_label.pack(side="top")
                        # operator data
                        operator_data_str = "id:\t" + str(operator_data[0]) + "\nrarity:\t" + str(operator_data[1]) + "\nname:\t" + operator_data[2] + "\ntags:\t" + operator_data[3]
                        operator_data_label = ttkTools.label_setup(delete_operator_window, display_text=operator_data_str, width=200)
                        operator_data_label.pack(side="top")
                        confirm_button = ttkTools.button_setup(delete_operator_window, display_text="CONFIRM",
                                                               function=lambda: [recruit_tools.delete_operator(id=int(operator_id)), delete_operator_window.destroy(), delete_operator_window.update(), configure_tables()])
                        confirm_button.pack(side="top")
                    cancel_button = ttkTools.button_setup(delete_operator_window, display_text="CANCEL", function=lambda: [delete_operator_window.destroy(), delete_operator_window.update()])
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
                    if statement_type == "insert":
                        recruit_tools.insert_new_operator(operator_name=operator_name, rarity=rarity, tag_list=tags)
                nameVar.set("")
                rarityVar.set("")
                idVar.set("")
                tagsQual_lbox.selection_clear(0, "end")
                tagsPos_lbox.selection_clear(0, "end")
                tagsClass_lbox.selection_clear(0, "end")
                tagsSpec_lbox.selection_clear(0, "end")
                name_entry_setup()
                configure_tables()
        add_operator_button = ttkTools.button_setup(operator_form, display_text="Add to Database", function=lambda: update_recruit_db("insert"))
        add_operator_button.grid(column=0, row=3, sticky="NW")
        update_operator_button = ttkTools.button_setup(operator_form, display_text="Update Database", function=lambda: update_recruit_db("update"))
        update_operator_button.grid(column=0, row=4, sticky="NW")
        # undo_button = ttkTools.button_setup(operator_form, display_text="Undo", function=None, width=5)
        # undo_button.grid(column=0, row=5, sticky="NW")
        # delete operator options
        operator_id_entry = ttkTools.entry_setup(operator_form, saveTo_variable=idVar, width=6)
        operator_id_entry.grid(column=0, row=6, sticky="SE")
        delete_operator_button = ttkTools.button_setup(operator_form, display_text="Delete Operator", function=lambda: update_recruit_db("delete"))
        delete_operator_button.grid(column=0, row=7, sticky="SE")

    # remaining operator form setup --end--




    operator_form_widgets()

home_frame_widgets()
database_tools_widgets()
home_frame.grid()


root.mainloop()
