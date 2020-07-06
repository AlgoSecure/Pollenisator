"""Ask a question to the user.
"""
import tkinter as tk
import tkinter.ttk as ttk


class ChildDialogQuestion:
    """
    Open a child dialog of a tkinter application to ask a question.
    """

    def __init__(self, parent, title, question, answers=("Yes", "No")):
        """
        Open a child dialog of a tkinter application to ask a question.

        Args:
            parent: the tkinter parent view to use for this window construction.
            title: title of the new window
            question: question to answer
            answers: a tuple with possible answers. Default to ("Yes" ,"No")
        """
        self.app = tk.Toplevel(parent)
        self.app.title(title)
        self.app.resizable(False, False)
        appFrame = ttk.Frame(self.app)
        self.rvalue = None
        self.parent = parent
        lbl = ttk.Label(appFrame, text=question)
        lbl.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        buttonsFrame = ttk.Frame(appFrame)
        for i, answer in enumerate(answers):
            _button = ttk.Button(buttonsFrame, text=answer)
            _button.bind("<Button-1>", self.onOk)
            _button.grid(row=0, column=i, padx=15)
        buttonsFrame.pack(side=tk.TOP, ipadx=5, pady=5)
        appFrame.pack(fill=tk.BOTH)
        self.app.transient(parent)
        try:
            self.app.wait_visibility()
            self.app.grab_set()
        except tk.TclError:
            pass

    def onOk(self, event):
        """
        Called when the user clicked the validation button.
        Set the rvalue attributes to the answer string choosen.
        """
        # send the data to the parent
        self.rvalue = event.widget["text"]
        self.app.destroy()
