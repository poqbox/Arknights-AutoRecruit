import tkinter
from tkinter import ttk
import recruitment_database_tools


class GUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.title("Auto Recruit")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.geometry("800x450")
        self.root.minsize(400, 200)
        self.root_frame = tkinter.ttk.Frame(self.root)
        self.root_frame.grid(column=0, row=0, sticky="NSEW")
        self.root_frame.columnconfigure(0, weight=1)
        self.root_frame.rowconfigure(0, weight=0, minsize=60)
        self.root_frame.rowconfigure(1, weight=10)
        self.root_frame.rowconfigure(2, weight=1)
        self.tagsQual_dict = {
            "ROB": "Robot",
            "STR": "Starter",
            "SEN": "Senior Operator",
            "TOP": "Top Operator"
        }
        self.tagsPos_dict = {
            "MEL": "Melee",
            "RNG": "Ranged"
        }
        self.tagsClass_dict = {
            "CAS": "Caster",
            "DEF": "Defender",
            "GUA": "Guard",
            "MED": "Medic",
            "SNI": "Sniper",
            "SPE": "Specialist",
            "SUP": "Supporter",
            "VAN": "Vanguard"
        }
        self.tagsSpec_dict = {
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
        self.tagsQual_keysList = list(self.tagsQual_dict.keys())
        self.tagsQual_valuesList = list(self.tagsQual_dict.values())
        self.tagsPos_keysList = list(self.tagsPos_dict.keys())
        self.tagsPos_valuesList = list(self.tagsPos_dict.values())
        self.tagsClass_keysList = list(self.tagsClass_dict.keys())
        self.tagsClass_valuesList = list(self.tagsClass_dict.values())
        self.tagsSpec_keysList = list(self.tagsSpec_dict.keys())
        self.tagsSpec_valuesList = list(self.tagsSpec_dict.values())
        # home frame
        self.home_frame = tkinter.ttk.Frame(self.root_frame)
        self.home_frame_grid(setup=True)
        # database tools frame
        self.database_tools_frame = tkinter.ttk.Frame(self.root_frame)
        self.database_tools_frame_grid(setup=True)

    def switch_frame(self, current_frame, new_frame_grid):
        """new_frame_grid should be a function that configures the grid of a frame"""
        current_frame.grid_forget()
        new_frame_grid

    def home_frame_grid(self, setup=False):
        def home_frame_widgets(self):
            title = ttk.Label(self.home_frame, text="Arknights AutoRecruit", font=("Helvetica", 16, "bold"), padding=10)
            title.grid(column=0, row=0, rowspan=20, sticky="NW")
            ttk.Button(self.home_frame, text="Setup", command=None).grid(column=0, row=2, sticky="SE")
            menu = tkinter.ttk.Frame(self.home_frame)
            menu.grid(column=0, row=1, sticky="NSEW")
            menu.columnconfigure(0, weight=1)
            menu.rowconfigure(0, weight=0, minsize=30)
            menu.rowconfigure(1, weight=0, minsize=30)
            menu.rowconfigure(2, weight=0, minsize=30)
            ttk.Button(menu, text="Start AutoRecruit", command=None).grid(column=0, row=0, sticky="NE")
            ttk.Button(menu, text="Database Tools", command=lambda: self.switch_frame(self.home_frame, self.database_tools_frame_grid())).grid(column=0, row=1, sticky="NE")
            ttk.Button(menu, text="Update Recruitment Operators", command=None).grid(column=0, row=2, sticky="NE")

        self.home_frame.grid(column=0, row=0, sticky="NSEW")
        if setup:
            self.home_frame.columnconfigure(0, weight=1)
            self.home_frame.rowconfigure(0, weight=0, minsize=60)
            self.home_frame.rowconfigure(1, weight=10)
            self.home_frame.rowconfigure(2, weight=1)
            home_frame_widgets(self)
            self.home_frame.grid_forget()

    def database_tools_frame_grid(self, setup=False):
        db_tools = recruitment_database_tools.tools()

        def database_tools_frame_widgets():
            def switch_tab(current_frame, new_frame_grid):
                current_frame.grid_forget()
                new_frame_grid

            def table_frame_grid(setup=False):
                table_frame.grid(column=0, row=1, sticky="NSEW")
                if setup:
                    table_frame.columnconfigure(0, weight=1, minsize=150)
                    table_frame.rowconfigure(0, weight=0, minsize=30)
                    table_frame.rowconfigure(1, weight=1, minsize=150)
                    table_frame.rowconfigure(1, weight=0, minsize=30)
                    table_frame_widgets()
                    table_frame.grid_forget()

            def table_frame_widgets():
                def table_view_pack():
                    def select_row(row, num_cols):
                        for c in range(num_cols):
                            print(operator_list[row][c])

                    canvas_frame = ttk.Frame(table_frame, width=350, height=300)
                    canvas_frame.grid(column=0, row=1, sticky="NW")
                    canvas_frame.grid_rowconfigure(0, weight=1)
                    canvas_frame.grid_columnconfigure(0, weight=1)
                    canvas_frame.grid_propagate(False)

                    # canvas_frame --> canvas
                    canvas = tkinter.Canvas(canvas_frame)
                    canvas.grid(column=0, row=0, sticky="NSEW")

                    # v_scrollbar linked to canvas
                    v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
                    v_scrollbar.grid(column=1, row=0, sticky='ns')
                    canvas.configure(yscrollcommand=v_scrollbar.set)

                    # h_scrollbar linked to canvas
                    h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
                    h_scrollbar.grid(column=0, row=1, sticky='we')
                    canvas.configure(xscrollcommand=h_scrollbar.set)

                    # canvas_frame --> canvas --> frame for table
                    table1 = ttk.Frame(canvas)
                    table1.grid(column=0, row=0)
                    table1.columnconfigure(0, weight=0, minsize=40)
                    table1.columnconfigure(1, weight=0, minsize=10)
                    table1.columnconfigure(2, weight=0, minsize=160)
                    table1.columnconfigure(3, weight=0, minsize=80)
                    canvas.create_window((0, 0), window=table1, anchor='nw')

                    # setup table
                    operator_list = db_tools.select_all_from_Operators()
                    num_rows = len(operator_list)
                    num_cols = len(operator_list[0])
                    table = [[ttk.Button() for j in range(num_cols)] for i in range(num_rows)]
                    operator_list = db_tools.select_all_from_Operators()
                    num_rows = len(operator_list)
                    num_cols = len(operator_list[0])
                    for r in range(num_rows):
                        table1.rowconfigure(r, weight=0)
                        for c in range(num_cols):
                            if c == 0:
                                table[r][c] = ttk.Entry(table1, width=5)
                            if c == 1:
                                table[r][c] = ttk.Entry(table1, width=2, foreground="grey")
                            if c == 2:
                                table[r][c] = ttk.Entry(table1, width=20)
                            if c == 3:
                                table[r][c] = ttk.Entry(table1, width=24)
                            table[r][c].grid(column=c, row=r)
                            table[r][c].insert(0, operator_list[r][c])
                            table[r][c].configure(state="readonly")
                            table[r][c].bind("<FocusIn>", lambda event, row=r, num_cols=num_cols: select_row(row, num_cols))

                    table1.update_idletasks()
                    canvas.configure(scrollregion=canvas.bbox("all"))

                self.tableVar = tkinter.StringVar()
                table_selection = ttk.Combobox(table_frame, textvariable=self.tableVar, width=20, values=("Operator Data", "Recruitment Tree"))
                table_selection.current(0)
                table_selection.grid(column=0, row=0, sticky="NW")
                table_view_pack()

            def operator_form_grid(setup=False):
                operator_form.grid(column=1, row=1, sticky="NSEW")
                if setup:
                    operator_form.columnconfigure(0, weight=0, minsize=150)
                    operator_form.rowconfigure(0, weight=0, minsize=30)
                    operator_form.rowconfigure(1, weight=0, minsize=30)
                    operator_form.rowconfigure(2, weight=0, minsize=150)
                    operator_form.rowconfigure(3, weight=0, minsize=30)
                    operator_form_widgets()
                    operator_form.grid_forget()

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
                    db_tools.update_operator(orig_name=operator_name, new_tags=tags)
                    table_frame_grid(setup=True)
                    table_frame_grid()
                    return

                nameVar = tkinter.StringVar()
                rarityVar = tkinter.StringVar()
                operator_name_entry = ttk.Entry(operator_form, textvariable=nameVar)
                operator_name_entry.grid(column=0, row=0, sticky="NW")
                # operator_name_entry.bind("<FocusIn>", handle_focus_in())
                # operator_name_entry.bind("<FocusOut>", handle_focus_out())
                ttk.Combobox(operator_form, textvariable=rarityVar, width=2, values=(1, 2, 3, 4, 5, 6)).grid(column=0, row=1, sticky="NW")
                # configure_AutoRecruit_frame --> tag_options
                tag_options = ttk.Frame(operator_form)
                tag_options.grid(column=0, row=2, sticky="NSEW")
                ttk.Label(tag_options, text="Tags").pack(side="top", anchor="nw")
                tagsQual_lbox = tkinter.Listbox(
                    tag_options,
                    listvariable=tkinter.StringVar(value=self.tagsQual_valuesList),
                    selectmode="multiple",
                    exportselection=False,
                    relief="ridge",
                    height=6,
                    width=14
                )
                tagsPos_lbox = tkinter.Listbox(
                    tag_options,
                    listvariable=tkinter.StringVar(value=self.tagsPos_valuesList),
                    selectmode="multiple",
                    exportselection=False,
                    relief="ridge",
                    height=6,
                    width=7
                )
                tagsClass_lbox = tkinter.Listbox(
                    tag_options,
                    listvariable=tkinter.StringVar(value=self.tagsClass_valuesList),
                    selectmode="multiple",
                    exportselection=False,
                    relief="ridge",
                    height=6,
                    width=9
                )
                tagsSpec_lbox = tkinter.Listbox(
                    tag_options,
                    listvariable=tkinter.StringVar(value=self.tagsSpec_valuesList),
                    selectmode="multiple",
                    exportselection=False,
                    relief="ridge",
                    height=6,
                    width=12
                )
                tagsQual_lbox.pack(side="left", anchor="nw", padx=(0, 0))
                tagsPos_lbox.pack(side="left", anchor="nw", padx=(0, 0))
                tagsClass_lbox.pack(side="left", anchor="nw", padx=(0, 0))
                tagsSpec_lbox.pack(side="left", anchor="nw", padx=(0, 0))
                # ttk.Button(operator_form, text="Add to Database", command=lambda: insert_operator()).grid(column=0, row=3, sticky="NW")
                ttk.Button(operator_form, text="Update Database", command=lambda: insert_operator()).grid(column=0, row=3, sticky="NW")

            def close_database():
                db_tools.close_db()

            back_button = ttk.Button(self.database_tools_frame, text="Back", command=lambda: self.switch_frame(self.database_tools_frame, self.home_frame_grid()))
            back_button.grid(column=0, row=0, sticky="NW")
            back_button.bind("<ButtonPress>", lambda e: close_database())
            table_frame = ttk.Frame(self.database_tools_frame)
            table_frame_grid(setup=True)
            table_frame_grid()
            operator_form = ttk.Frame(self.database_tools_frame)
            operator_form_grid(setup=True)
            operator_form_grid()

        self.database_tools_frame.grid(column=0, row=0, sticky="NSEW")
        if setup:
            self.database_tools_frame.columnconfigure(0, weight=0, minsize=400)
            self.database_tools_frame.columnconfigure(1, weight=1, minsize=100)
            self.database_tools_frame.rowconfigure(0, weight=0, minsize=50)
            self.database_tools_frame.rowconfigure(1, weight=1, minsize=500)
            database_tools_frame_widgets()
            self.database_tools_frame.grid_forget()

    def start(self):
        self.home_frame_grid()
        self.root.mainloop()


Arknights_AutoRecruit = GUI()
Arknights_AutoRecruit.start()
