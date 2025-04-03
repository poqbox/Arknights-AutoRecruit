import desktop_control
import math
import screen_capture_tools
import time
from win32api import GetSystemMetrics

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
#   - UI Adaptation specifies the UI's distance from the left and right edges, in pixels
#   - Window sizes on Windows 11 seem to have 5 extra pixels on all sides
#   - Cannot find the "Recruit" button
#   - Can find the "Recruitment" label
#       - Cannot find it when full-screen and not deskewed
#       - Can find it when zoomed in on the label
#
# Testings:
#   - button positions were tested in 3440x1440 full-screen with a UI Adaptation of 0
#   - button stickiness/resizing was tested using the "UI Adaptation" setting, not with different window resolutions


scr_res = (GetSystemMetrics(0), GetSystemMetrics(1))
scr_mdpt = (int(scr_res[0] / 2), int(scr_res[1] / 2))
gcd = math.gcd(scr_res[0], scr_res[1])
aspect_ratio = (scr_res[0]/gcd, scr_res[1]/gcd)
scr_res_cmn = scr_res
if scr_res[1] == 1080:
    scr_res_cmn = (1920, scr_res[1])
elif scr_res[1] == 1440:
    scr_res_cmn = (2560, scr_res[1])
elif scr_res[1] == 2160:
    scr_res_cmn = (3840, scr_res[1])
gcd_res = (640, 360)
mult = (scr_res_cmn[0] / gcd_res[0], scr_res_cmn[1] / gcd_res[1])
rng = desktop_control.RandomNumberGenerator()


def __get_button_pos(gcd_pts, sticky: str="none"):
    """
    Takes a 2-tuple of points scaled to a specified resolution
    Scales the points to the current screen resolution
    (default: 640x360, i.e., 16:9 aspect ratio)
    """
    # Common screen widths: 1920, 2560, 3440, 3840      GCD: 640, excludes 3440
    # Common screen heights: 1080, 1440, 2160           GCD: 360
    # Widescreen monitors have additional black bars on the left and right sides (40px for 3440x1440)
    # gcd_pt = gcd_res * pt/scr_res, rounds to center
    x1 = math.ceil(gcd_pts[0][0] * mult[0])
    y1 = math.ceil(gcd_pts[0][1] * mult[1])
    x2 = math.floor(gcd_pts[1][0] * mult[0])
    y2 = math.floor(gcd_pts[1][1] * mult[1])
    if scr_res_cmn[0] != scr_res[0]:
        # diff_px is the difference in width to a resolution of the same height, but with 16:9 aspect ratio
        # bars_px is the width of the black bar that appears when the screen is too wide for the game
        diff_px = 0
        bars_px = 0
        if scr_res[0] == 3440:
            # 3440-2560
            diff_px = 880
            bars_px = 40
        if sticky is None or sticky.lower() == "none":
            x1 += diff_px/2
            x2 += diff_px/2
        elif sticky.lower() == "right":
            x1 += diff_px - bars_px
            x2 += diff_px - bars_px
        elif sticky.lower() == "left":
            x1 += bars_px
            x2 += bars_px
    return (x1, y1), (x2, y2)


