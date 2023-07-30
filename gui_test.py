import tkinter
from tkinter import ttk
import tkinter_ttk_tools as ttkTools
import recruitment_database_tools as recruitTools


def swap_frame_grids(old_frame: ttk.Frame, new_frame: ttk.Frame):
    """
    Only works with frames with grids
    """
    old_frame.grid_remove()
    new_frame.grid()

recruit_tools = recruitTools.tools()
root = ttkTools.setup("Auto Recruit", window_size=(800, 450), min_size=(400, 200))
ttkTools.configure_grid(root,
                        [
                            [0, None, None, None, 1]
                        ],
                        [
                            [0, None, None, None, 1]
                        ]
                        )
root_frame = ttkTools.frame_setup(root)
ttkTools.grid(root_frame, column=0, row=0, sticky="NSEW")
root_frame.columnconfigure(0, weight=1)
root_frame.rowconfigure(0, weight=1)
tagsQual_dict = {
    "ROB": "Robot",
    "STR": "Starter",
    "SEN": "Senior Operator",
    "TOP": "Top Operator"
}
tagsPos_dict = {
    "MEL": "Melee",
    "RNG": "Ranged"
}
tagsClass_dict = {
    "CAS": "Caster",
    "DEF": "Defender",
    "GUA": "Guard",
    "MED": "Medic",
    "SNI": "Sniper",
    "SPE": "Specialist",
    "SUP": "Supporter",
    "VAN": "Vanguard"
}
tagsSpec_dict = {
    "AOE": "AOE",
    "CDC": "Crowd Control",
    "DBF": "Debuff",
    "DFS": "Defense",
    "DPR": "DP-Recovery",
    "DPS": "DPS",
    "FRD": "Fast-Redeploy",
    "HEA": "Healing",
    "NUK": "Nuker",
    "SFT": "Shift",
    "SLW": "Slow",
    "SMN": "Summon",
    "SPT": "Support",
    "SRV": "Survival"
}
tagsQual_keysList = list(tagsQual_dict.keys())
tagsQual_valuesList = list(tagsQual_dict.values())
tagsPos_keysList = list(tagsPos_dict.keys())
tagsPos_valuesList = list(tagsPos_dict.values())
tagsClass_keysList = list(tagsClass_dict.keys())
tagsClass_valuesList = list(tagsClass_dict.values())
tagsSpec_keysList = list(tagsSpec_dict.keys())
tagsSpec_valuesList = list(tagsSpec_dict.values())

# home frame
home_frame = ttkTools.frame_setup(root_frame)
ttkTools.grid(home_frame, column=0, row=0, sticky="NSEW")
ttkTools.configure_grid(home_frame,
                        [
                            [0, None, None, None, 1]
                        ],
                        [
                            [0, 60, None, None, 0],
                            [1, None, None, None, 10],
                            [2, None, None, None, 1]
                        ]
                        )
home_frame.grid_remove()

# database_tools frame
database_tools_frame = ttkTools.frame_setup(root_frame)
ttkTools.grid(database_tools_frame, column=0, row=0, sticky="NSEW")
ttkTools.configure_grid(database_tools_frame,
                        [
                            [0, 160, None, None, 0],
                            [1, 200, None, None, 1],
                            [2, 100, None, None, 0]
                        ],
                        [
                            [0, 50, None, None, 0],
                            [1, 500, None, None, 1]
                        ]
                        )
database_tools_frame.grid_remove()

# widgets for the frames
def home_frame_widgets():
    title = ttkTools.label_setup(home_frame, display_text="Arknights AutoRecruit", font=("Helvetica", 16, "bold"), text_padding=10)
    title.grid(column=0, row=0, sticky="NW")
    setup_button = ttkTools.button_setup(home_frame, display_text="Setup", function=None)
    setup_button.grid(column=0, row=2, sticky="SE")
    menu = ttkTools.frame_setup(home_frame)
    menu.grid(column=0, row=1, sticky="NSEW")
    ttkTools.configure_grid(menu,
                            [
                                [0, None, None, None, 1]
                            ],
                            [
                                [0, 30, None, None, 0],
                                [1, 30, None, None, 0]
                            ]
                            )
    recruit_button = ttkTools.button_setup(menu, display_text="Enter AutoRecruit", function=None)
    recruit_button.grid(column=0, row=0, sticky="NE")
    database_tools_button = ttkTools.button_setup(menu, display_text="Database Tools",
                                    function=lambda: swap_frame_grids(home_frame, database_tools_frame))
    database_tools_button.grid(column=0, row=1, sticky="NE")
    database_tools_button.bind("<ButtonPress>", lambda e: recruit_tools.open_db())

