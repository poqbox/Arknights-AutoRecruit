import tkinter_tools as tkTools
import gui.AutoRecruitFrame
import gui.DatabaseToolsFrame


# home frame
class HomeFrame(tkTools.Frame):
    def __init__(self, root):
        super().__init__(root.frame)
        self.root = root
        self.AutoRecruitFrame = gui.AutoRecruitFrame.AutoRecruitFrame(self, root)
        self.DatabaseToolsFrame = gui.DatabaseToolsFrame.DatabaseToolsFrame(self, root)
        self.grid_configure(column=0, row=0, sticky="NSEW")
        self.grid_setup()
        self.widgets()

    def grid_setup(self):
        tkTools.grid_setup(self,
                           [
                                [0, None, None, None, 1]
                            ],
                           [
                                [0, 60, None, None, 0],
                                [1, None, None, None, 10],
                                [2, None, None, None, 1]
                            ]
                           )
        self.grid_remove()

    def widgets(self):
        title = tkTools.Label(self, display_text="Arknights AutoRecruit", font=("Helvetica", 16, "bold"), text_padding=10)
        title.grid(column=0, row=0, sticky="NW")
        menu = tkTools.Frame(self)
        menu.grid(column=0, row=1, sticky="NSEW")
        tkTools.grid_setup(menu,
                           [
                               [0, None, None, None, 1]
                           ],
                           [
                               [0, 30, None, None, 0],
                               [1, 30, None, None, 0]
                           ]
                           )
        recruit_button = tkTools.Button(menu, display_text="Enter AutoRecruit",
                                        function_when_clicked=tkTools.swap_frame(self, self.AutoRecruitFrame))
        recruit_button.grid(column=0, row=0, sticky="NE")
        database_tools_button = tkTools.Button(menu, display_text="Database Tools",
                                               function_when_clicked=tkTools.swap_frame(self, self.DatabaseToolsFrame))
        database_tools_button.grid(column=0, row=1, sticky="NE")
        database_tools_button.bind("<ButtonPress>", lambda e: self.root.database.open_db())
        setup_button = tkTools.Button(self, display_text="Setup", function_when_clicked=None)
        setup_button.grid(column=0, row=2, sticky="SE")
