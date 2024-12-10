import recruitment_database_tools as recruit_tools
import tkinter_tools as tkTools
import gui.HomeFrame


class Root(tkTools.MainWindow):
    def __init__(self, auto_recruit_window_name="Auto Recruit", window_size=(992, 450), position=(100, 100), min_size=(500, 200)):
        super().__init__(title=auto_recruit_window_name,
                         window_size=window_size,
                         position=position,
                         min_size=min_size)
        self.database = recruit_tools.Database()
        self.frame = None
        self.grid()
        self.widgets()
        self.HomeFrame = gui.HomeFrame.HomeFrame(self)
        self.HomeFrame.grid()
        self.mainloop()

    def grid(self):
        tkTools.grid_setup(self,
                           [
                                [0, None, None, None, 1]
                            ],
                           [
                                [0, None, None, None, 1]
                            ]
                           )

    def widgets(self):
        self.frame = tkTools.Frame(self)
        tkTools.grid_into(self.frame, column=0, row=0, sticky="NSEW")
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
