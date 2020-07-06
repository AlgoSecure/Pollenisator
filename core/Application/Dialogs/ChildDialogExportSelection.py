"""ChildDialogExportSelection class
Ask the user to select fields and returns the selected options"""
import tkinter as tk
import tkinter.ttk as ttk
from core.Forms.FormPanel import FormPanel
from core.Views.ViewElement import ViewElement


class ChildDialogExportSelection:
    """
    Open a child dialog of a tkinter application to ask the user to select fields between many.
    """

    def __init__(self, parent, keys):
        """
        Open a child dialog of a tkinter application to ask details about
        an export of treeview items.

        Args:
            parent: the tkinter parent view to use for this window construction.
            keys: The keys to export
        """
        self.rvalue = None
        self.parent = parent
        self.app = tk.Toplevel(parent)
        self.app.title("Export selection")
        appFrame = ttk.Frame(self.app)
        self.form = FormPanel()
        self.form.addFormChecklist("Fields", sorted(keys), [])
        self.form.addFormButton("Export", self.onOk)
        self.rvalue = None
        self.form.constructView(appFrame)
        appFrame.pack(ipadx=10, ipady=10)
        self.app.transient(parent)
        self.app.wait_visibility()
        self.app.grab_set()

    def onOk(self, _event=None):
        """Called the the Export button is pressed.
        return a list of strings corresponding to the selected fields.
        
        Args:
            _event: not used but mandatory"""
        res, msg = self.form.checkForm()
        if res:
            form_values = self.form.getValue()
            form_values_as_dicts = ViewElement.list_tuple_to_dict(form_values)
            mfields = form_values_as_dicts["Fields"]
            fields = [k for k, v in mfields.items() if v == 1]
            self.rvalue = fields
            self.app.destroy()
        else:
            tk.messagebox.showwarning(
                "Form not validated", msg, parent=self.app)
