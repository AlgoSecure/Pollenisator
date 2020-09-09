"""Defines a dialog window for filling a tool settings"""

import tkinter as tk
import tkinter.ttk as ttk
from core.Forms.FormPanel import FormPanel
from core.Components.Utils import listPlugin
from core.Views.ViewElement import ViewElement

class ChildDialogEditCommandSettings:
    """
    Open a child dialog of a tkinter application to fill settings for a command
    """

    def __init__(self, parent, displayMsg="Choose a database to open:", default=None):
        """
        Open a child dialog of a tkinter application to ask a combobox option.

        Args:
            parent: the tkinter parent view to use for this window construction.
            options: A list of string correspondig to options of the combobox
            displayMsg: The message that will explain to the user what he is choosing.
            default: Choose a default selected option (one of the string in options). default is None
        """
        self.app = tk.Toplevel(parent)
        self.app.title("Upload result file")
        self.rvalue = None
        self.parent = parent
        appFrame = ttk.Frame(self.app)
        self.form = FormPanel()
        self.form.addFormLabel(displayMsg, side=tk.TOP)
        optionsFrame = self.form.addFormPanel(grid=True)
        optionsFrame.addFormLabel("Remote bin path", row=0, column=0)
        optionsFrame.addFormStr("bin", r".+", row=0, column=1)
        optionsFrame.addFormLabel("Plugin", row=1, column=0)
        optionsFrame.addFormCombo("plugin", tuple(listPlugin()), row=1, column=1)
        self.form.addFormButton("Cancel", self.onError)
        self.form.addFormButton("OK", self.onOk)
        self.form.constructView(appFrame)
        appFrame.pack(ipadx=10, ipady=10)
        self.app.transient(parent)
        try:
            self.app.grab_set()
        except tk.TclError:
            pass

    def onOk(self, _event):
        """
        Called when the user clicked the validation button. Set the rvalue attributes to the value selected and close the window.
        """
        # send the data to the parent
        res, msg = self.form.checkForm()
        if not res:
            tk.messagebox.showwarning(
                "Form not validated", msg, parent=self.app)
            return
        form_values = self.form.getValue()
        form_values_as_dicts = ViewElement.list_tuple_to_dict(form_values)
        self.rvalue = (form_values_as_dicts["bin"], form_values_as_dicts["plugin"])
        self.app.destroy()

    def onError(self, _event=None):
        """
        Close the dialog and set rvalue to None
        """
        self.rvalue = None
        self.app.destroy()
