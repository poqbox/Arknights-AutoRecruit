import tkinter
from tkinter import ttk
from typing import Literal


class MainWindow(tkinter.Tk):
    def __init__(self, title: str, window_size, min_size=None, max_size=None,
                 resizable_width=True, resizable_height=True):
        """
        Everything will be created within this object\n
        Widgets can be either packed or gridded, but not combined
        """

        # extends functionality from tkinter.Tk
        super().__init__()
        self.title(title)
        if isinstance(window_size, str):
            self.geometry(window_size)
        else:
            self.geometry("x".join(str(_) for _ in window_size[0:2]))
        if min_size:
            if isinstance(min_size, str):
                xy = min_size.split("x")
                self.minsize(int(xy[0]), int(xy[1]))
            else:
                self.minsize(min_size[0], min_size[1])
        if max_size:
            if isinstance(max_size, str):
                xy = max_size.split("x")
                self.maxsize(int(xy[0]), int(xy[1]))
            else:
                self.maxsize(max_size[0], max_size[1])
        self.resizable(width=resizable_width, height=resizable_height)


Tk = MainWindow


class SubWindow(tkinter.Toplevel):
    def __init__(self, parent, title: str, window_size, min_size=None, max_size=None,
                 resizable_width=True, resizable_height=True,
                 background_color=None, cursor_shape=None, pad_x=None, pad_y=None):
        """Creates a window over the parent window"""

        # extends functionality from tkinter.Toplevel
        super().__init__(master=parent,
                         background=background_color,
                         cursor=cursor_shape,
                         padx=pad_x,
                         pady=pad_y
                         )
        self.title(title)
        if isinstance(window_size, str):
            self.geometry(window_size)
        else:
            self.geometry("x".join(str(_) for _ in window_size[0:2]))
        if min_size:
            if isinstance(min_size, str):
                xy = min_size.split("x")
                self.minsize(int(xy[0]), int(xy[1]))
            else:
                self.minsize(min_size[0], min_size[1])
        if max_size:
            if isinstance(max_size, str):
                xy = max_size.split("x")
                self.maxsize(int(xy[0]), int(xy[1]))
            else:
                self.maxsize(max_size[0], max_size[1])
        self.resizable(width=resizable_width, height=resizable_height)


Toplevel = SubWindow


def swap_frame(current_frame: ttk.Frame, new_frame: ttk.Frame, _use_with_lambda_function=False):
    """
    Only works with frames configured with grids
    """
    def reference_func():
        current_frame.grid_remove()
        new_frame.grid()

    if _use_with_lambda_function:
        reference_func()
    else:
        return reference_func


def grid_setup(widget, columns_list, rows_list):
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


def add_grid_column(widget, index, min_size=None, pad=None, uniform=None, weight=None):
    widget.columnconfigure(index=index,
                           minsize=min_size,
                           pad=pad,
                           uniform=uniform,
                           weight=weight
                           )


def add_grid_row(widget, index, min_size=None, pad=None, uniform=None, weight=None):
    widget.rowconfigure(index=index,
                        minsize=min_size,
                        pad=pad,
                        uniform=uniform,
                        weight=weight
                        )


