import screen_capture_tools


find_text = "START"
image_name = "Recruitment Label.png"
scr = screen_capture_tools.SourceWindow("Arknights")
scr.find_text_in_image(image_name, find_text, print_detected_text=True, show_image=True, bound_text=False)