def database_tools_widgets():
    back_button = ttkTools.button_setup(database_tools_frame, display_text="Back",
                                        function=lambda: swap_frame_grids(database_tools_frame, home_frame))
    back_button.grid(column=0, row=0, sticky="NW")
    back_button.bind("<ButtonPress>", lambda e: recruit_tools.close_db())

    # buttons to change the displayed data
    button_display_frame = ttkTools.frame_setup(database_tools_frame)
    button_display_frame.grid(column=0, row=1, sticky="NSEW")
    operator_table_button = ttkTools.button_setup(button_display_frame, display_text="Operator Table",
                                                  function=None)
    operator_table_button.pack(side="top", anchor="nw")
    tag_combinations_table_button = ttkTools.button_setup(button_display_frame, display_text="Tag Combinations",
                                                          function=None)
    tag_combinations_table_button.pack(side="top", anchor="nw")
    recalculate_button = ttkTools.button_setup(button_display_frame, display_text="Recalculate\nTag Combinations",
                                               function=None)
    recalculate_button.pack(side="top", anchor="nw")

    # table of recruitable operators
    table_frame, scroll_canvas, operator_table = ttkTools.scrollbar_frame_setup(database_tools_frame, height=300, width=400)
    table_frame.grid(column=1, row=1)
    ttkTools.configure_grid(operator_table,
                            [
                                [0, 40, None, None, 0],
                                [1, 10, None, None, 0],
                                [2, 160, None, None, 0],
                                [3, 80, None, None, 0]
                            ],
                            []
                            )
    # configure table
    def configure_operator_table():
        operator_list = recruit_tools.select_all_from_Operators()
        num_rows = len(operator_list)
        num_cols = len(operator_list[0])
        table = [[ttk.Entry() for j in range(num_cols)] for i in range(num_rows)]
        for r in range(num_rows):
            operator_table.rowconfigure(r, weight=0)
            for c in range(num_cols):
                if c == 0:
                    table[r][c] = ttkTools.entry_setup(operator_table, width=5)
                if c == 1:
                    table[r][c] = ttkTools.entry_setup(operator_table, width=2, foreground="grey")
                if c == 2:
                    table[r][c] = ttkTools.entry_setup(operator_table, width=20)
                if c == 3:
                    table[r][c] = ttkTools.entry_setup(operator_table, width=24)
                table[r][c].grid(column=c, row=r)
                table[r][c].insert(0, operator_list[r][c])
                table[r][c].configure(state="readonly")
                table[r][c].bind("<FocusIn>", lambda event, row=r, num_cols=num_cols: select_row(row, num_cols))
        table_frame.update_idletasks()
        scroll_canvas.configure(scrollregion=scroll_canvas.bbox("all"))
    configure_operator_table()

    # frame containing the settings to add an operator to the database
    operator_form = ttk.Frame(database_tools_frame)
    operator_form.grid(column=2, row=1, sticky="NSEW")
    ttkTools.configure_grid(operator_form,
                            [
                                [0, 150, None, None, 0]
                            ],
                            [
                                [0, 30, None, None, 0],
                                [1, 30, None, None, 0],
                                [2, 150, None, None, 0],
                                [3, 30, None, None, 0]
                            ]
                            )
    def operator_form_widgets():
        def insert_operator():
            operator_name = nameVar.get()
            rarity = rarityVar.get()
            TQidx = tagsQual_lbox.curselection()
            TPidx = tagsPos_lbox.curselection()
            TCidx = tagsClass_lbox.curselection()
            TSidx = tagsSpec_lbox.curselection()
            tags = []
            if TQidx:
                for i in TQidx:
                    tags.append(tagsQual_keysList[i])
            if TPidx:
                for i in TPidx:
                    tags.append(tagsPos_keysList[i])
            if TCidx:
                for i in TCidx:
                    tags.append(tagsClass_keysList[i])
            if TSidx:
                for i in TSidx:
                    tags.append(tagsSpec_keysList[i])
            nameVar.set("")
            rarityVar.set("")
            tagsQual_lbox.selection_clear(0, "end")
            tagsPos_lbox.selection_clear(0, "end")
            tagsClass_lbox.selection_clear(0, "end")
            tagsSpec_lbox.selection_clear(0, "end")
            db_tools.update_operator(orig_name=operator_name, new_tags=tags)
            table_frame_grid(setup=True)
            table_frame_grid()
            return

        nameVar = tkinter.StringVar()
        rarityVar = tkinter.StringVar()
        operator_name_entry = ttkTools.entry_setup(operator_form, saveTo_variable=nameVar)
        operator_name_entry.grid(column=0, row=0, sticky="NW")
        # operator_name_entry.bind("<FocusIn>", handle_focus_in())
        # operator_name_entry.bind("<FocusOut>", handle_focus_out())
        rarity_box = ttkTools.spinbox_setup(operator_form, 1, 6, width=4)
        rarity_box.grid(column=0, row=1, sticky="NW")
        # frame for packing inside a gridded frame
        tag_options = ttkTools.frame_setup(operator_form)
        tag_options.grid(column=0, row=2, sticky="NSEW")
        tags_label = ttkTools.label_setup(tag_options, display_text="Tags")
        tags_label.pack(side="top", anchor="nw")
        tagsQual_lbox = ttkTools.listbox_setup(
            tag_options,
            list_variable=tkinter.StringVar(value=tagsQual_valuesList),
            select_mode="multiple",
            stay_selected_when_unfocused=True,
            backdrop="ridge",
            height=6,
            width=14
        )
        tagsPos_lbox = ttkTools.listbox_setup(
            tag_options,
            list_variable=tkinter.StringVar(value=tagsPos_valuesList),
            select_mode="multiple",
            stay_selected_when_unfocused=False,
            backdrop="ridge",
            height=6,
            width=7
        )
        tagsClass_lbox = ttkTools.listbox_setup(
            tag_options,
            list_variable=tkinter.StringVar(value=tagsClass_valuesList),
            select_mode="multiple",
            stay_selected_when_unfocused=False,
            backdrop="ridge",
            height=6,
            width=9
        )
        tagsSpec_lbox = ttkTools.listbox_setup(
            tag_options,
            list_variable=tkinter.StringVar(value=tagsSpec_valuesList),
            select_mode="multiple",
            stay_selected_when_unfocused=False,
            backdrop="ridge",
            height=6,
            width=12
        )
        tagsQual_lbox.pack(side="left", anchor="nw", padx=(0, 0))
        tagsPos_lbox.pack(side="left", anchor="nw", padx=(0, 0))
        tagsClass_lbox.pack(side="left", anchor="nw", padx=(0, 0))
        tagsSpec_lbox.pack(side="left", anchor="nw", padx=(0, 0))
        # buttons to update the table
        def update_recruit_db(statement_type: str):
            operator_name = nameVar.get()
            rarity = rarityVar.get()
            TQidx = tagsQual_lbox.curselection()
            TPidx = tagsPos_lbox.curselection()
            TCidx = tagsClass_lbox.curselection()
            TSidx = tagsSpec_lbox.curselection()
            tags = []
            if TQidx:
                for i in TQidx:
                    tags.append(self.tagsQual_keysList[i])
            if TPidx:
                for i in TPidx:
                    tags.append(self.tagsPos_keysList[i])
            if TCidx:
                for i in TCidx:
                    tags.append(self.tagsClass_keysList[i])
            if TSidx:
                for i in TSidx:
                    tags.append(self.tagsSpec_keysList[i])
            nameVar.set("")
            rarityVar.set("")
            tagsQual_lbox.selection_clear(0, "end")
            tagsPos_lbox.selection_clear(0, "end")
            tagsClass_lbox.selection_clear(0, "end")
            tagsSpec_lbox.selection_clear(0, "end")
            if statement_type == "insert":
                recruit_tools.insert_new_operator(operator_name=operator_name, rarity=rarity, tag_list=tags)
            if statement_type == "update":
                db_tools.update_operator(orig_name=operator_name, new_tags=tags)
            configure_operator_table()

        # add_operator_button = ttkTools.button_setup(operator_form, display_text="Add to Database", function=lambda: update_recruit_db("insert"))
        # add_operator_button.grid(column=0, row=3, sticky="NW")
        update_operator_button = ttkTools.button_setup(operator_form, display_text="Update Database", function=lambda: update_recruit_db("update"))
        update_operator_button.grid(column=0, row=3, sticky="NW")

    operator_form_widgets()

home_frame_widgets()
database_tools_widgets()
home_frame.grid()


root.mainloop()