def grid_into(widget, column: int, row: int, sticky: str = None, columnspan: int = None, rowspan: int = None,
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
    return lambda: widget_grid(widget, column, row, sticky, columnspan, rowspan, interior_padding_x, interior_padding_y,
                               exterior_padding_x, exterior_padding_y)


def pack_into(widget, side, anchor,
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


class Frame(ttk.Frame):
    def __init__(self, parent,
                 width=None, padding=None, height=None, take_focus=None, style=None, backdrop=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        :param backdrop: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]
        """

        # extends functionality from ttk.Frame
        super().__init__(master=parent,
                         cursor=cursor_shape,
                         height=height,
                         padding=padding,
                         relief=backdrop,
                         style=style,
                         takefocus=take_focus,
                         width=width
                         )
        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class Button(ttk.Button):
    def __init__(self, parent, display_text: str = None, display_image=None, function_when_clicked=None,
                 width=None, display_padding=None, state=None, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use "lambda: [function]" when using the function parameter
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # extends functionality from ttk.Button
        super().__init__(master=parent,
                         command=function_when_clicked,
                         cursor=cursor_shape,
                         image=display_image,
                         padding=display_padding,
                         state=state,
                         style=style,
                         takefocus=take_focus,
                         text=display_text,
                         width=width
                         )
        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class Checkbutton(ttk.Checkbutton):
    def __init__(self, parent, display_text: str = None, display_image=None, saveValueTo_variable=None,
                 value_when_checked=1, value_when_unchecked=0, function_when_checked=None,
                 width=None, padding=None, state=None, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
        Use "lambda: [function]" when using the function parameter
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # extends functionality from ttk.Checkbutton
        super().__init__(master=parent,
                         command=function_when_checked,
                         cursor=cursor_shape,
                         image=display_image,
                         offvalue=value_when_unchecked,
                         onvalue=value_when_checked,
                         padding=padding,
                         state=state,
                         style=style,
                         takefocus=take_focus,
                         text=display_text,
                         variable=saveValueTo_variable,
                         width=width
                         )
        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class Combobox(ttk.Combobox):
    def __init__(self, parent, values, saveValueTo_variable=None,
                 validation_test: Literal["none", "focus", "focusin", "focusout", "key", "all"] = "none",
                 function_for_testing_validation=None, function_when_invalid=None,
                 text_alignment=None, font=None, text_color=None, background_color=None,
                 width=None, state=None, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # extends functionality from ttk.Combobox
        super().__init__(master=parent,
                         background=background_color,
                         cursor=cursor_shape,
                         font=font,
                         foreground=text_color,
                         invalidcommand=function_when_invalid,
                         justify=text_alignment,
                         state=state,
                         style=style,
                         takefocus=take_focus,
                         textvariable=saveValueTo_variable,
                         validate=validation_test,
                         validatecommand=function_for_testing_validation,
                         values=values,
                         width=width
                         )
        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class Entry(ttk.Entry):
    def __init__(self, parent, saveValueTo_variable=None,
                 validation_test: Literal["none", "focus", "focusin", "focusout", "key", "all"] = "none",
                 function_for_testing_validation=None, function_when_invalid=None,
                 font=None, text_color=None, background_color=None,
                 width=None, state=None, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
        Use "lambda: [function]" when using the function_for_testing_validation and function_when_invalid parameters
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # extends functionality from ttk.Entry
        super().__init__(master=parent,
                         background=background_color,
                         cursor=cursor_shape,
                         font=font,
                         foreground=text_color,
                         invalidcommand=function_when_invalid,
                         state=state,
                         style=style,
                         takefocus=take_focus,
                         textvariable=saveValueTo_variable,
                         validate=validation_test,
                         validatecommand=function_for_testing_validation,
                         width=width
                         )
        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class Entry_with_default_value(ttk.Entry):
    def __init__(self, parent, default_value="", saveValueTo_variable=None,
                 font=None, focusIn_text_color="black", focusOut_text_color="grey", background_color=None,
                 width=None, state=None, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # extends functionality from ttk.Entry
        super().__init__(master=parent,
                         background=background_color,
                         cursor=cursor_shape,
                         font=font,
                         foreground=focusOut_text_color,
                         state=state,
                         style=style,
                         takefocus=take_focus,
                         textvariable=saveValueTo_variable,
                         width=width
                         )
        self.saveTo_variable = saveValueTo_variable
        self.default_value = default_value
        self.focusOut_text_color = focusOut_text_color
        self.focusIn_text_color = focusIn_text_color
        self.configure(foreground=self.focusOut_text_color)
        self.insert(0, default_value)
        self.bind("<FocusIn>", lambda e: self.focus_in())
        self.bind("<FocusOut>", lambda e: self.focus_out())

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )

    def focus_in(self):
        if self.saveTo_variable.get() == self.default_value:
            self.configure(foreground=self.focusIn_text_color)
            self.delete(0, "end")

    def focus_out(self):
        if not self.saveTo_variable.get() or self.saveTo_variable.get() == self.default_value:
            self.configure(foreground=self.focusOut_text_color)
            self.delete(0, "end")
            self.insert(0, self.default_value)


class Label(ttk.Label):
    def __init__(self, parent, display_text: str = None,
                 text_alignment: Literal["left", "center", "right"] = "left", font=None, text_color=None, background_color=None,
                 width=None, text_padding=None, state=None, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # text_alignment == "left"
        justify = text_alignment
        anchor = "w"
        if text_alignment == "center":
            justify = text_alignment
            anchor = "center"
        elif text_alignment == "right":
            justify = text_alignment
            anchor = "e"

        # extends functionality from ttk.Label
        super().__init__(master=parent,
                         anchor=anchor,
                         background=background_color,
                         cursor=cursor_shape,
                         font=font,
                         foreground=text_color,
                         justify=justify,
                         padding=text_padding,
                         state=state,
                         style=style,
                         takefocus=take_focus,
                         text=display_text,
                         width=width
                         )

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class Listbox(tkinter.Listbox):
    def __init__(self, parent, list_variable=None, select_mode: Literal["single", "multiple"] = "single",
                 stay_selected_when_unfocused=False,
                 font=None, text_color=None, background_color=None,
                 width=None, height=None, state=None, take_focus=None, backdrop=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        :param backdrop: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]
        """

        # extends functionality from tkinter.Listbox
        super().__init__(master=parent,
                         background=background_color,
                         cursor=cursor_shape,
                         exportselection=not stay_selected_when_unfocused,
                         font=font,
                         foreground=text_color,
                         height=height,
                         listvariable=list_variable,
                         relief=backdrop,
                         selectmode=select_mode,
                         state=state,
                         takefocus=take_focus,
                         width=width
                         )

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class Listbox_with_drag_drop(tkinter.Listbox):
    def __init__(self, parent, list_variable=None, select_mode: Literal["single", "multiple"] = "single",
                 stay_selected_when_unfocused=False,
                 font=None, text_color=None, background_color=None,
                 width=None, height=None, state=None, take_focus=None, backdrop=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        :param backdrop: Literal["raised", "sunken", "flat", "ridge", "solid", "groove"]
        """

        # extends functionality from tkinter.Listbox
        super().__init__(master=parent,
                         background=background_color,
                         cursor=cursor_shape,
                         exportselection=not stay_selected_when_unfocused,
                         font=font,
                         foreground=text_color,
                         height=height,
                         listvariable=list_variable,
                         relief=backdrop,
                         selectmode=select_mode,
                         state=state,
                         takefocus=take_focus,
                         width=width
                         )
        self.held_index = None
        self.bind("<Button-1>", self._get_selected_index)
        self.bind("<B1-Motion>", self._shift_item)

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )

    def _get_selected_index(self, event):
        self.held_index = self.nearest(event.y)

    def _shift_item(self, event):
        idx = self.nearest(event.y)
        if idx != self.held_index:
            item = self.get(self.held_index)
            self.delete(self.held_index)
            self.insert(idx, item)
            self.held_index = idx


class _Menu(tkinter.Menu):
    def __init__(self, parent):
        super().__init__(master=parent,
                         tearoff=0
                         )

    def add_option(self, label, function=None, keybind=None, keybind_via_character_index: int = None):
        self.add_command(label=label, command=function, accelerator=keybind, underline=keybind_via_character_index)
        if keybind:
            self.bind_all(keybind, function)

    def insert_option(self, index, label, function=None, keybind=None, keybind_via_character_index: int = None):
        self.insert_command(index=index, label=label, command=function, accelerator=keybind,
                            underline=keybind_via_character_index)
        if keybind:
            self.bind_all(keybind, function)

    def delete_menu_items(self, start_index, end_index=None):
        """Delete menu items between INDEX1 and INDEX2 (inclusive)."""
        self.delete(index1=start_index, index2=end_index)


class Menubar(_Menu):
    def __init__(self, parent):
        """
        Use the SubMenu class to add menus to the menubar
        """

        super().__init__(parent=parent)
        parent.config(menu=self)


class SubMenu(_Menu):
    def __init__(self, parent_menu, label: str, underline=None):
        """
        Use the SubMenu class to add submenus to this menu

        disable_self() can be used to disable the menu

        disable_option() can be used to disable an option or submenu

        delete_menu_items() can be used to delete an option or submenu
        """

        super().__init__(parent=parent_menu)
        self.label = label
        parent_menu.add_cascade(menu=self, label=self.label)

    def disable_option(self, option_label):
        self.entryconfigure(option_label, state="disabled")

    def disable_self(self):
        self.nametowidget(self.winfo_parent()).entryconfigure(self.label, state="disabled")



class Notebook(ttk.Notebook):
    def __init__(self, parent,
                 width=None, height=None, padding=None, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use [notebook].add() to add tabs
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # extends functionality from ttk.Notebook
        super().__init__(master=parent,
                         cursor=cursor_shape,
                         height=height,
                         padding=padding,
                         style=style,
                         takefocus=take_focus,
                         width=width
                         )

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class PanedFrame(ttk.Panedwindow):
    def __init__(self, parent, orientation: Literal["vertical", "horizontal"],
                 width=None, height=None, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use [PanedFrame].add() to add resizable widgets
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # extends functionality from ttk.Panedwindow
        super().__init__(master=parent,
                         cursor=cursor_shape,
                         height=height,
                         orient=orientation,
                         style=style,
                         takefocus=take_focus,
                         width=width
                         )

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


PanedWindow = Panedwindow = PanedFrame


class Progressbar(ttk.Progressbar):
    def __init__(self, parent, orientation, length, max_value=100,
                 style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use increment_value() or set_value() to control the progressbar
        Use get_value() to get the current value
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """
        self.progress_value = tkinter.IntVar()

        # extends functionality from ttk.Progressbar
        super().__init__(master=parent,
                         cursor=cursor_shape,
                         length=length,
                         mode="determinate",
                         orient=orientation,
                         style=style,
                         value=max_value,
                         variable=self.progress_value
                         )

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )

    def increment_value(self, increment):
        self.step(increment)

    def set_value(self, value):
        self.progress_value.set(value)

    def get_value(self):
        self.progress_value.get()


class Radiobutton(ttk.Radiobutton):
    def __init__(self, parent, display_text: str = None, value_when_selected=None, saveValueTo_variable=None,
                 function_when_selected=None,
                 width=None, padding=None, state=None, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
        Use "lambda: [function]" when using the function parameter
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # extends functionality from ttk.Radiobutton
        super().__init__(master=parent,
                         command=function_when_selected,
                         cursor=cursor_shape,
                         padding=padding,
                         state=state,
                         style=style,
                         takefocus=take_focus,
                         text=display_text,
                         value=value_when_selected,
                         variable=saveValueTo_variable,
                         width=width
                         )

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class Separator(ttk.Separator):
    def __init__(self, parent, orientation, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # extends functionality from ttk.Separator
        super().__init__(master=parent,
                         cursor=cursor_shape,
                         orient=orientation,
                         style=style,
                         takefocus=take_focus
                         )

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class Spinbox(ttk.Spinbox):
    def __init__(self, parent, start_value=None, end_value=None, values=None, increment=None, saveValueTo_variable=None,
                 text_alignment=None, font=None, text_color=None, background_color=None,
                 width=None, state=None, take_focus=None, style=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        values overrides from_/to/increment
        Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
        """

        # extends functionality from ttk.Spinbox
        super().__init__(master=parent,
                         background=background_color,
                         cursor=cursor_shape,
                         font=font,
                         foreground=text_color,
                         from_=start_value,
                         increment=increment,
                         justify=text_alignment,
                         to=end_value,
                         textvariable=saveValueTo_variable,
                         state=state,
                         style=style,
                         takefocus=take_focus,
                         values=values,
                         width=width
                         )

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )


class Text(tkinter.Text):
    def __init__(self, parent, text:str = None, wrap_on=None, font=None, text_color=None, background_color=None,
                 width=None, height=None, state=None, take_focus=None, backdrop=None, cursor_shape=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        # extends functionality from tkinter.Text
        super().__init__(master=parent,
                         background=background_color,
                         cursor=cursor_shape,
                         font=font,
                         foreground=text_color,
                         height=height,
                         relief=backdrop,
                         state=state,
                         takefocus=take_focus,
                         width=width,
                         wrap=wrap_on
                         )

        if grid_column and grid_row:
            self.grid_configure(column=grid_column,
                                columnspan=grid_columnspan,
                                row=grid_row,
                                rowspan=grid_rowspan,
                                sticky=grid_sticky,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.pack_configure(side=pack_side,
                                anchor=pack_anchor,
                                fill=pack_fill,
                                expand=pack_expand,
                                ipadx=ipad_x,
                                ipady=ipad_y,
                                padx=pad_x,
                                pady=pad_y
                                )
        if text:
            self.insert("end", text)


class Frame_with_scrollbar(ttk.Frame):
    def __init__(self, parent,
                 sticky_scrollframe: str = "NSEW", sticky_content: str = "NSEW", width=None, height=None,
                 grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                 pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                 ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
        """
        After content_frame is set up, use the finish_scrollbar_frame_setup() method
        hierarchy: canvas_frame --> canvas --> content_frame\n
        Use either the grid_ or pack_ parameters to make the widget appear,
        or use the grid_configure or pack_configure functions
        """

        self.canvas_frame = ttk.Frame(parent, width=width, height=height)
        if grid_column and grid_row:
            self.canvas_frame.grid_configure(column=grid_column,
                                             columnspan=grid_columnspan,
                                             row=grid_row,
                                             rowspan=grid_rowspan,
                                             sticky=sticky_scrollframe,
                                             ipadx=ipad_x,
                                             ipady=ipad_y,
                                             padx=pad_x,
                                             pady=pad_y
                                             )
        elif pack_side or pack_anchor or pack_fill or pack_expand:
            self.canvas_frame.pack_configure(side=pack_side,
                                             anchor=pack_anchor,
                                             fill=pack_fill,
                                             expand=pack_expand,
                                             ipadx=ipad_x,
                                             ipady=ipad_y,
                                             padx=pad_x,
                                             pady=pad_y)

        # configure canvas_frame grid
        self.canvas_frame.grid_columnconfigure(0, weight=1)
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_propagate(False)

        # place canvas in frame
        self.canvas = tkinter.Canvas(self.canvas_frame)
        self.canvas.grid(column=0, row=0, sticky=sticky_content)

        # link v_scrollbar to canvas
        v_scrollbar = ttk.Scrollbar(self.canvas_frame, orient="vertical", command=self.canvas.yview)
        v_scrollbar.grid(column=1, row=0, sticky='ns')
        self.canvas.configure(yscrollcommand=v_scrollbar.set)

        # link h_scrollbar to canvas
        h_scrollbar = ttk.Scrollbar(self.canvas_frame, orient="horizontal", command=self.canvas.xview)
        h_scrollbar.grid(column=0, row=1, sticky='we')
        self.canvas.configure(xscrollcommand=h_scrollbar.set)

        # place a frame in the canvas
        super().__init__(master=self.canvas,
                         height=height,
                         width=width
                         )
        super().grid(column=0, row=0)
        self.canvas.create_window((0, 0), window=self, anchor='nw')

    def grid_configure(self, cnf={}, **kw):
        self.canvas_frame.grid(cnf, **kw)

    grid = configure = config = grid_configure

    def grid_remove(self):
        self.canvas_frame.grid_remove()

    def finish_scrollbar_frame_setup(self):
        self.canvas_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))


class Compacted:
    class MainWindow(MainWindow):
        def __init__(self, title: str, window_size, min_size=None, max_size=None, resizable_width=True,
                     resizable_height=True):
            """
            Everything will be created within this object\n
            Widgets can be either packed or gridded, but not combined
            """
            super().__init__(title,
                             window_size,
                             min_size,
                             max_size,
                             resizable_width,
                             resizable_height
                             )

    class SubWindow(SubWindow):
        def __init__(self, parent, title: str, window_size, min_size=None, max_size=None, resizable_width=True,
                     resizable_height=True):
            """Creates a window over the parent window"""

            # extends functionality from tkinter.Toplevel
            super().__init__(parent,
                             title,
                             window_size,
                             min_size,
                             max_size,
                             resizable_width,
                             resizable_height
                             )

    def grid_setup(widget, columns_list, rows_list):
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

    def add_grid_column(widget, index, min_size=None, pad=None, uniform=None, weight=None):
        widget.columnconfigure(index=index,
                               minsize=min_size,
                               pad=pad,
                               uniform=uniform,
                               weight=weight
                               )

    def add_grid_row(widget, index, min_size=None, pad=None, uniform=None, weight=None):
        widget.rowconfigure(index=index,
                            minsize=min_size,
                            pad=pad,
                            uniform=uniform,
                            weight=weight
                            )

    def grid_into(widget, column: int, row: int, sticky: str = None, columnspan: int = None, rowspan: int = None,
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
        return lambda: widget_grid(widget, column, row, sticky, columnspan, rowspan, interior_padding_x,
                                   interior_padding_y,
                                   exterior_padding_x, exterior_padding_y)

    def pack_into(widget, side, anchor,
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

    class Frame(Frame):
        def __init__(self, parent,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """
            super().__init__(parent=parent,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Button(Button):
        def __init__(self, parent, display_text: str = None, display_image=None, function_when_clicked=None,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use "lambda: [function]" when using the function parameter
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """
            super().__init__(parent=parent, display_text=display_text, display_image=display_image,
                             function_when_clicked=function_when_clicked,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Checkbutton(Checkbutton):
        def __init__(self, parent, display_text: str = None, display_image=None, saveValueTo_variable=None,
                     value_when_checked=1, value_when_unchecked=0, function_when_checked=None,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
            Use "lambda: [function]" when using the function parameter
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """
            super().__init__(parent=parent, display_text=display_text, display_image=display_image,
                             saveValueTo_variable=saveValueTo_variable,
                             value_when_unchecked=value_when_unchecked, value_when_checked=value_when_checked,
                             function_when_checked=function_when_checked,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Combobox(Combobox):
        def __init__(self, parent, values, saveValueTo_variable=None,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """
            super().__init__(parent=parent, values=values, saveValueTo_variable=saveValueTo_variable,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Entry(Entry):
        def __init__(self, parent, saveValueTo_variable=None,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
            Use "lambda: [function]" when using the function_for_testing_validation and function_when_invalid parameters
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """
            super().__init__(parent=parent, saveValueTo_variable=saveValueTo_variable,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Entry_with_default_value(Entry_with_default_value):
        def __init__(self, parent, default_value="", saveValueTo_variable=None,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """
            super().__init__(parent=parent, default_value=default_value, saveValueTo_variable=saveValueTo_variable,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Label(Label):
        def __init__(self, parent, display_text: str = None,
                     text_alignment=None, font=None, text_color=None, background_color=None,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """
            super().__init__(parent=parent, display_text=display_text, text_alignment=text_alignment,
                             font=font, text_color=text_color, background_color=background_color,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Listbox(Listbox):
        def __init__(self, parent, list_variable=None,
                     select_mode="single", stay_selected_when_unfocused=True,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """
            super().__init__(parent=parent, list_variable=list_variable, select_mode=select_mode,
                             stay_selected_when_unfocused=stay_selected_when_unfocused,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Progressbar(Progressbar):
        def __init__(self, parent, orientation, length, max_value=100,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """
            super().__init__(parent=parent, orientation=orientation, length=length, max_value=max_value,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Radiobutton(Radiobutton):
        def __init__(self, parent, display_text: str = None, value_when_selected=None, saveValueTo_variable=None,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
            Use "lambda: [function]" when using the function parameter
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """

            # extends functionality from ttk.Radiobutton
            super().__init__(parent=parent, display_text=display_text,
                             value_when_selected=value_when_selected, saveValueTo_variable=saveValueTo_variable,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Spinbox(Spinbox):
        def __init__(self, parent, start_value=None, end_value=None, values=None, increment=None,
                     saveValueTo_variable=None,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            values overrides from_/to/increment
            Use tkinter type variables when using saveValueTo_variable, such as tkinter.StringVar(), and use .get() to retrieve the value
            """

            # extends functionality from ttk.Spinbox
            super().__init__(parent=parent, start_value=start_value, end_value=end_value, values=values,
                             increment=increment, saveValueTo_variable=saveValueTo_variable,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y
                             )

    class Text(Text):
        def __init__(self, parent, text=None, wrap_on=None,
                     grid_column=None, grid_row=None, grid_columnspan=None, grid_rowspan=None, grid_sticky="NSEW",
                     pack_side=None, pack_anchor=None, pack_fill=None, pack_expand=None,
                     ipad_x=None, ipad_y=None, pad_x=None, pad_y=None):
            """
            Use either the grid_ or pack_ parameters to make the widget appear,
            or use the grid_configure or pack_configure functions
            """
            super().__init__(parent=parent, text=text, wrap_on=wrap_on,
                             grid_column=grid_column, grid_row=grid_row,
                             grid_columnspan=grid_columnspan, grid_rowspan=grid_rowspan, grid_sticky=grid_sticky,
                             pack_side=pack_side, pack_anchor=pack_anchor, pack_fill=pack_fill, pack_expand=pack_expand,
                             ipad_x=ipad_x, ipad_y=ipad_y, pad_x=pad_x, pad_y=pad_y

                             )
