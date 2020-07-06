"""Widget with an entry to type a date and a calendar button to choose a date."""

import tkinter as tk
from tkinter import ttk
import datetime as datetime
from core.Forms.Form import Form
from PIL import ImageTk, Image
from core.Components.Utils import getIconDir
from core.Application.Dialogs.ChildDialogDate import ChildDialogDate

class FormDate(Form):
    """
    Form field representing a date.
    Default setted values: 
        state="readonly"
        if pack : padx = pady = 5, side = "right"
        if grid: row = column = 0 sticky = "west"
    """
    def __init__(self, name, root, default="", dateformat='%d/%m/%Y %H:%M:%S', **kwargs):
        """
        Constructor for a form checkbox

        Args:
            name: the date name (id).
            root: the tkinter root window
            default: a list of string that should be prechecked if in the choice list.
            dateformat: a date format as a string see datetime.strptime documentation.
            kwargs: same keyword args as you would give to ttk.Frame
        """
        super().__init__(name)
        self.dateformat = dateformat
        self.default = default
        self.root = root
        self.kwargs = kwargs
        self.entry = None
        FormDate.img_class = ImageTk.PhotoImage(
            Image.open(getIconDir()+"date.png"))

    def constructView(self, parent):
        """
        Create the date view inside the parent view given

        Args:
            parent: parent FormPanel.
        """
        self.parent = parent
        self.val = tk.StringVar()
        frame = ttk.Frame(parent.panel)
        self.entry = tk.Entry(frame, textvariable=self.val)
        self.val.set(self.default)
        self.entry.bind('<Control-a>', self.selectAll)
        self.entry.grid(row=0, column=0)
        datepicker = tk.Label(frame, image=FormDate.img_class)
        datepicker.grid(row=0,column=1, padx=5)
        datepicker.bind("<Button-1>", self.showDatePicker)
        if parent.gridLayout:
            frame.grid(row=self.getKw("row", 0), column=self.getKw("column", 0), sticky=self.getKw("sticky", tk.W), **self.kwargs)
        else:
            frame.pack(side=self.getKw("side", "right"), padx=self.getKw("padx", 10), pady=self.getKw("pady", 5), **self.kwargs)

    def showDatePicker(self, _event=None):
        """Callback to start displaying the date picker calendar window
        Args:
            _event: mandatory but not used
        """
        dialog = ChildDialogDate(self.root)
        self.root.wait_window(dialog.app)
        if dialog.rvalue is not None:
            datestr = datetime.datetime.strftime(dialog.rvalue, self.dateformat)
            self.val.set(datestr)

    def selectAll(self, _event):
        """Callback to select all the text in the date Entry.
        Args:
            _event: mandatory but not used
        Returns:
            Returns the string "break" to prevent the event to be treated by the Entry, thus inserting unwanted value.
        """
        # select text
        self.entry.select_range(0, 'end')
        # move cursor to the end
        self.entry.icursor('end')
        return "break"

    def getValue(self):
        """
        Return the form value. Required for a form.

        Returns:
            Return the date as string text.
        """
        return self.val.get()

    def checkForm(self):
        """
        Check if this form is correctly filled. Check with the dateformat given in constructorn or "None".

        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }
        """
        value = self.getValue()
        if value == "None":
            return True, ""
        try:
            # exception is raised if string cannot be converted with dateformat
            datetime.datetime.strptime(value, self.dateformat)
        except ValueError:
            return False, self.name+" does not respect the date format ("+str(self.dateformat)+")"
        return True, ""

    def setFocus(self):
        """Set the focus to the ttk entry part of the widget.
        """
        self.entry.focus_set()