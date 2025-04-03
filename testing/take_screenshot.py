import screen_capture_tools
import time


screenshot_name = "Recruitment Setup Screen"

scr = screen_capture_tools.SourceWindow("Arknights")
time.sleep(1)
img = scr.take_screenshot(save_screenshot=True, screenshot_name=screenshot_name)
