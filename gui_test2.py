import tkinter
from tkinter import ttk


class GUI(tkinter.Tk):
    # inheritance?
    def __init__(self, *args, **kwargs):
        # "self.root = tkinter.Tk()" is replaced with self?
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title("Auto Recruit")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.geometry("800x450")
        self.minsize(400, 200)
        self.root_frame = tkinter.ttk.Frame(self)
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
        self.home_frame.grid(column=0, row=0, sticky="NSEW")
        if setup:
            self.home_frame.columnconfigure(0, weight=1)
            self.home_frame.rowconfigure(0, weight=0, minsize=60)
            self.home_frame.rowconfigure(1, weight=10)
            self.home_frame.rowconfigure(2, weight=1)
            self.home_frame_widgets()
            self.home_frame.grid_forget()

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

    def database_tools_frame_grid(self, setup=False):
        self.database_tools_frame.grid(column=0, row=0, sticky="NSEW")
        if setup:
            self.database_tools_frame.columnconfigure(0, weight=0, minsize=150)
            self.database_tools_frame.columnconfigure(1, weight=1, minsize=400)
            self.database_tools_frame.rowconfigure(0, weight=0, minsize=50)
            self.database_tools_frame.rowconfigure(1, weight=1, minsize=100)
            self.database_tools_frame_widgets()
            self.database_tools_frame.grid_forget()

    def database_tools_frame_widgets(self):
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
            print(operator_name, rarity, tags)
            nameVar.set("")
            rarityVar.set("")
            tagsQual_lbox.selection_clear(0, "end")
            tagsPos_lbox.selection_clear(0, "end")
            tagsClass_lbox.selection_clear(0, "end")
            tagsSpec_lbox.selection_clear(0, "end")
            return

        ttk.Button(self.database_tools_frame, text="Back", command=lambda: self.switch_frame(self.database_tools_frame, self.home_frame_grid())).grid(column=0, row=0, sticky="NW")
        operator_form = ttk.Frame(self.database_tools_frame)
        operator_form.grid(column=1, row=1, sticky="NSEW")
        operator_form.columnconfigure(0, weight=0, minsize=150)
        operator_form.rowconfigure(0, weight=0, minsize=30)
        operator_form.rowconfigure(1, weight=0, minsize=30)
        operator_form.rowconfigure(2, weight=0, minsize=150)
        operator_form.rowconfigure(3, weight=0, minsize=30)
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
        tagsQual_lbox.pack(side="left", anchor="nw", padx=(0, 10))
        tagsPos_lbox.pack(side="left", anchor="nw", padx=(0, 10))
        tagsClass_lbox.pack(side="left", anchor="nw", padx=(0, 10))
        tagsSpec_lbox.pack(side="left", anchor="nw", padx=(0, 10))
        ttk.Button(operator_form, text="Add to Database", command=lambda: insert_operator()).grid(column=0, row=3, sticky="NW")

    def update_recruitment_operators(self):
        self.home_frame = tkinter.ttk.Frame(self.root)
        self.home_frame.grid(column=0, row=0, sticky="NSEW")
        self.home_frame.columnconfigure(0, weight=1)
        self.home_frame.rowconfigure(0, weight=0, minsize=60)
        self.home_frame.rowconfigure(1, weight=0, minsize=60)
        #
        ttk.Button(self.home_frame, text="Back", command=self.switch_frame(0))
        #

    def start(self):
        self.home_frame_grid()
        self.mainloop()


Arknights_AutoRecruit = GUI()
Arknights_AutoRecruit.start()
