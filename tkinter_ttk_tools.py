import tkinter
from tkinter import ttk
from typing import Union


def setup(title: str, window_size, min_size=None):
    """
    Everything will be created within this variable.\n
    Widgets can be either packed or gridded, but not combined.
    """
    root = tkinter.Tk()
    root.title(title)
    root.geometry(str(window_size[0]) + "x" + str(window_size[1]))
    if min_size:
        root.minsize(min_size[0], min_size[1])
    return root


def frame_setup(parent, padding=None, width=None, height=None):
    frame = ttk.Frame(parent,
                      padding=padding,
                      width=width,
                      height=height
                      )
    return frame


def configure_grid(widget, columns_list, rows_list):
    """
    The parameters of each index are:\n
    [0]: [int] col/row index\n
    [1]: [float] minimum size\n
    [2]: [float] padding\n
    [3]: [str] name of the uniform-group\n
    [4]: [int] weight\n
    Use type [None] for unused parameters
    """
    for col in columns_list:
        widget.columnconfigure(index=col[0],
                               minsize=col[1],
                               pad=col[2],
                               uniform=col[3],
                               weight=col[4]
                               )
    for row in rows_list:
        widget.rowconfigure(index=row[0],
                            minsize=row[1],
                            pad=row[2],
                            uniform=row[3],
                            weight=row[4]
                            )


def grid(widget, column: int, row: int, sticky: str=None, columnspan: int=None, rowspan: int=None,
               interior_padding_x=None, interior_padding_y=None, exterior_padding_x=None, exterior_padding_y=None):
    """
    column and row refer to the parent widget
    """
    def widget_grid(widget, a, b, c, d, e, f, g, h, i):
        widget.grid(column=a,
                    row=b,
                    sticky=c,
                    columnspan=d,
                    rowspan=e,
                    ipadx=f,
                    ipady=g,
                    padx=h,
                    pady=i
                    )

    widget_grid(widget, column, row, sticky, columnspan, rowspan,
                interior_padding_x, interior_padding_y, exterior_padding_x, exterior_padding_y
                )
    return lambda: widget_grid(widget, column, row, sticky, columnspan, rowspan, interior_padding_x, interior_padding_y, exterior_padding_x, exterior_padding_y)


def pack(widget, side, anchor,
               interior_padding_x=None, interior_padding_y=None, exterior_padding_x=None, exterior_padding_y=None):
    widget_pack = lambda: widget.pack(side=side,
                                      anchor=anchor,
                                      ipadx=interior_padding_x,
                                      ipady=interior_padding_y,
                                      padx=exterior_padding_x,
                                      pady=exterior_padding_y
                                      )
    widget_pack
    return widget_pack


def button_setup(parent, display_text: str=None, function=None, width=None, text_padding=None, state=None):
    """
    use "lambda: [function]" when using the function parameter
    """
    button = ttk.Button(parent,
                        text=display_text,
                        command=function,
                        width=width,
                        padding=text_padding,
                        state=state
                        )
    return button


def checkbox_setup(parent, display_text: str=None, saveValueTo_variable=None, value_when_checked=1, value_when_unchecked=0, width=None, state=None):
    """
    Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
    """
    checkbutton = ttk.Checkbutton(parent,
                                  text=display_text,
                                  variable=saveValueTo_variable,
                                  onvalue=value_when_checked,
                                  offvalue=value_when_unchecked,
                                  width=width,
                                  state=state
                                  )
    return checkbutton


def combobox_setup(parent, values, saveTo_variable=None, font=None, width=None, background=None, state=None):
    """
    Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
    """
    combobox = ttk.Combobox(parent,
                            values=values,
                            textvariable=saveTo_variable,
                            font=font,
                            width=width,
                            background=background,
                            state=state
                            )
    return combobox


def entry_setup(parent, saveTo_variable: tkinter.StringVar=None, font=None, width=None, foreground=None, state=None):
    """
    Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
    """
    entry = ttk.Entry(parent,
                      textvariable=saveTo_variable,
                      font=font,
                      width=width,
                      foreground=foreground,
                      state=state
                      )
    return entry


def label_setup(parent, display_text: str=None, font=None, width=None, background=None, text_padding=None, state=None):
    label = ttk.Label(parent,
                      text=display_text,
                      font=font,
                      width=width,
                      background=background,
                      padding=text_padding,
                      state=state
                      )
    return label


