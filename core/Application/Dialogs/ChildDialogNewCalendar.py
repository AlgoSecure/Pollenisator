"""Help the user to create a new pentest database.
"""
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from core.Forms.FormPanel import FormPanel
from core.Views.ViewElement import ViewElement
from core.Components.Settings import Settings


class ChildDialogNewCalendar:
    """
    Open a child dialog of a tkinter application to ask details about
    a new pentest database to create.
    """

    def __init__(self, parent, default):
        """
        Open a child dialog of a tkinter application to ask details about
        the new pentest.

        Args:
            parent: the tkinter parent view to use for this window construction.
        """
        self.app = tk.Toplevel(parent)
        self.app.resizable(False, False)
        self.rvalue = None
        self.parent = parent
        mainFrame = ttk.Frame(self.app)
        self.form = FormPanel()
        form1 = self.form.addFormPanel(grid=True, side=tk.TOP, fill=tk.X)
        form1.addFormLabel("Database name")
        form1.addFormStr("Database name", r"^\S+$", default=default.get("name", ""), width=50, column=1)
        types = list(Settings.getPentestTypes().keys())
        if types:
            form1.addFormLabel("Pentest type", row=1)
            form1.addFormCombo(
                "Pentest type", types, default=default.get("type", types[0]), row=1, column=1)
        form1.addFormLabel("Starting", row=2)
        form1.addFormDate("startd", parent, default.get("start", datetime.strftime(datetime.now(), "%d/%m/%Y %H:%M:%S")), "%d/%m/%Y %H:%M:%S", row=2, column=1)
        form1.addFormLabel("Ending", row=3)
        form1.addFormDate("endd", parent, default.get("end", "31/12/2099 00:00:00"),
                          "%d/%m/%Y %H:%M:%S", row=3, column=1)
        form2 = self.form.addFormPanel(grid=True, side=tk.TOP, fill=tk.X, pady=5)
        form2.addFormLabel("Scope", pady=5)
        form2.addFormText(
            "Scope", "", default.get("scope", ""), height=5, column=1, sticky=tk.E, pady=5)
        form2.addFormHelper(
            "You can declare network ip as IP/MASKSIZE, ips or domains", column=2, sticky=tk.W)
        form2.addFormLabel("Pentester names", row=1, sticky=tk.E)
        form2.addFormText(
            "Pentester names", "", default.get("pentesters", ""),  row=1, column=1, sticky=tk.W, height=3, pady=5)
        form3 = self.form.addFormPanel(side=tk.TOP, fill=tk.X, pady=5)
        default_settings = []
        for key, val in default.get("settings", {}).items():
            if val == 1:
                default_settings.append(key)
        form3.addFormChecklist("Settings", ["Add domains whose IP are in scope",
                                            "Add domains who have a parent domain in scope", "Add all domains found"], default_settings, side=tk.TOP, fill=tk.X, pady=5)
        form3.addFormButton("Create", self.onOk, side=tk.BOTTOM)
        self.form.constructView(mainFrame)
        self.form.setFocusOn("Database name")
        mainFrame.pack(fill=tk.BOTH, ipadx=10, ipady=10)
        self.app.transient(parent)
        self.app.wait_visibility()
        self.app.grab_set()

    def onOk(self, _event):
        """
        Called when the user clicked the validation button. Set the rvalue attributes to the value selected and close the window.
        
        Args:
            _event: not used but mandatory
        """
        # send the data to the parent
        res, msg = self.form.checkForm()
        if res:
            form_values = self.form.getValue()
            form_values_as_dicts = ViewElement.list_tuple_to_dict(form_values)
            self.rvalue = {"name": form_values_as_dicts["Database name"],
                           "type": form_values_as_dicts.get("Pentest type", ""),
                           "start": form_values_as_dicts["startd"],
                           "end": form_values_as_dicts["endd"],
                           "settings": form_values_as_dicts["Settings"],
                           "scope": form_values_as_dicts["Scope"],
                           "pentesters": form_values_as_dicts["Pentester names"]}
            self.app.destroy()
        else:
            tk.messagebox.showwarning(
                "Form not validated", msg, parent=self.app)
