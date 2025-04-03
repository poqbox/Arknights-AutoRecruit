import screen_capture_tools


image_name = "Recruitment Label.png"
scr = screen_capture_tools.SourceWindow("Arknights")
scr.find_points_on_image(image_name)
