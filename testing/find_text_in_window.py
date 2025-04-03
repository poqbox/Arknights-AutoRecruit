import screen_capture_tools


find_text = "Recruit"
scr = screen_capture_tools.SourceWindow("Arknights")
scr.take_windowed_screenshot(screenshot_name="test")
scr.find_text_in_window(find_text, print_detected_text=False, show_window=True, bound_text=True)
scr.find_text_in_window(find_text, bound=((85, 325), (180, 385)), print_detected_text=True, show_window=True, bound_text=False)