def __get_stage_selection_tab_pos(tab):
    """
    Takes the name of a tab (i.e.: terminal, main theme, supplies, etc.)
    Like __get_button_pos() but specialized for the stage selection tabs
    """
    # all tabs shift towards center
    # all tabs resize when needed to fit within the window's aspect ratio
    if aspect_ratio == (16, 9):
        if tab == "terminal":
            # Screen resolution: 2560x1440, full-screen
            # UI Adp.=0:    l=0, r=292, t=1262, b=1440
            #               width=292
            gcd_pts = (0, 315.5), (73, 360)
        elif tab == "main theme":
            # Screen resolution: 2560x1440, full-screen
            # UI Adp.=0:    l=294, r=612, t=1262, b=1440
            #               width=318
            gcd_pts = (73.5, 315.5), (153, 360)
        elif tab == "supplies":
            # Screen resolution: 2560x1440, full-screen
            # UI Adp.=0:    l=1248, r=1566, t=1262, b=1440
            #               width=318
            gcd_pts = (312, 315.5), (391.5, 360)
        elif tab == "regular tasks":
            # Screen resolution: 2560x1440, full-screen
            # UI Adp.=0:    l=1568, r=1886, t=1262, b=1440
            #               width=318
            gcd_pts = (392, 315.5), (471.5, 360)
        x1 = math.ceil(gcd_pts[0][0] * mult[0])
        y1 = math.ceil(gcd_pts[0][1] * mult[1])
        x2 = math.floor(gcd_pts[1][0] * mult[0])
        y2 = math.floor(gcd_pts[1][1] * mult[1])
        return (x1, y1), (x2, y2)
    elif aspect_ratio == (21, 9):
        if tab == "terminal":
            # Screen resolution: 3440x1440, full-screen
            # UI Adp.=0:    l=70, r=426, t=1262, b=1440
            #               width=356
            gcd_pts = (13.1, 315.5), (79.2, 360)
        elif tab == "main theme":
            # Screen resolution: 3440x1440, full-screen
            # UI Adp.=0:    l=484, r=842, t=1262, b=1440
            # UI Adp.=60:   l=522, r=880
            # UI Adp.=120:  l=560, r=918
            #               width=358
            gcd_pts = (90.1, 315.5), (156.6, 360)
        elif tab == "supplies":
            # Screen resolution: 3440x1440, full-screen
            # UI Adp.=0:    l=1738, r=2108, t=1262, b=1440
            #               width=370
            gcd_pts = (323.4, 315.5), (392.1, 360)
        elif tab == "regular tasks":
            # Screen resolution: 3440x1440, full-screen
            # UI Adp.=0:    l=2158, r=2528, t=1262, b=1440
            #               width=370
            gcd_pts = (401.5, 315.5), (470.3, 360)
        x1 = math.ceil(gcd_pts[0][0] * 5.375)
        y1 = math.ceil(gcd_pts[0][1] * mult[1])
        x2 = math.floor(gcd_pts[1][0] * 5.375)
        y2 = math.floor(gcd_pts[1][1] * mult[1])
        return (x1, y1), (x2, y2)


def delayed_click(bounding_box):
    time.sleep(rng.click_delay_sample())
    x, y = rng.xy_normal_distribution_sample(bounding_box)
    desktop_control.click(x, y)


# l = left bound
# r = right bound
# t = top bound
# b = bottom bound

