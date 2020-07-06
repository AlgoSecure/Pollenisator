"""Display a simple information for the user.
"""
import tkinter as tk
import tkinter.ttk as ttk


class ChildDialogInfo:
    """
    Open a child dialog of a tkinter application to inform the user.
    """

    def __init__(self, parent, title, msg):
        """
        Open a child dialog of a tkinter application to choose autoscan settings.

        Args:
            parent: the tkinter parent view to use for this window construction.
            title: title of the popup window
            msg: Message to show to the user
        """
        self.app = tk.Toplevel(parent)
        self.app.transient(parent)
        self.app.wait_visibility()
        self.app.grab_set()
        self.app.resizable(False, False)
        self.app.title(title)
        appFrame = ttk.Frame(self.app)
        self.rvalue = None
        self.parent = parent
        lbl = ttk.Label(appFrame, text=msg)
        lbl.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        appFrame.pack(fill=tk.BOTH)

    def show(self):
        """Start displaying this window."""
        self.app.update()

    def destroy(self):
        """
        Close the window.
        """
        # send the data to the parent
        self.app.destroy()
