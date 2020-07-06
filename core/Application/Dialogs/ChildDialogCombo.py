"""Defines a dialog window for choosing 1 between option many thourgh a combobox"""

import tkinter as tk
import tkinter.ttk as ttk


class ChildDialogCombo:
    """
    Open a child dialog of a tkinter application to ask a user a calendar name.
    """

    def __init__(self, parent, options, displayMsg="Choose a database to open:", default=None):
        """
        Open a child dialog of a tkinter application to ask a combobox option.

        Args:
            parent: the tkinter parent view to use for this window construction.
            options: A list of string correspondig to options of the combobox
            displayMsg: The message that will explain to the user what he is choosing.
            default: Choose a default selected option (one of the string in options). default is None
        """
        self.app = tk.Toplevel(parent, bg="white")
        self.app.resizable(False, False)
        appFrame = ttk.Frame(self.app)
        self.rvalue = None
        self.parent = parent
        if options is None:
            self.onError()
        lbl = ttk.Label(appFrame, text=displayMsg)
        lbl.pack(pady=5)
        self.box_template = ttk.Combobox(
            appFrame, values=tuple(options), state="readonly")
        if default is not None:
            self.box_template.set(default)
        self.box_template.pack(padx=10, pady=5)
        self.ok_button = ttk.Button(appFrame, text="OK", command=self.onOk)
        self.ok_button.pack(padx=10, pady=5)
        appFrame.pack(ipadx=10, ipady=5)
        try:
            self.app.wait_visibility()
            self.app.transient(parent)
            self.app.grab_set()
        except tk.TclError:
            pass

    def onOk(self):
        """
        Called when the user clicked the validation button. Set the rvalue attributes to the value selected and close the window.
        """
        # send the data to the parent
        self.rvalue = self.box_template.get()
        self.app.destroy()

    def onError(self):
        """
        Close the dialog and set rvalue to None
        """
        self.rvalue = None
        self.app.destroy()