def click_startup_button():
    """Clicks the "START" button that appears on the title screen, before entering the home screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=1506, r=1914, t=950, b=1085
    # no sticky
    # no resize
    gcd_pts = (266.5, 237.5), (368.5, 271.25)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))


def click_back_button():
    """
    Shown on most screens.
    Not shown on: home screen
    """
    # Screen resolution: 3440x1440, full-screen
    # l=74, r=362, t=25, b=125
    # left sticky
    # no resize
    gcd_pts = (8.5, 6.25), (80.5, 31.25)
    delayed_click(__get_button_pos(gcd_pts, sticky="left"))


def to_terminal_from_home_screen():
    """
    Located on the home screen.
    Avoids the sanity box, orundum button, and event button.
    """
    # Screen resolution: 3440x1440, full-screen
    # l=2429, r=2780, t=214, b=556
    # right sticky
    # no resize
    gcd_pts = (397.25, 53.5), (485, 139)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def to_recruit_from_home_screen():
    """Located on the home screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=2520, r=2846, t=974, b=1092
    # right sticky
    # no resize
    gcd_pts = (420, 243.5), (501.5, 273)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def click_recruitment_slot(slot_num: int):
    """Located on the recruit screen."""
    # Screen resolution: 3440x1440, full-screen
    # slot 1: l=476, r=1698, t=366, b=858
    # slot 2: l=1738, r=2960, t=366, b=858
    # slot 3: l=476, r=1698, t=920, b=1412
    # slot 4: l=1738, r=2960, t=920, b=1412
    # no sticky
    # no resize
    if slot_num == 1:
        gcd_pts = (9, 91.5), (314.5, 214.5)
    if slot_num == 2:
        gcd_pts = (324.5, 91.5), (630, 214.5)
    if slot_num == 3:
        gcd_pts = (9, 230), (314.5, 353)
    if slot_num == 4:
        gcd_pts = (324.5, 230), (630, 353)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def click_hour_up():
    """Located on the recruitment slot screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=1200, r=1490, t=251, b=347
    # no sticky
    # no resize
    gcd_pts = (190, 62.75), (262.5, 86.75)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def click_hour_down():
    """Located on the recruitment slot screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=1196, r=1483, t=546, b=642
    # no sticky
    # no resize
    gcd_pts = (189, 136.5), (260.75, 160.5)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def click_minute_up():
    """Located on the recruitment slot screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=1530, r=1820, t=251, b=347
    # no sticky
    # no resize
    gcd_pts = (272.5, 62.75), (345, 86.75)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def click_minute_down():
    """Located on the recruitment slot screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=1524, r=1813, t=546, b=642
    # no sticky
    # no resize
    gcd_pts = (271, 136.5), (343.25, 160.5)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def click_tag(tag_num: int):
    """
    Located on the recruitment slot screen.
    Numbered left-to-right, then down.
    """
    # Screen resolution: 3440x1440, full-screen
    # tag 1: l=1190, r=1478, t=720, b=812
    # tag 2: l=1524, r=1812, t=720, b=812
    # tag 3: l=1858, r=2146, t=720, b=812
    # tag 4: l=1190, r=1478, t=863, b=955
    # tag 5: l=1524, r=1812, t=863, b=955
    # no sticky
    # no resize
    if tag_num == 1:
        gcd_pts = (187.5, 180), (259.5, 203)
    if tag_num == 2:
        gcd_pts = (271, 180), (343, 203)
    if tag_num == 3:
        gcd_pts = (354.5, 180), (426.5, 203)
    if tag_num == 4:
        gcd_pts = (187.5, 215.75), (259.5, 238.75)
    if tag_num == 5:
        gcd_pts = (271, 215.75), (343, 238.75)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def click_refresh_tags():
    """
    Located on the recruitment slot screen.
    Requires confirmation.
    """
    # Screen resolution: 3440x1440, full-screen
    # l=2312, r=2444, t=746, b=877
    # no sticky
    # no resize
    gcd_pts = (468, 186.5), (501, 219.25)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def refresh_tags_confirmation():
    click_right_confirmation()

def start_recruitment():
    """Located on the recruitment slot screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=2220, r=2580, t=1114, b=1212
    # no sticky
    # no resize
    gcd_pts = (445, 278.5), (535, 303)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def exit_recruitment_slot_screen():
    """Located on the recruitment slot screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=2214, r=2580, t=1244, b=1342
    # no sticky
    # no resize
    gcd_pts = (443.5, 311), (535, 335.5)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def stop_recruitment(slot_num: int):
    """
    Located on the recruit screen.
    Appears during an ongoing recruitment.
    Requires confirmation.
    """
    # Screen resolution: 3440x1440, full-screen
    # slot 1: l=515, r=1078, t=698, b=820
    # slot 2: l=1777, r=2340, t=698, b=820
    # slot 3: l=515, r=1078, t=1253, b=1375
    # slot 4: l=1777, r=2340, t=1253, b=1375
    # no sticky
    # no resize
    if slot_num == 1:
        gcd_pts = (18.75, 174.5), (159.5, 205)
    if slot_num == 2:
        gcd_pts = (334.25, 174.5), (475, 205)
    if slot_num == 3:
        gcd_pts = (18.75, 313.25), (159.5, 343.75)
    if slot_num == 4:
        gcd_pts = (334.25, 313.25), (475, 343.75)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def use_expedited_plan(slot_num: int):
    """
    Located on the recruit screen.
    Appears during an ongoing recruitment.
    Requires confirmation.
    """
    # Screen resolution: 3440x1440, full-screen
    # slot 1: l=1107, r=1667, t=698, b=820
    # slot 2: l=2369, r=2929, t=698, b=820
    # slot 3: l=1107, r=1667, t=1253, b=1375
    # slot 4: l=2369, r=2929, t=1253, b=1375
    # no sticky
    # no resize
    if slot_num == 1:
        gcd_pts = (166.75, 174.5), (306.75, 205)
    if slot_num == 2:
        gcd_pts = (482.25, 174.5), (622.25, 205)
    if slot_num == 3:
        gcd_pts = (166.75, 313.25), (306.75, 343.75)
    if slot_num == 4:
        gcd_pts = (482.25, 313.25), (622.25, 343.75)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))

