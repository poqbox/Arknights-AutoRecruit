import recruitment_database_tools
import screen_capture_tools
import time


scr = screen_capture_tools.SourceWindow("Arknights")
tag_positions_list = [[(563, 540), (778, 608)],
                      [(813, 540),  (1028, 608)],
                      [(1063, 540), (1278, 608)],
                      [(563, 648),  (778, 716)],
                      [(813, 648),  (1028, 716)]
                      ]
all_tags_list = recruitment_database_tools.tag_dict.values()
available_tags = []
time.sleep(2)
for pt1, pt2 in tag_positions_list:
    tag_recognized = False
    # tries to recognize the tag three times before returning and giving an error message
    for tries in range(3):
        img = scr.take_bounded_screenshot(pt1, pt2, save_screenshot=False)
        detected_text, img = scr.detect_text_in_image(img)
        for tag in all_tags_list:
            if tag in detected_text:
                if tag in available_tags:
                    print("Warning: recognized duplicate tag.\nContinuing with operation.")
                else:
                    available_tags.append(tag)
                tag_recognized = True
                break
        if tag_recognized:
            break
        time.sleep(1)
    if not tag_recognized:
        print("Error: Failed to recognize tag.")
        # break
        # return
print(available_tags)
