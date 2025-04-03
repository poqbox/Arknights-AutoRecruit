import screen_capture_tools


min_search_pt = (3112, 50)
max_search_pt = (3298, 112)
search_w = 240

emu = screen_capture_tools.SourceWindow("Arknights")
pt1, pt2 = emu.get_window_position()
emu.draw_rectangle_on_window((min_search_pt[0] + pt1[0], min_search_pt[1] + pt1[1]), (min_search_pt[0] + search_w + pt1[0], max_search_pt[1] + pt1[1]))
