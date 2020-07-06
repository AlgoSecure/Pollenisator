"""Defines a dialog window to display an error"""

import tkinter as tk
import tkinter.ttk as ttk
import webbrowser
from core.Forms.FormPanel import FormPanel


def postIssue(_err):
    """Open a tab in a browser to github issues page.
        Args:
            _err: Not used"""
    webbrowser.open_new_tab(
        "https://github.com/AlgoSecure/Pollenisator/issues")


class ChildDialogException:
    """
    Open a child dialog of a tkinter application to present the user to an unhandled exception.
    Can be used to report issue to github.
    """

    def __init__(self, parent, title, err):
        """
        Open a child dialog of a tkinter application to present the user to an unhandled exception.
        Can be used to report issue to github.
        Args:
            parent: the tkinter parent view to use for this window construction.
            title: A title for the new windows
            err: the error that occured causing this window to appear
        """
        self.rvalue = None
        self.parent = parent
        self.app = tk.Toplevel(parent)
        self.app.title(title)
        appFrame = ttk.Frame(self.app)
        self.form = FormPanel()
        self.err = err
        self.form.addFormLabel(
            "An error occured. Please make an issue with the below stack trace and when it occured.", side=tk.TOP)
        self.form.addFormText("Error", ".+", self.err,
                              None, side=tk.TOP)
        self.form.addFormButton("Report bug", self.onOk, side=tk.RIGHT)
        self.form.addFormButton("Close", self.onError, side=tk.RIGHT)
        self.rvalue = None
        self.form.constructView(appFrame)
        appFrame.pack(ipadx=10, ipady=10)
        self.app.transient(parent)
        try:
            self.app.wait_visibility()
            self.app.grab_set()
        except tk.TclError:
            pass

    def onOk(self, _event=None):
        """
        Called when the user clicked the validation button. Set the rvalue attributes to the value selected and close the window.
        
        Args:
            _event: not used but mandatory
        """
        # send the data to the parent
        postIssue(self.err)

    def onError(self, _event=None):
        """
        Close the dialog and set rvalue to None
        Args:
            _event: not used but mandatory
        """
        self.rvalue = False
        self.app.destroy()
