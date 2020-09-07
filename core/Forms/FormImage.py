"""Describe tkinter Label as image with default common args"""

import tkinter as tk
from core.Forms.Form import Form
from PIL import ImageTk, Image


class FormImage(Form):
    """
    Form field representing a label Image.
    Default setted values:
        if pack : padx = pady = 5, side = left
        if grid: row = column = 0 sticky = "East"
    """
    def __init__(self, path, **kwargs):
        """
        Constructor for a form label
        Args:
            path: the path to the image
            kwargs: same keyword args as you would give to ttk.Label
        """
        super().__init__("Image")
        self.path = path
        self.kwargs = kwargs

    def constructView(self, parent):
        """
        Create the label view inside the parent view given

        Args:
            parent: parent FormPanel.
        """
        self.img = Image.open(self.path)
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.lbl = tk.Label(parent.panel, image=self.tkimage, bg="white", justify=tk.LEFT)
        if parent.gridLayout:
            self.lbl.grid(column=self.getKw("column", 0), row=self.getKw("row", 0), sticky=self.getKw("sticky", tk.E) , padx=self.getKw("padx", 5), pady=self.getKw("pady", 5), **self.kwargs)
        else:
            self.lbl.pack(side=self.getKw("side", "left"), padx=self.getKw("padx", 10), pady=self.getKw("pady", 5), **self.kwargs)

    
    def setImage(self, newPath):
        """nothing to set so overwrite
        Args:
            _newval: not used"""
        self.path = newPath
        self.img = Image.open(newPath)
        self.tkimage = ImageTk.PhotoImage(self.img)
        self.lbl.configure(image=self.tkimage)
        self.lbl.image = self.tkimage
