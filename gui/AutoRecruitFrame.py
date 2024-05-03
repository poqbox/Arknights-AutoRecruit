import AutoRecruit
import config.config as config
import screen_capture_tools
import tkinter_tools as tkTools
import tkinter
from tkinter import font
from tkinter import scrolledtext
from tkinter import ttk


class AutoRecruitFrame(tkTools.Frame):
    def __init__(self, parent, root):
        super().__init__(root.frame)
        self.parent = parent
        self.root = root
        self.grid_configure(column=0, row=0, sticky="NSEW")
        self.grid_setup()
        self.widgets()

    def grid_setup(self):
        tkTools.grid_setup(self,
                           [
                                [0, 134, None, None, 0],
                                [1, 400, None, None, 1],
                                [2, 200, None, None, 0]
                            ],
                           [
                                [0, 50, None, None, 0],
                                [1, 340, None, None, 1]
                            ]
                           )
        self.grid_remove()

    def widgets(self):
        back_button = tkTools.Button(self, display_text="Back", function_when_clicked=tkTools.swap_frame(self, self.parent))
        back_button.grid(column=0, row=0, sticky="NW")

        # output textbox
        output_textbox = scrolledtext.ScrolledText(self, height=18)
        output_textbox.grid(column=1, row=1, sticky="NEW")
        output_text_font = font.nametofont(output_textbox.cget("font"))
        output_textbox.tag_configure("indent", lmargin1=output_text_font.measure("    "), lmargin2=output_text_font.measure("    "))
        output_textbox.configure(state="disabled")
        def output_text(text):
            output_textbox.configure(state="normal")
            output_textbox.insert("end", text)
            output_textbox.configure(state="disabled")
        def output_indented_text(text):
            output_textbox.configure(state="normal")
            output_textbox.insert("end", text, "indent")
            output_textbox.configure(state="disabled")

        # frame for packing buttons
        button_display_frame = tkTools.Frame(self)
        button_display_frame.grid(column=0, row=1, sticky="NSEW")
        get_window_titles_button = tkTools.Button(button_display_frame, display_text="Get opened\nwindow titles",
                                                  function_when_clicked=lambda: [output_text("Window titles:\n"),
                                                                                  output_indented_text(screen_capture_tools.get_window_titles()),
                                                                                  output_text("\n")])
        get_window_titles_button.pack(side="top", anchor="nw")
        def open_help_window():
            help_window = tkTools.SubWindow(self.root, title="Instructions", window_size=(600, 400), background_color="white")
            # Text for [Using AutoRecruit]
            label1 = tkTools.Label(help_window, display_text="Using AutoRecruit", font=("Helvetica", 12, "bold"), background_color="white")
            label1.pack(side="top", anchor="nw", fill="x")
            help_textbox1 = tkTools.Text(help_window, wrap_on="word", font=("Segoe UI", 9), backdrop="flat", height=6)
            help_textbox1.pack(side="top", anchor="nw", fill="x")
            text1 = "To get the emulator's path, right click on the application and select [Copy as path].\n" \
                    "To get the emulator's window title, try using the [Get opened window titles] button.\n" \
                    "This button will output a list of presently open window titles, separated by curly brackets. " \
                    "If the emulator is open, it's title will appear in the output box.\n" \
                    "If the emulator is open, it's window title will appear in the output box.\n"
            help_textbox1.insert("end", text1)
            help_textbox1.configure(state="disabled")
            # Text for [Setup]
            label2 = tkTools.Label(help_window, display_text="Setup", font=("Helvetica", 12, "bold"), background_color="white")
            label2.pack(side="top", anchor="nw", fill="x")
            help_textbox2 = tkTools.Text(help_window, wrap_on="word", backdrop="flat", height=10)
            help_textbox2.pack(side="top", anchor="nw", fill="x")
            help_text_font2 = font.nametofont(help_textbox2.cget("font"))
            help_textbox2.tag_configure("indent", lmargin1=help_text_font2.measure("  "), lmargin2=help_text_font2.measure("  "))
            text2_1h = "[Recruitment permits]\n"
            text2_1p = "The number of recruitment permits to be used by AutoRecruit.\n"
            text2_2h = "[Priority Tags]\n"
            text2_2p = "Determines the tag combinations that AutoRecruit will prioritize (top-to-bottom).\n" \
                       "Drag and drop to reorder the list, use the swap button to add/remove priorities."\
                       "If no matching tags are found, AutoRecruit will recruit with no tags selected at the specified recruit time.\n"
            text2_3h = "[Expedited Plans]\n"
            text2_3p = "If checked, AutoRecruit will use expedited plans.\n"
            text2_4h = "[Save]\n"
            text2_4p = "Saves the current configuration.\n"
            text2_5h = "[Start]\n"
            text2_5p = "Starts AutoRecruit. It will continue to run until the specified number of recruitment permits have been used.\n"
            text2_6h = "[Force Stop]\n"
            text2_6p = "Stops AutoRecruit from running any further. Closing the application will also stop AutoRecruit."
            help_textbox2.insert("end", text2_1h)
            help_textbox2.insert("end", text2_1p, "indent")
            help_textbox2.insert("end", text2_2h)
            help_textbox2.insert("end", text2_2p, "indent")
            help_textbox2.insert("end", text2_3h)
            help_textbox2.insert("end", text2_3p, "indent")
            help_textbox2.insert("end", text2_4h)
            help_textbox2.insert("end", text2_4p, "indent")
            help_textbox2.insert("end", text2_5h)
            help_textbox2.insert("end", text2_5p, "indent")
            help_textbox2.insert("end", text2_6h)
            help_textbox2.insert("end", text2_6p, "indent")
            help_textbox2.configure(font=("Segoe UI", 9))
            help_textbox2.configure(state="disabled")
        help_button = tkTools.Button(button_display_frame, display_text="Help", function_when_clicked=lambda: open_help_window(), width=4)
        help_button.pack(side="top", anchor="nw")




        # settings frame setup --start--
        # frame containing the setup for AutoRecruit
        settings_frame = tkTools.Frame(self)
        settings_frame.grid(column=2, row=1, sticky="NSEW")
        profile = config.Profile(config.get_last_used_profile())
        skip_emulator_launch_Var = tkinter.BooleanVar()
        use_expedited_plans_Var = tkinter.BooleanVar()
        prep_recruitments_Var = tkinter.BooleanVar()
        operators_list = self.root.database.get_operator_data(get=["name"], sort_order=[["name", "asc"]], reduce_nested_lists=True)
        priority_list = profile.get_profile_option("priority_list").split("|")
        priority_extras_list = ["6-star", "5-star", "4-star"]
        priority_extras_list.extend(operators_list)
        priority_extras_list = [item for item in priority_extras_list if item not in priority_list]
        recruitment_times_list = []
        for hours in range(1, 10):
            if hours < 10:
                hours = f"0{hours}"
            for minutes in range(0, 60, 10):
                if minutes < 10:
                    minutes = f"0{minutes}"
                recruitment_times_list.append(f"{hours}:{minutes}")
                if hours == f"09":
                    break
        profile_entry = tkTools.Entry(settings_frame, width=16)
        profile_entry.pack(side="top", anchor="nw")
        profile_entry.insert(0, profile.profile)
        emulator_path_entry = tkTools.Entry(settings_frame, width=32)
        emulator_path_entry.pack(side="top", anchor="nw")
        emulator_path_entry.insert(0, profile.get_profile_option("emulator_path"))
        emulator_title_entry = tkTools.Entry(settings_frame, width=32)
        emulator_title_entry.pack(side="top", anchor="nw")
        emulator_title_entry.insert(0, profile.get_profile_option("emulator_title"))
        skip_emulator_checkbutton = tkTools.Checkbutton(settings_frame, display_text="Start from Arknights home screen", saveValueTo_variable=skip_emulator_launch_Var)
        skip_emulator_checkbutton.pack(side="top", anchor="nw")
        # frame for recruitment_permits widgets --start--
        recruitment_permits_frame = tkTools.Frame(settings_frame)
        recruitment_permits_frame.pack(side="top", anchor="nw")
        recruitment_permits_label = tkTools.Label(recruitment_permits_frame, display_text="Recruitment Permits:", text_alignment="left", width=20)
        recruitment_permits_label.pack(side="left", anchor="nw")
        recruitment_permits_entry = tkTools.Entry(recruitment_permits_frame, width=6)
        recruitment_permits_entry.pack(side="left", anchor="nw")
        recruitment_permits_entry.insert(0, profile.get_profile_option("permits_num"))
        # frame for recruitment_permits widgets --end--


        # frame for ordering tag priorities --start--
        priority_tags_frame = tkTools.Frame(settings_frame)
        priority_tags_frame.pack(side="top", anchor="nw")
        tkTools.grid_setup(priority_tags_frame,
                           [
                                [0, None, None, None, None],
                                [1, None, None, None, None],
                                [2, None, None, None, None],
                                [3, None, None, None, None],
                                [4, None, None, None, None]
                            ],
                           [
                                [0, None, None, None, None],
                                [1, None, None, None, None]
                            ]
                           )
        priority_label = tkTools.Label(priority_tags_frame, display_text="Priority Tags")
        priority_label.grid(column=0, row=0, columnspan=3, sticky="NW")
        priority_listbox = tkTools.Listbox_with_drag_drop(
            priority_tags_frame,
            list_variable=tkinter.StringVar(value=priority_list),
            select_mode="multiple",
            stay_selected_when_unfocused=True,
            backdrop="ridge",
            height=6,
            width=14
        )
        priority_listbox.grid(column=0, row=1, rowspan=4)
        priority_extras_listbox = tkTools.Listbox(
            priority_tags_frame,
            list_variable=tkinter.StringVar(value=priority_extras_list),
            select_mode="multiple",
            stay_selected_when_unfocused=True,
            backdrop="ridge",
            height=6,
            width=14
        )
        priority_extras_listbox.grid(column=2, row=1, rowspan=4)
        def add_remove_priority():
            selected_list = []
            while priority_listbox.curselection():
                i = priority_listbox.curselection()[0]
                selected_list.insert(0, priority_listbox.get(i))
                priority_listbox.delete(i)
            for item in selected_list:
                if item in operators_list:
                    listbox_list = priority_extras_listbox.get(0, "end")
                    i = operators_list.index(item)
                    # if i == 0:
                    #     i += 1
                    #     next_operator = operators_list[i]
                    #     while next_operator not in listbox_list:
                    #         i += 1
                    #         next_operator = operators_list[i]
                    #     i = listbox_list.index(next_operator)
                    # check below
                    prev_operator = operators_list[i]
                    while i > 0 and prev_operator not in listbox_list:
                        i -= 1
                        prev_operator = operators_list[i]
                    # if none below, check above
                    if i == 0:
                        i = operators_list.index(item)
                        i += 1
                        next_operator = operators_list[i]
                        while next_operator not in listbox_list:
                            i += 1
                            next_operator = operators_list[i]
                        i = listbox_list.index(next_operator)
                    else:
                        i = listbox_list.index(prev_operator) + 1
                    priority_extras_listbox.insert(i, item)
                else:
                    priority_extras_listbox.insert(0, item)
            selected_list = []
            while priority_extras_listbox.curselection():
                i = priority_extras_listbox.curselection()[0]
                selected_list.insert(0, priority_extras_listbox.get(i))
                priority_extras_listbox.delete(i)
            for item in selected_list:
                priority_listbox.insert(0, item)
        def clear_selection():
            priority_listbox.selection_clear(0, "end")
            priority_extras_listbox.selection_clear(0, "end")
        add_remove_priority_button = tkTools.Button(priority_tags_frame, display_text="<->", width=4, function_when_clicked=lambda: add_remove_priority())
        add_remove_priority_button.grid(column=1, row=2)
        clear_selection_button = tkTools.Button(priority_tags_frame, display_text="Clr", width=4, function_when_clicked=lambda: clear_selection())
        clear_selection_button.grid(column=1, row=3)
        # frame for ordering tag priorities --end--


        recruitment_time_spinbox = tkTools.Spinbox(settings_frame, values=recruitment_times_list, width=8, state="readonly")
        recruitment_time_spinbox.pack(side="top", anchor="nw")
        recruitment_time_spinbox.set(profile.get_profile_option("recruitment_time"))
        expedited_plans_checkbutton = tkTools.Checkbutton(settings_frame, display_text="Use expedited plans", saveValueTo_variable=use_expedited_plans_Var)
        expedited_plans_checkbutton.pack(side="top", anchor="nw")
        if profile.get_profile_option("use_expedited_plans") == "True":
            use_expedited_plans_Var.set(True)
        prepare_recruitments_checkbutton = tkTools.Checkbutton(settings_frame, display_text="Prepare recruitments afterwards", saveValueTo_variable=prep_recruitments_Var)
        prepare_recruitments_checkbutton.pack(side="top", anchor="nw")
        if profile.get_profile_option("prepare_end_recruits") == "True":
            prep_recruitments_Var.set(True)
        def update_profile():
            profile.settings["emulator_path"] = emulator_path_entry.get()
            profile.settings["emulator_title"] = emulator_title_entry.get()
            profile.settings["permits_num"] = recruitment_permits_entry.get()
            profile.settings["recruitment_time"] = recruitment_time_spinbox.get()
            profile.settings["use_expedited_plans"] = str(use_expedited_plans_Var.get())
            profile.settings["prepare_end_recruits"] = str(prep_recruitments_Var.get())
            profile.settings["priority_list"] = "|".join(priority_listbox.get(0, "end"))
            profile.save_profile()
        save_button = tkTools.Button(settings_frame, display_text="Save", function_when_clicked=lambda: update_profile())
        save_button.pack(side="top", anchor="nw")
        start_button = tkTools.Button(settings_frame, display_text="Start",
                                      function_when_clicked=lambda: AutoRecruit.start_AutoRecruit(
                                          emulator_path_entry.get(),
                                          emulator_title_entry.get(),
                                          int(recruitment_permits_entry.get()),
                                          recruitment_time_spinbox.get(),
                                          use_expedited_plans_Var.get(),
                                          prep_recruitments_Var.get(),
                                          priority_listbox.get(0, "end"),
                                          skip_emulator_launch=skip_emulator_launch_Var.get(),
                                          output_box=output_text
                                      )
                                      )
        start_button.pack(side="top", anchor="nw")

        # settings frame setup --end--
