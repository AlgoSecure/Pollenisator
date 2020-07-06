"""Describe tkinter button with default common args"""
import tkinter as tk
import tkinter.ttk as ttk

from core.Forms.Form import Form


class FormButton(Form):
    """
    Form field representing a button.
    Default setted values: 
        if pack : padx = pady = 5, side = right
        if grid: row = column = 0 sticky = "west
    """

    def __init__(self, name, callback, **kwargs):
        """
        Constructor for a form button

        Args:
            name: the button text.
            callback: a function that will be called when the button is clicked.
            kwargs: same keyword args as you would give to ttk.Button
        """
        super().__init__(name)
        self.callback = callback
        self.kwargs = kwargs
        self.btn = None
        self.wid_kwargs = None

    def constructView(self, parent):
        """
        Create the button view inside the parent view given

        Args:
            parent: parent form panel.
        """
        self.btn = ttk.Button(parent.panel, text=self.name)
        if parent.gridLayout:
            self.btn.grid(row=self.getKw("row", 0), column=self.getKw("column", 0), sticky=self.getKw("sticky", tk.W), **self.kwargs)
        else:
            self.btn.pack(side=self.getKw("side", "right"), padx=self.getKw("padx", 5), pady=self.getKw("pady", 5), **self.kwargs)
        self.btn.bind('<Button-1>', self.callback)
        if self.wid_kwargs is not None:
            self.btn.configure(**self.wid_kwargs)

    def configure(self, **kwargs):
        """Change kwargs to given one. Must be called before constructView
        Args:
            **kwargs: any ttk Button keyword arguments."""
        self.wid_kwargs = kwargs

    def setFocus(self):
        """Set the focus to the ttk button.
        """
        self.btn.focus_set()