def stop_recruitment_confirmation():
    click_left_confirmation()

def use_expedited_plan_confirmation():
    click_right_confirmation()

def click_hire_button(slot_num: int):
    """
    Located on the recruit screen.
    Appears after the recruitment completes.
    """
    # Screen resolution: 3440x1440, full-screen
    # slot 1: l=504, r=1676, t=702, b=822
    # slot 2: l=1765, r=2938, t=702, b=822
    # slot 3: l=504, r=1676, t=1257, b=1377
    # slot 4: l=1765, r=2938, t=1257, b=1377
    # no sticky
    # no resize
    if slot_num == 1:
        gcd_pts = (16, 175.5), (309, 205.5)
    if slot_num == 2:
        gcd_pts = (331.25, 175.5), (624.5, 205.5)
    if slot_num == 3:
        gcd_pts = (16, 314.25), (309, 344.25)
    if slot_num == 4:
        gcd_pts = (331.25, 314.25), (624.5, 344.25)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))


def to_store_from_home_screen():
    """Located on the home screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=2129, r=2505, t=861, b=1068
    # right sticky
    # no resize
    gcd_pts = (322.25, 215.25), (416.25, 267)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def to_missions_from_home_screen():
    """Located on the home screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=2038, r=2460, t=1136, b=1306
    # right sticky
    # no resize
    gcd_pts = (299.5, 284), (405, 326.5)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def to_base_from_home_screen():
    """Located on the home screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=2495, r=2970, t=1182, b=1366
    # right sticky
    # no resize
    gcd_pts = (413.75, 295.5), (532.5, 341.5)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def click_stage_auto_deploy_button():
    """Tailored to stages: story, supplies"""
    # Screen resolution: 3440x1440, full-screen
    # l=2928, r=3326, t=1170, b=1252
    # right sticky
    # no resize
    gcd_pts = (522, 292.5), (621.5, 313)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def click_stage_repeat_button(repeat_num: int=1):
    """
    Appears when enabling Auto Deploy.
    Available for stages: story, supplies
    """
    # Screen resolution: 3440x1440, full-screen
    # l=2742, r=2926, t=1174, b=1248
    # x1: l=2760, r=2916, t=1007, b=1226
    # x2: l=2760, r=2916, t=884, b=1002
    # x3: l=2760, r=2916, t=761, b=879
    # x4: l=2760, r=2916, t=637, b=756
    # x5: l=2760, r=2916, t=514, b=632
    # x6: l=2760, r=2916, t=387, b=509
    # right sticky
    # no resize
    gcd_pts = (475.5, 293.5), (521.5, 312)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))
    if repeat_num <= 1:
        gcd_pts = (480, 251.75), (519, 306.5)
    elif repeat_num == 2:
        gcd_pts = (480, 221), (519, 250.5)
    elif repeat_num == 3:
        gcd_pts = (480, 190.25), (519, 219.75)
    elif repeat_num == 4:
        gcd_pts = (480, 159.25), (519, 189)
    elif repeat_num == 5:
        gcd_pts = (480, 128.5), (519, 158)
    elif repeat_num >= 6:
        gcd_pts = (480, 96.75), (519, 127.25)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def click_stage_start_button():
    """
    Opens the roster screen.
    Tailored to stages: story, supplies
    """
    # Screen resolution: 3440x1440, full-screen
    # l=2914, r=3326, t=1279, b=1404
    # right sticky
    # no resize
    gcd_pts = (518.5, 319.75), (621.5, 351)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def click_mission_start_button():
    """
    This is the start button on the roster screen.
    Path: stage > stage-start button
    """
    # Screen resolution: 3440x1440, full-screen
    # l=2510, r=2780, t=732, b=1290
    # no sticky
    # no resize
    gcd_pts = (517.5, 183), (585, 322.5)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))


def to_terminal_via_tab():
    """Located on the stage-selection screen."""
    delayed_click(__get_stage_selection_tab_pos(tab="terminal"))


def to_main_theme_via_tab():
    """
    Located on the stage-selection screen.
    a.k.a. story stages
    """
    delayed_click(__get_stage_selection_tab_pos(tab="main theme"))


def to_previous_act():
    """
    Located on the Main Theme tab, where story episodes are grouped into acts.
    Clicks on the Act above the current one.
    Path: terminal > main theme
    """
    # Screen resolution: 3440x1440, full-screen
    # l=42, r=804, t=162, b=380
    # left sticky
    # no resize
    gcd_pts = (0.5, 40.5), (191, 95)
    delayed_click(__get_button_pos(gcd_pts, sticky="left"))


def to_following_act():
    """
    Located on the Main Theme tab, where story episodes are grouped into acts.
    Clicks on the Act below the current one.
    Path: terminal > main theme
    """
    # Screen resolution: 3440x1440, full-screen
    # l=42, r=804, t=1046, b=1260
    # left sticky
    # no resize
    gcd_pts = (0.5, 261.5), (191, 315)
    delayed_click(__get_button_pos(gcd_pts, sticky="left"))


def to_episode():
    """
    Located on the Main Theme tab, where story stages are grouped into episodes.
    Clicks on the episode button that is in-focus.
    Path: terminal > main theme
    """
    # Screen resolution: 3440x1440, full-screen
    # l=1988, r=2693, t=348, b=1052
    # no sticky
    # no resize
    gcd_pts = (387, 87), (563.25, 263)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))


def to_previous_episode():
    """
    Located on the episode stage-selection screen.
    Clicks on the button at the bottom-right.
    Path: terminal > main theme > episode
    """
    # Screen resolution: 3440x1440, full-screen
    # l=2738, r=2864, t=1248, b=1408
    # right sticky
    # no resize
    gcd_pts = (474.5, 312), (506, 352)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def to_following_episode():
    """
    Located on the episode stage-selection screen.
    Clicks on the button at the bottom-right.
    Path: terminal > main theme > episode
    """
    # Screen resolution: 3440x1440, full-screen
    # l=3146, r=3273, t=1248, b=1408
    # right sticky
    # no resize
    gcd_pts = (576.5, 312), (608.25, 352)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def to_supplies_via_tab():
    """Located on the stage-selection screen."""
    delayed_click(__get_stage_selection_tab_pos(tab="supplies"))


def to_regular_tasks_via_tab():
    """Located on the stage-selection screen."""
    delayed_click(__get_stage_selection_tab_pos(tab="regular tasks"))


def to_annihilation_stages():
    """Path: terminal > regular tasks"""
    # Screen resolution: 3440x1440, full-screen
    # l=1346, r=2006, t=1107, b=1206
    # center sticky
    # no resize
    gcd_pts = (126.5, 276.75), (291.5, 301.5)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def to_annihilation_rotation_stage():
    """Path: terminal > regular tasks"""
    # Screen resolution: 3440x1440, full-screen
    # l=1329, r=2021, t=820, b=1011
    # center sticky
    # no resize
    gcd_pts = (122.25, 205), (295.25, 252.75)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def click_annihilation_stage_auto_deploy_button():
    """No stage repeat button for annihilation stages."""
    # Screen resolution: 3440x1440, full-screen
    # l=2928, r=3326, t=1144, b=1226
    # right sticky
    # no resize
    gcd_pts = (522, 286), (621.5, 306.5)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def click_annihilation_stage_start_button():
    """Button position is slightly different from the standard stage-start button."""
    # Screen resolution: 3440x1440, full-screen
    # l=2914, r=3326, t=1248, b=1373
    # right sticky
    # no resize
    gcd_pts = (518.5, 312), (621.5, 343.25)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def to_credit_store_via_tab():
    """Path: home screen > store"""
    # Screen resolution: 3440x1440, full-screen
    # l=2634, r=2998, t=173, b=253
    # center sticky
    # POTENTIALLY resizes towards center on smaller aspect ratios
    gcd_pts = (548.5, 43.25), (639.5, 63.25)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))


def claim_daily_credit():
    """
    Clicks the 'Claim' button on the credit store screen.
    Path: store > credit store
    """
    # Screen resolution: 3440x1440, full-screen
    # l=2771, r=2986, t=53, b=105
    # right sticky
    # no resize
    gcd_pts = (482.75, 13.25), (536.5, 26.25)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def click_skip_recruitment():
    """Clicks the 'Skip' button on the bag-opening screen when recruiting operators."""
    # Screen resolution: 3440x1440, full-screen
    # l=3188, r=3376, t=20, b=155
    # right sticky
    # no resize
    gcd_pts = (587, 5), (634, 38.75)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def to_daily_missions_via_tab():
    """Path: home screen > missions"""
    # Screen resolution: 3440x1440, full-screen
    # l=1360, r=1878, t=22, b=126
    # no sticky
    # no resize
    gcd_pts = (230, 5.5), (359.5, 31.5)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))


def to_weekly_missions_via_tab():
    """Path: home screen > missions"""
    # Screen resolution: 3440x1440, full-screen
    # l=1900, r=2418, t=22, b=126
    # no sticky
    # no resize
    gcd_pts = (365, 5.5), (494.5, 31.5)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))


def collect_all_mission_rewards():
    """
    Clicks the 'Collect All' button on the missions screen.
    Path: mission > daily missions/weekly missions
    """
    # Screen resolution: 3440x1440, full-screen
    # l=2418, r=2936, t=204, b=240
    # no sticky
    # no resize
    gcd_pts = (494.5, 51), (624, 60)
    delayed_click(__get_button_pos(gcd_pts, sticky=None))


def click_base_notification_button(side="top"):
    """
    Appears in the base screen when base resources can be obtained.
    The button shifts downwards when the emergency button appears.
    """
    # Screen resolution: 3440x1440, full-screen
    # top position: l=3188, r=3397, t=144, b=228
    # bottom position: l=3188, r=3397, t=241, b=325
    # right sticky
    # no resize
    if side.lower() == "bottom":
        gcd_pts = (587, 60.25), (639.25, 81.25)
    else:
        gcd_pts = (587, 36), (639.25, 57)
    delayed_click(__get_button_pos(gcd_pts, sticky="right"))


def collect_base_resources_via_resource_bar():
    """
    Appears after clicking the base notification button.
    Claims the left-most resource.
    """
    # Screen resolution: 3440x1440, full-screen
    # l=368, r=662, t=1307, b=1412
    # left sticky
    # no resize
    gcd_pts = (82, 326.75), (155.5, 353)
    delayed_click(__get_button_pos(gcd_pts, sticky="left"))


def click_right_confirmation():
    """Clicks the right button of a confirmation message."""
    # Screen resolution: 3440x1440, full-screen
    # l=1740, r=3398, t=910, b=1066
    # left side = no sticky, right side = right sticky
    gcd_pts = (325, 227.5), (639.5, 266.5)
    x1 = math.ceil(gcd_pts[0][0] * mult[0])
    y1 = math.ceil(gcd_pts[0][1] * mult[1])
    x2 = math.floor(gcd_pts[1][0] * mult[0])
    y2 = math.floor(gcd_pts[1][1] * mult[1])
    if scr_res_cmn[0] != scr_res[0]:
        diff_px = 0
        bars_px = 0
        if scr_res[0] == 3440:
            # 3440-2560
            diff_px = 880
            bars_px = 40
        x1 += diff_px / 2
        x2 += diff_px - bars_px
    delayed_click(((x1, y1), (x2, y2)))


def click_left_confirmation():
    """Clicks the left button of a confirmation message."""
    # Screen resolution: 3440x1440, full-screen
    # l=40, r=1720, t=910, b=1066
    # left side = left sticky, right side = no sticky
    gcd_pts = (0, 227.5), (320, 266.5)
    x1 = math.ceil(gcd_pts[0][0] * mult[0])
    y1 = math.ceil(gcd_pts[0][1] * mult[1])
    x2 = math.floor(gcd_pts[1][0] * mult[0])
    y2 = math.floor(gcd_pts[1][1] * mult[1])
    if scr_res_cmn[0] != scr_res[0]:
        diff_px = 0
        bars_px = 0
        if scr_res[0] == 3440:
            # 3440-2560
            diff_px = 880
            bars_px = 40
        x1 += bars_px
        x2 += diff_px / 2
    delayed_click(((x1, y1), (x2, y2)))


def leave_base_confirmation():
    """Appears when leaving the base, if "Exiting Base Notification" is enabled in the game settings."""
    click_right_confirmation()


def exit_game_confirmation():
    """Appears when pressing the ESC key from the home screen."""
    click_right_confirmation()


def get_screen_location():
    search_box = click_startup_button()
    if screen_capture_tools.find_text("START", bound=search_box) == "START":
        return "startup"
    if screen_capture_tools.find_text("Recruit", bound=search_box) == "Recruit":
        return "home"
    if screen_capture_tools.find_text("Terminal", bound=search_box) == "Terminal":
        return "terminal"
    if screen_capture_tools.find_text("Main Theme", bound=search_box) == "Main Theme":
        return "main theme"
    if screen_capture_tools.find_text("Supplies", bound=search_box) == "Supplies":
        return "supplies"
    if screen_capture_tools.find_text("Regular Tasks", bound=search_box) == "Regular Tasks":
        return "regular tasks"
    if screen_capture_tools.find_text("Start", bound=search_box) == "Start":
        return "stage details"
    if screen_capture_tools.find_text("MISSION START", bound=search_box) == "MISSION START":
        return "roster screen"
    if screen_capture_tools.find_text("Credit Store", bound=search_box) == "Credit Store":
        return "credit store"
    if screen_capture_tools.find_text("Daily Missions", bound=search_box) == "Daily Missions":
        return "daily missions"
    if screen_capture_tools.find_text("Weekly Missions", bound=search_box) == "Weekly Missions":
        return "weekly missions"


def get_sanity_count_from_home_screen():
    """Located on the home screen."""
    # Screen resolution: 3440x1440, full-screen
    # l=2136, r=2426, t=270, b=434
    # right sticky
    # no resize
    gcd_pts = (324, 67.5), (396.5, 108.5)
    screen_capture_tools.detect_text(__get_button_pos(gcd_pts))


def get_sanity_count_from_stage_details():
    """Appears when viewing any stage details."""
    # Screen resolution: 3440x1440, full-screen
    # l=3104, r=3194, t=56, b=108
    # right sticky
    # no resize
    gcd_pts = (324, 67.5), (396.5, 108.5)
    screen_capture_tools.detect_text(__get_button_pos(gcd_pts))


def get_recruitment_tag_refresh_num():
    """
    Located on the recruitment screen and the recruitment slot screen.
    Path: home screen > recruit
    """
    # Screen resolution: 3440x1440, full-screen
    # l=2696, r=2724, t=148, b=188
    # right sticky
    # no resize
    gcd_pts = (464, 37), (471, 47)
    screen_capture_tools.detect_text(__get_button_pos(gcd_pts))


def get_store_credit_num():
    """
    Located on the credit store screen.
    Path: home screen > store > credit store
    """
    # Screen resolution: 3440x1440, full-screen
    # l=3134, r=3240, t=52, b=104
    # right sticky
    # no resize
    gcd_pts = (573.5, 13), (600, 26)
    screen_capture_tools.detect_text(__get_button_pos(gcd_pts))
