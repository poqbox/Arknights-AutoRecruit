import cv2
import os
import screen_capture_tools


# setup path for reading and deskewing images
directory = "Screenshots"
image_name = "Recruitment Label.png"

scr = screen_capture_tools.SourceWindow("Arknights")
file_dir = os.path.dirname(__file__)
file_dir = os.path.dirname(file_dir)
image_path = os.path.join(file_dir, directory, image_name)
image = cv2.imread(image_path)
pts1 = ((0, 0), (0, 55), (230, 70))
pts2 = ((0, 0), (0, 55), (235, 55))
scr.skew_image(image, image_pts=pts1, output_pts=pts2, save_image=True, file_name="Recruitment Label [skewed]")
