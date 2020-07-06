"""Widget with a list of checkbox packed and wrapping. A checkbox to check or uncheck all is at the top
#TODO improve looking and constructing"""

import tkinter as tk
import tkinter.ttk as ttk
from core.Forms.Form import Form


class FormChecklist(Form):
    """
    Form field representing a checklist.
    Default setted values: 
        if pack : padx = 10, pady = 5, side = top, fill = "x"
        if grid: row = column = 0
    """
    def __init__(self, name, choicesList, default, **kwargs):
        """
        Constructor for a form checklist
        Args:
            name: the checklist name (id).
            choicesList: a list of string forming all the possible choices.
            default: a list of string that should be prechecked if in the choice list.
            kwargs: same keyword args as you would give to ttk.Frame
        """
        super().__init__(name)
        self.choicesList = choicesList
        self.default = default
        self.kwargs = kwargs
        self.checkallval = None
        self.checks = []

    def checkall(self):
        """
        Will check all the checkbox or uncheck same depending on the checkbox state.
        """
        for cb in self.val:
            if self.checkallval.get() == 1:
                cb.set(1)
            else:
                cb.set(0)
    def constructView(self, parent):
        """
        Create the checlist view inside the parent view given

        Args:
            FormPanel: parent form panel.
        """
        ################################ THIS is difficult to achieve as the forms positions and width are complicated to get.
        ################################ Temporary fix : hard coded max width.
        frame = ttk.Frame(parent.panel)
        self.val = []
        lbl = ttk.Label(frame, text=self.name+" : ", background="white")
        lbl.pack(side="top", pady=5, padx=10)
        self.checkallval = tk.IntVar()
        chk = ttk.Checkbutton(
            frame, text="All", variable=self.checkallval, command=self.checkall)
        chk.pack(side="top", pady=5, padx=10)
        if parent.gridLayout:
            frame.grid(row=self.getKw("row", 0), column=self.getKw("column", 0), **self.kwargs)
        else:
            frame.pack(fill=self.getKw("fill", "x"), side=self.getKw("side", "top"), pady=self.getKw("pady", 5), padx=self.getKw("padx", 10), **self.kwargs)
        #frame = ttk.Frame(parent.panel)
        accx = 0
        for choice in self.choicesList:
            v1 = tk.IntVar()
            if choice in self.default:
                v1.set(1)
            self.val.append(v1)
            chk = ttk.Checkbutton(frame, text=choice,
                                 variable=self.val[-1])
            if chk.winfo_reqwidth() + accx >= 400:
                frame = ttk.Frame(parent.panel)
                accx = 0
            else:
                accx += chk.winfo_reqwidth()
            self.checks.append(chk)
            chk.pack(side="left", anchor="w", padx=3)
            if parent.gridLayout:
                frame.grid(row=self.getKw("row", 0), column=self.getKw("column", 0))
            else:
                frame.pack(fill=self.getKw("fill", "x"), side=self.getKw("side", "top"), pady=self.getKw("pady", 5), padx=self.getKw("padx", 10), **self.kwargs)


        if parent.gridLayout:
            frame.grid(row=self.getKw("row", 0), column=self.getKw("column", 0))
        else:
            frame.pack(fill=self.getKw("fill", "x"), side=self.getKw("side", "top"), pady=self.getKw("pady", 5), padx=self.getKw("padx", 10), **self.kwargs)

    def getValue(self):
        """
        Return the form value. Required for a form.

        Returns:
            Return a dictionnary of all checkboxs with texts as keys and 0 or 1 as value. 1 is if the checkbox was ticked.
        """
        ret = {}
        for i, v in enumerate(self.val):
            ret[self.checks[i].cget("text")] = int(v.get())
        return ret

    def setValue(self, newval):
        """Set value of checkboxes defined in given list.
        Args:
            newval: A list with checkbox texts. If a checkbox text matches one in the list, it will checked.
        """
        for i, v in enumerate(self.val):
            if self.checks[i].cget("text").lower() in newval.lower():
                v.set(1)

    def checkForm(self):
        """
        Check if this form is correctly filled. A checklist cannot be malformed.

        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }
        """
        return True, ""

    def setFocus(self):
        """Set the focus to the first ttk checkbox of the list."""
        if len(self.checks) > 0:
            self.checks[0].focus_set()