import tkinter as tk
from core.Forms.Form import Form

import tkinter.ttk as ttk
import tkinter.messagebox


class FormSearchBar(Form):
    """
    Form field representing a string input.
    """

    def __init__(self, name, searchCallback, panel_to_fill, list_of_forms_to_fill, default="", **kwargs):
        """
        Constructor for a form entry

        Args:
            name: the entry name (id).
            regexValidation: a regex used to check the input in the checkForm function., default is ""
            default: a default value for the Entry, defauult is ""
        """
        super().__init__(name)
        self.searchCallback = searchCallback
        self.panel_to_fill = panel_to_fill
        self.list_of_forms_to_fill = list_of_forms_to_fill
        self.default = default
        self._results = None
        self.kwargs = kwargs
        self.entry = None
        self.combo_search = None

    def constructView(self, parent):
        """
        Create the string view inside the parent view given

        Args:
            parent: parent FormPanel.
        """
        self.val = tk.StringVar()
        frame = ttk.Frame(parent.panel)
        lbl = ttk.Label(frame, text=self.name+" : ", background="white")
        lbl.grid(column=0, row=0)
        self.entry = tk.Entry(frame, textvariable=self.val, width=50)
        self.entry.grid(column=1, row=0)
        self.entry.bind("<Control-a>", self.selectAll)
        self.val.set(self.default)
        lbl = ttk.Label(frame, text="Search results : ", background="white")
        lbl.grid(column=0, row=1)
        values = []
        if self.default != "":
            values.append(self.default)
        self.combo_search = ttk.Combobox(frame, values=values, width=50, state="readonly")
        self.combo_search.bind('<<ComboboxSelected>>', self.postSelect)
        if self.default != "":
            self.combo_search.set(self.default)
        self.combo_search.grid(column=1, row=1)
        self.entry.bind('<Key-Return>', self.updateValues)
        if self.getKw("autofocus", True):
            self.entry.focus_set()
        if parent.gridLayout:
            frame.grid(row=self.getKw("row", 0), column=self.getKw("column", 0), **self.kwargs)
        else:
            frame.pack(side=self.getKw("side", "top"), padx=self.getKw("padx", 10), pady=self.getKw("pady", 5), **self.kwargs)
        

    def selectAll(self, _event):
        # select text
        self.entry.select_range(0, 'end')
        # move cursor to the end
        self.entry.icursor('end')
        return "break"
    
    def updateValues(self, _event=None):
        self._results = self.searchCallback(self.val.get())
        if self._results is None:
            tkinter.messagebox.showinfo("SearchBar is not responding", "Error while searching. Check internet connection or request.")
            self.combo_search['values'] = [self.val.get()]
            self.combo_search.set(self.val.get())
            return
        list_choice = []
        for result in self._results:
            list_choice.append(result["title"])
        self.combo_search['values'] = list_choice
        if len(list_choice) > 0:
            self.combo_search.set(list_choice[0])
            self.postSelect()

    def postSelect(self, _event=None):
        selected = self.getValue()
        if selected != None:
            for subform in self.panel_to_fill.subforms:
                if getattr(subform, "subforms", None) is not None: # 1 depth max
                    for subform_depth in subform.subforms:
                        if getattr(subform_depth, "subforms", None) is None:
                            if subform_depth.name.lower() in selected.keys():
                                subform_depth.setValue(selected[subform_depth.name.lower()])
                else:
                    if subform.name.lower() in selected.keys():
                        subform.setValue(selected[subform.name.lower()])


    def getValue(self):
        """
        Return the form value. Required for a form.

        Returns:
            Return the entry value as string.
        """
        title = self.combo_search.get()
        if self._results is not None:
            for elem in self._results:
                if elem["title"] == title:
                    return elem
        return None

    def setFocus(self):
        self.entry.focus_set()

