"""Describe tkinter checkbox with default common args"""

import tkinter as tk
import tkinter.ttk as ttk
from core.Forms.Form import Form


class FormCheckbox(Form):
    """
    Form field representing a checkbox.
    Default setted values: 
        if pack : padx = pady = 5, side = right
        if grid: row = column = 0 sticky = "west"
    """
    def __init__(self, name, text, default, **kwargs):
        """
        Constructor for a form checkbox
        
        Args:
            name: the checkbox name (id).
            text: the text on the checkbox
            default: boolean indicating if the checkbox should be checked by default.
            kwargs: same keyword args as you would give to ttk.CheckButton
        """
        super().__init__(name)
        self.text = text
        self.default = default
        self.kwargs = kwargs
        self.chk = None

    def constructView(self, parent):
        """
        Create the checkbox view inside the parent view given

        Args:
            parent: parent form panel.
        """
        self.val = tk.IntVar()
        if self.default:
            self.val.set(1)
        else:
            self.val.set(0)
        self.chk = ttk.Checkbutton(
            parent.panel, text=self.text, variable=self.val)
        if parent.gridLayout:
            self.chk.grid(row=self.getKw("row", 0), column=self.getKw("column", 0), sticky=self.getKw("sticky", tk.W), **self.kwargs)
        else:
            self.chk.pack(side=self.getKw("side", "right"), padx=self.getKw("padx", 10), pady=self.getKw("pady", 5), **self.kwargs)

    def getValue(self):
        """
        Return the form value. Required for a form.

        Returns:
            Return True if the checkbox was checked, False otherwise.
        """
        return self.val.get() == 1

    def checkForm(self):
        """
        Check if this form is correctly filled. A checkbox cannot be malformed.

        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }
        """
        return True, ""

    def setFocus(self):
        """Set the focus to the ttk checkbutton."""
        self.chk.focus_set()