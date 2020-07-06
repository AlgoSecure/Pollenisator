"""Show a progess bar for the user.
"""
import tkinter as tk
import tkinter.ttk as ttk


class ChildDialogProgress:
    """
    Open a child dialog of a tkinter application to inform the user about a ongoing process.
    """

    def __init__(self, parent, title, msg, length=200, progress_mode="indeterminate"):
        """
        Open a child dialog of a tkinter application to display a progress bar.

        Args:
            parent: the tkinter parent view to use for this window construction.
            title: Title for the new window
            msg: Message to display on the window to inform about a progession.
            length: Length of the progress bar, default to 200
            progress_mode: mode of progression. Either "determinate" or "inderterminate". Default to the second.
                           indeterminate: bouncing progress bar.
                           determinate: Show progression of a value against a max value.
        """
        self.app = tk.Toplevel(parent)
        self.app.transient(parent)
        self.app.resizable(False, False)
        self.app.title(title)
        appFrame = ttk.Frame(self.app)
        self.rvalue = None
        self.parent = parent
        lbl = ttk.Label(appFrame, text=msg)
        lbl.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        self.mode = progress_mode
        self.progressbar = ttk.Progressbar(appFrame, orient="horizontal",
                                           length=length, mode=progress_mode)
        self.progressbar.pack(side=tk.BOTTOM, padx=10, pady=10, fill=tk.X)
        appFrame.pack(fill=tk.BOTH)
        try:
            self.app.wait_visibility()
            self.app.grab_set()
        except tk.TclError:
            pass

    def show(self, maximum=None, startValue=0):
        """Start displaying the progressbar.
        Args:
            - maximum: only for determinate mode. Set the goal value. Default to None.
            - startValue: only for determinate mode. Set the starting value. Default to None.
        """
        if self.mode == "indeterminate":
            self.progressbar.start()
        elif self.mode == "determinate" and maximum is not None:
            self.progressbar["value"] = startValue
            self.progressbar["maximum"] = maximum
        self.app.update()

    def update(self, value=None):
        """Update the progressbar and show progression value.
        Call this regularly if on inderminate mode.
        Args:
            - value: The new value for the progressbar. Default to None.
        """
        if self.mode == "indeterminate":
            try:
                self.progressbar.step()
            except tk.TclError:
                print("Shutdown while loading...")
                return
        elif self.mode == "determinate":
            if value is None:
                self.progressbar["value"] += 1
            else:
                self.progressbar["value"] = value
        self.app.update()

    def destroy(self):
        """
        Close the window and stop the progressbar.
        """
        # send the data to the parent
        self.progressbar.stop()
        self.app.destroy()