def listbox_setup(parent, list_variable=None, select_mode=None, stay_selected_when_unfocused=None, backdrop=None, height=None, width=None, state=None):
    """
    Use tkinter type variables when using list_variable
    :param parent:
    :param saveTo_variable:
    :param select_mode:
    :param stay_selected_when_unfocused:
    :param backdrop: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]
    :param height:
    :param width:
    :return:
    """
    listbox = tkinter.Listbox(parent,
                              listvariable=list_variable,
                              selectmode=select_mode,
                              exportselection=stay_selected_when_unfocused,
                              relief=backdrop,
                              height=height,
                              width=width,
                              state=state
                              )
    return listbox


def dragdrop_listbox_setup(parent, list_variable=None, stay_selected_when_unfocused=None, backdrop=None, height=None, width=None, state=None):
    """
    tkinter listbox with dragable items for reordering
    Use tkinter type variables when using list_variable
    :param parent:
    :param saveTo_variable:
    :param stay_selected_when_unfocused:
    :param backdrop: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]
    :param height:
    :param width:
    :return:
    """
    class dragdrop_listbox(tkinter.Listbox):
        def __init__(self):
            tkinter.Listbox.__init__(self,
                                     parent,
                                     listvariable=list_variable,
                                     selectmode="single",
                                     exportselection=stay_selected_when_unfocused,
                                     relief=backdrop,
                                     height=height,
                                     width=width,
                                     state=state
                                     )
            self.held_index = None
            self.bind("<Button-1>", self.get_selected_index)
            self.bind("<B1-Motion>", self.shift_item)

        def get_selected_index(self, event):
            self.held_index = self.nearest(event.y)

        def shift_item(self, event):
            idx = self.nearest(event.y)
            if idx != self.held_index:
                item = self.get(self.held_index)
                self.delete(self.held_index)
                self.insert(idx, item)
                self.held_index = idx

    return dragdrop_listbox()


def progressbar_setup(parent, orientation, length, max_value, progress_mode):
    progressbar = ttk.Progressbar(parent,
                                  orient=orientation,
                                  length=length,
                                  value=max_value,
                                  mode=progress_mode
                                  )


def radiobutton_setup(parent, display_text: str=None, saveValueTo_variable=None, value=None, width=None, padding=None, state=None):
    """
    Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
    """
    radiobutton = ttk.Radiobutton(parent,
                                  text=display_text,
                                  variable=saveValueTo_variable,
                                  value=value,
                                  width=width,
                                  padding=padding,
                                  state=state
                                  )
    return radiobutton


def spinbox_setup(parent, start_value=None, end_value=None, values=None, increment=None, saveTo_variable=None, font=None, width=None, state=None):
    """
    values overrides from_/to/increment
    Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
    :param parent:
    :param start_value:
    :param end_value:
    :param values:
    :param increment:
    :param width:
    :param state:
    :return:
    """
    spinbox = ttk.Spinbox(parent,
                          values=values,
                          from_=start_value,
                          to=end_value,
                          increment=increment,
                          textvariable=saveTo_variable,
                          font=font,
                          width=width,
                          state=state
                          )
    return spinbox


def scrollbar_frame_setup(parent, height, width, sticky_scrollframe: str="NSEW", sticky_content: str="NSEW"):
    """
    tkinter frame with scrollbars
    return: list[canvas_frame, canvas, content_frame]\n
    hierarchy: canvas_frame --> canvas --> content_frame\n
    Instructions:\n
    Create the desired content inside content_frame\n
    After content_frame is set up, use the following\n
    [canvas_frame].update_idletasks()\n
    [canvas].configure(scrollregion=[canvas].bbox("all"))
    """
    canvas_frame = frame_setup(parent, width=width, height=height)
    canvas_frame.grid(column=0, row=1, sticky=sticky_scrollframe)
    canvas_frame.grid_columnconfigure(0, weight=1)
    canvas_frame.grid_rowconfigure(0, weight=1)
    canvas_frame.grid_propagate(False)

    # canvas_frame --> canvas
    canvas = tkinter.Canvas(canvas_frame)
    canvas.grid(column=0, row=0, sticky=sticky_content)

    # v_scrollbar linked to canvas
    v_scrollbar = ttk.Scrollbar(canvas_frame, orient="vertical", command=canvas.yview)
    v_scrollbar.grid(column=1, row=0, sticky='ns')
    canvas.configure(yscrollcommand=v_scrollbar.set)

    # h_scrollbar linked to canvas
    h_scrollbar = ttk.Scrollbar(canvas_frame, orient="horizontal", command=canvas.xview)
    h_scrollbar.grid(column=0, row=1, sticky='we')
    canvas.configure(xscrollcommand=h_scrollbar.set)

    # canvas_frame --> canvas --> frame
    content_frame = ttk.Frame(canvas)
    content_frame.grid(column=0, row=0)
    canvas.create_window((0, 0), window=content_frame, anchor='nw')

    return canvas_frame, canvas, content_frame
