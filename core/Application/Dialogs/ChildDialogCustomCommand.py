"""Deprecated.
Ask the user to enter a command and select a worker and plugin to launch it."""
import tkinter as tk
import tkinter.ttk as ttk
from core.Components.Utils import listPlugin


class ChildDialogCustomCommand:
    """
    Open a child dialog of a tkinter application to ask details about
    a custom command to launch on target.
    """

    def __init__(self, parent, workers, default_worker="localhost"):
        """
        Open a child dialog of a tkinter application to ask details about
        a custom command to launch on target.

        Args:
            parent: the tkinter parent view to use for this window construction.
            workers: A list of workers registered.
            default_worker: a worker to be selected by default.
        """
        self.app = tk.Toplevel(parent)
        appFrame = ttk.Frame(self.app)
        self.app.resizable(False, False)
        self.rvalue = None
        self.parent = parent
        lbl = ttk.Label(appFrame, text="Enter the custom command Name")
        lbl.pack()
        self.ent_customCommandName = ttk.Entry(appFrame, width="50")
        self.ent_customCommandName.pack()
        lbl = ttk.Label(
            appFrame, text="Enter the custom command to launch")
        lbl.pack()
        self.ent_customCommand = ttk.Entry(appFrame, width="50")
        self.ent_customCommand.pack()
        lbl2 = ttk.Label(appFrame, text="Select the parser:")
        lbl2.pack()
        parsers = listPlugin()
        self.box_template = ttk.Combobox(
            appFrame, values=tuple(parsers), state="readonly")
        self.box_template.set("default.py")
        self.box_template.pack()
        lbl3 = ttk.Label(appFrame, text="Select the worker:")
        lbl3.pack()
        self.box_workers = ttk.Combobox(
            appFrame, values=tuple(workers), state="readonly")
        self.box_workers.set(default_worker)
        self.box_workers.pack()
        self.ok_button = ttk.Button(appFrame, text="OK", command=self.onOk)
        self.ok_button.pack(side=tk.BOTTOM, pady=5)
        appFrame.pack(ipady=10, ipadx=10)
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
        self.rvalue = (self.ent_customCommandName.get(), self.ent_customCommand.get(
        ), self.box_template.get(), self.box_workers.get())
        self.app.destroy()
