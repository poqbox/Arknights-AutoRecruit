import config.config as config
import recruitment_database_tools as recruit_tools
import tkinter_tools as tkTools
import tkinter
from tkinter import font
from tkinter import scrolledtext
from tkinter import ttk


class DatabaseToolsFrame(tkTools.Frame):
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
                                [2, 100, None, None, 0]
                            ],
                           [
                                [0, 40, None, None, 0],
                                [1, 340, None, None, 1],
                                [2, 50, None, None, 0]
                            ]
                           )
        self.grid_remove()

    def widgets(self):
        # Back button
        back_button = tkTools.Button(self, display_text="Back",
                                     function_when_clicked=lambda: [tkTools.swap_frame(self, self.parent, _use_with_lambda_function=True), self.root.database.calculate()])
        back_button.grid(column=0, row=0, sticky="NW")

        # Operator Form setup --part 1--
        operator_form = tkTools.Frame(self)
        operator_form.grid(column=2, row=1, rowspan=2, sticky="NSEW")
        tkTools.grid_setup(operator_form,
                           [
                                [0, 150, None, None, 0]
                            ],
                           [
                                [0, 30, None, None, 0],
                                [1, 30, None, None, 0],
                                [2, 150, None, None, 0],
                                [3, 30, None, None, 0],
                                [4, 30, None, None, 0],
                                [5, 30, None, None, 0],
                                [6, 30, None, None, 1],
                                [7, 30, None, None, 0]
                            ]
                           )
        # global variables and widgets for extra access
        nameVar = tkinter.StringVar()
        rarityVar = tkinter.StringVar()
        idVar = tkinter.StringVar()
        name_entry = tkTools.Entry(operator_form, saveValueTo_variable=nameVar)
        name_entry.grid(column=0, row=0, sticky="NW")
        # frame for packing tag options inside a gridded frame
        tag_options = tkTools.Frame(operator_form)
        tag_options.grid(column=0, row=2, sticky="NSEW")
        tags_label = tkTools.Label(tag_options, display_text="Tags")
        tags_label.pack(side="top", anchor="nw")
        tagsQual_lbox = tkTools.Listbox(
            tag_options,
            list_variable=tkinter.StringVar(value=recruit_tools.tagsQual_valuesList),
            select_mode="multiple",
            stay_selected_when_unfocused=True,
            backdrop="ridge",
            height=6,
            width=14
        )
        tagsPos_lbox = tkTools.Listbox(
            tag_options,
            list_variable=tkinter.StringVar(value=recruit_tools.tagsPos_valuesList),
            select_mode="multiple",
            stay_selected_when_unfocused=True,
            backdrop="ridge",
            height=6,
            width=7
        )
        tagsClass_lbox = tkTools.Listbox(
            tag_options,
            list_variable=tkinter.StringVar(value=recruit_tools.tagsClass_valuesList),
            select_mode="multiple",
            stay_selected_when_unfocused=True,
            backdrop="ridge",
            height=6,
            width=9
        )
        tagsSpec_lbox = tkTools.Listbox(
            tag_options,
            list_variable=tkinter.StringVar(value=recruit_tools.tagsSpec_valuesList),
            select_mode="multiple",
            stay_selected_when_unfocused=True,
            backdrop="ridge",
            height=6,
            width=12
        )
        tagsQual_lbox.pack(side="left", anchor="nw", padx=(0, 0))
        tagsPos_lbox.pack(side="left", anchor="nw", padx=(0, 0))
        tagsClass_lbox.pack(side="left", anchor="nw", padx=(0, 0))
        tagsSpec_lbox.pack(side="left", anchor="nw", padx=(0, 0))

        # table setups --start--
        # Recruit-able Operators Table setup --start--
        operator_table = tkTools.Frame_with_scrollbar(self, sticky_scrollframe="NSEW",
                                                      sticky_content="NSEW", height=360, width=520,
                                                      grid_row=1, grid_column=1)
        tkTools.grid_setup(operator_table,
                           [
                                [0, 40, None, None, 0],
                                [1, 10, None, None, 0],
                                [2, 200, None, None, 0],
                                [3, 100, None, None, 0]
                            ],
                           []
                           )
        # configure operator_table
        def configure_operator_table():
            operator_list = self.root.database.get_operator_data(get=["all"])

            # method for filling the operator form by selecting a row in the operator table
            def fill_operator_form_with_table_row(row, cols):
                tagsQual_lbox.selection_clear(0, "end")
                tagsPos_lbox.selection_clear(0, "end")
                tagsClass_lbox.selection_clear(0, "end")
                tagsSpec_lbox.selection_clear(0, "end")
                name_entry.configure(foreground="black")
                idVar.set(operator_list[row][0])
                rarityVar.set(operator_list[row][1])
                nameVar.set(operator_list[row][2])
                tags_list = self.root.database.split_tags(operator_list[row][3])
                for tag in tags_list:
                    if recruit_tools.tagsQual_dict.get(tag):
                        tagsQual_lbox.selection_set(recruit_tools.tagsQual_keysList.index(tag))
                    if recruit_tools.tagsPos_dict.get(tag):
                        tagsPos_lbox.selection_set(recruit_tools.tagsPos_keysList.index(tag))
                    if recruit_tools.tagsClass_dict.get(tag):
                        tagsClass_lbox.selection_set(recruit_tools.tagsClass_keysList.index(tag))
                    if recruit_tools.tagsSpec_dict.get(tag):
                        tagsSpec_lbox.selection_set(recruit_tools.tagsSpec_keysList.index(tag))

            num_rows = len(operator_list)
            num_cols = len(operator_list[0])
            table = [[ttk.Entry() for col in range(num_cols)] for row in range(num_rows)]
            for r in range(num_rows):
                operator_table.rowconfigure(r, weight=0)
                for c in range(num_cols):
                    if c == 0:
                        table[r][c] = tkTools.Entry(operator_table, width=5)
                    if c == 1:
                        table[r][c] = tkTools.Entry(operator_table, width=2, text_color="grey")
                    if c == 2:
                        table[r][c] = tkTools.Entry(operator_table, width=25)
                    if c == 3:
                        table[r][c] = tkTools.Entry(operator_table, width=25)
                    table[r][c].grid(column=c, row=r)
                    table[r][c].insert(0, operator_list[r][c])
                    table[r][c].configure(state="readonly")
                    table[r][c].bind("<FocusIn>", lambda event, row=r, cols=num_cols: fill_operator_form_with_table_row(row, cols))
            operator_table.finish_scrollbar_frame_setup()
        configure_operator_table()
        operator_table.grid_remove()

        # Tag Combinations Table setup --start--
        raw_tag_combos_text = scrolledtext.ScrolledText(self, height=18)
        raw_tag_combos_text.grid(column=1, row=1, sticky="NEW")
        def configure_tag_combinations_table():
            raw_tag_combos_text.delete(1.0, "end")
            tag_combinations_txt = [self.root.database.non_dist_combos,
                                    self.root.database.r4_tag_combos_dist,
                                    self.root.database.r5_tag_combos_dist,
                                    self.root.database.r6_tag_combos_dist
                                    ]
            for i, rarity_row in enumerate(tag_combinations_txt):
                if i == 0:
                    raw_tag_combos_text.insert("end", "rarity 3-4\n")
                else:
                    raw_tag_combos_text.insert("end", "\nrarity")
                    raw_tag_combos_text.insert("end", str(i+3))
                    raw_tag_combos_text.insert("end", "\n")
                for combo_count_row in rarity_row:
                    for combo in combo_count_row:
                        raw_tag_combos_text.insert("end", ",".join(combo) + "|")
                    raw_tag_combos_text.insert("end", "\n")
            raw_tag_combos_text.configure(state="disabled")
        configure_tag_combinations_table()
        raw_tag_combos_text.grid_remove()
        operator_table.grid()

        # method for swapping tables
        class table_tool:
            current_id = 0
            table_frame_id = {}
        table_control = table_tool
        table_control.current_id = 1
        table_control.table_frame_id[1] = operator_table
        table_control.table_frame_id[2] = raw_tag_combos_text

        def swap_table_frame_grids(new_table_frame_id: int):
            """
            Refer to the table_frame_dict for table_frame ids
            """
            if new_table_frame_id != table_control.current_id:
                table_control.table_frame_id[table_control.current_id].grid_remove()
                table_control.table_frame_id[new_table_frame_id].grid()
                table_control.current_id = new_table_frame_id

        # method for updating the current table after updating the recruitment database
        def configure_tables():
            configure_operator_table()
            configure_tag_combinations_table()
        # table setups --end--

        # buttons to change the displayed data
        button_display_frame = tkTools.Frame(self)
        button_display_frame.grid(column=0, row=1, sticky="NSEW")
        operator_table_button = tkTools.Button(button_display_frame, display_text="Operator Table", function_when_clicked=lambda: swap_table_frame_grids(1))
        operator_table_button.pack(side="top", anchor="nw")
        tag_combinations_table_button = tkTools.Button(button_display_frame, display_text="Tag Combinations", function_when_clicked=lambda: swap_table_frame_grids(2))
        tag_combinations_table_button.pack(side="top", anchor="nw")
        recalculate_button = tkTools.Button(button_display_frame, display_text="Recalculate\nTag Combinations", function_when_clicked=lambda: [self.root.database.calculate(), configure_tables()])
        recalculate_button.pack(side="top", anchor="nw")
        def open_help_window():
            help_window = tkTools.SubWindow(self.root, title="Instructions", window_size="400x300")
            text1 = "Using the database"
            text2 = "Updating an operator:\n" \
                    "        Requires name, tags\n" \
                    "Adding a new operator:\n" \
                    "        Requires name, rarity, tags\n" \
                    "Deleting an operator:\n" \
                    "        Requires operator ID"
            label1 = tkTools.Label(help_window, display_text=text1, font=("Helvetica", 12, "bold"))
            label1.pack(side="top", anchor="nw")
            label2 = tkTools.Label(help_window, display_text=text2)
            label2.pack(side="top", anchor="nw")
            label2.configure(wraplength=400)
        help_button = tkTools.Button(button_display_frame, display_text="Help", function_when_clicked=lambda: open_help_window(), width=4)
        help_button.pack(side="top", anchor="nw")

        # version frame --start--
        version_frame = tkTools.Frame(self)
        version_frame.grid(column=0, row=2, columnspan=2, sticky="NSEW")
        version_text = "ver. " + config.get_autorecruit_version() + ".[" + config.get_database_version() + "]"
        version_label = tkTools.Label(version_frame, display_text=version_text, font=("Courier", 8))
        version_label.configure(foreground="grey")
        version_label.pack(side="bottom", anchor="sw")
        def open_update_version_window():
            def update_database_version():
                config.set_database_version(version_textbox.get("1.0", "end"))
                updated_version = "ver. " + config.get_autorecruit_version() + ".[" + config.get_database_version() + "]"
                version_label.configure(text=updated_version)

            version_window = tkinter.Toplevel(self.root)
            version_window.title("Update recruitment version")
            version_window.geometry("400x110")
            version_textbox = tkTools.Text(version_window, width=20, height=2)
            version_textbox.pack(side="top", anchor="nw")
            version_textbox.insert("end", config.get_database_version())
            update_version_button = tkTools.Button(version_window, display_text="Update database version",
                                                   function_when_clicked=lambda: [update_database_version(), version_window.destroy(), version_window.update()])
            update_version_button.pack(side="top", anchor="nw")
            cancel_button = tkTools.Button(version_window, display_text="CANCEL", width=7,
                                           function_when_clicked=lambda: [version_window.destroy(), version_window.update()])
            cancel_button.pack(side="top", anchor="nw")
        recruit_version_button = tkTools.Button(version_frame, display_text="Update Version", function_when_clicked=lambda: open_update_version_window())
        recruit_version_button.pack(side="bottom", anchor="sw")
        # version frame --end--

        # Operator Form setup --part 2--
        def operator_form_widgets():
            # methods for implementing a default value in the name_entry widget
            def name_entry_default():
                name_entry.configure(foreground="grey")
                name_entry.insert(0, "Operator Name")
            def name_entry_Focus(focus_type: str):
                name = nameVar.get()
                if focus_type.lower() == "in":
                    if name.lower() == "operator name":
                        name_entry.configure(foreground="black")
                        name_entry.delete(0, "end")
                if focus_type.lower() == "out":
                    if not name or name.lower() == "operator name":
                        name_entry.configure(foreground="grey")
                        name_entry.delete(0, "end")
                        name_entry.insert(0, "Operator Name")
            name_entry_default()
            name_entry.bind("<FocusIn>", lambda e: name_entry_Focus("in"))
            name_entry.bind("<FocusOut>", lambda e: name_entry_Focus("out"))
            rarity_box = tkTools.Spinbox(operator_form, 1, 6, saveValueTo_variable=rarityVar, width=4)
            rarity_box.grid(column=0, row=1, sticky="NW")
            # buttons to update the table
            def update_recruit_db(statement_type: str):
                if statement_type == "insert" or statement_type == "update" or statement_type == "delete":
                    operator_id = idVar.get()
                    if statement_type == "delete":
                        delete_operator_window = tkinter.Toplevel(self.root)
                        delete_operator_window.title("Warning: Deleting Operator")
                        delete_operator_window.geometry("400x200")
                        delete_operator_window.grab_set()
                        delete_operator_window.bind("<FocusOut>", lambda e: [delete_operator_window.bell(), delete_operator_window.focus_force()])
                        operator_data = self.root.database.get_operator_data(get=["all"], where=["id=" + operator_id])
                        if operator_data == None:
                            # error label
                            error_label = tkTools.Label(delete_operator_window, display_text="Error: operator_id_" + operator_id + " not found")
                            error_label.pack(side="top")
                        else:
                            # warning label
                            warning_label = tkTools.Label(delete_operator_window, display_text="Are you sure you want to delete the following operator:")
                            warning_label.pack(side="top")
                            # operator data
                            operator_data_str = "id:\t" + str(operator_data[0]) + "\nrarity:\t" + str(operator_data[1]) + "\nname:\t" + operator_data[2] + "\ntags:\t" + operator_data[3]
                            operator_data_label = tkTools.Label(delete_operator_window, display_text=operator_data_str, width=200)
                            operator_data_label.pack(side="top")
                            confirm_button = tkTools.Button(delete_operator_window, display_text="CONFIRM",
                                                            function_when_clicked=lambda: [self.root.database.delete_operator(
                                                                operator_id=int(operator_id)), delete_operator_window.destroy(), delete_operator_window.update(), self.root.calculate(), configure_tables()])
                            confirm_button.pack(side="top")
                        cancel_button = tkTools.Button(delete_operator_window, display_text="CANCEL", function_when_clicked=lambda: [delete_operator_window.destroy(), delete_operator_window.update()])
                        cancel_button.pack(side="top")
                    else:
                        operator_name = nameVar.get()
                        rarity = rarityVar.get()
                        TQidx = tagsQual_lbox.curselection()
                        TPidx = tagsPos_lbox.curselection()
                        TCidx = tagsClass_lbox.curselection()
                        TSidx = tagsSpec_lbox.curselection()
                        tags = []
                        if TQidx:
                            for i in TQidx:
                                tags.append(recruit_tools.tagsQual_keysList[i])
                        if TPidx:
                            for i in TPidx:
                                tags.append(recruit_tools.tagsPos_keysList[i])
                        if TCidx:
                            for i in TCidx:
                                tags.append(recruit_tools.tagsClass_keysList[i])
                        if TSidx:
                            for i in TSidx:
                                tags.append(recruit_tools.tagsSpec_keysList[i])
                        if statement_type == "update":
                            self.root.database.update_operator(orig_name=operator_name, new_tags=tags)
                            self.root.database.calculate()
                        if statement_type == "insert":
                            self.root.database.insert_new_operator(operator_name=operator_name, rarity=rarity, tag_list=tags)
                        self.root.database.calculate()
                    nameVar.set("")
                    rarityVar.set("")
                    idVar.set("")
                    tagsQual_lbox.selection_clear(0, "end")
                    tagsPos_lbox.selection_clear(0, "end")
                    tagsClass_lbox.selection_clear(0, "end")
                    tagsSpec_lbox.selection_clear(0, "end")
                    name_entry_default()
                    configure_tables()
            add_operator_button = tkTools.Button(operator_form, display_text="Add to Database", function_when_clicked=lambda: update_recruit_db("insert"))
            add_operator_button.grid(column=0, row=3, sticky="NW")
            update_operator_button = tkTools.Button(operator_form, display_text="Update Database", function_when_clicked=lambda: update_recruit_db("update"))
            update_operator_button.grid(column=0, row=4, sticky="NW")
            # undo_button = ttkTools.button_setup(operator_form, display_text="Undo", function=None, width=5)
            # undo_button.grid(column=0, row=5, sticky="NW")
            # delete operator options
            operator_id_entry = tkTools.Entry(operator_form, saveValueTo_variable=idVar, width=6)
            operator_id_entry.grid(column=0, row=6, sticky="SE")
            delete_operator_button = tkTools.Button(operator_form, display_text="Delete Operator", function_when_clicked=lambda: update_recruit_db("delete"))
            delete_operator_button.grid(column=0, row=7, sticky="SE")
        # Operator Form setup --end--
