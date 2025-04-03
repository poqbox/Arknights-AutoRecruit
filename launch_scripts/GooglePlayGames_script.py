import subprocess
import time
import win32gui
import screen_capture_tools
import desktop_control as desktop


def launch(emulator_path, emulator_title, screen_resolution):
    # open emulator and bring to foreground
    scr_mdpt = (int(screen_resolution[0] / 2), int(screen_resolution[1] / 2))
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
