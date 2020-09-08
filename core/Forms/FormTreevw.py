"""Widget "Table" using a ttk Treeview"""

import tkinter as tk
import tkinter.ttk as ttk
from core.Forms.Form import Form
import pyperclip


class FormTreevw(Form):
    """
    Form field representing a multi-lined input.
    """

    def __init__(self, name, headings, default_values=None, **kwargs):
        """
        Constructor for a form text

        Args:
            name: the treeview name (id).
            headings: table headers
            default_values: default values for the Table as a dict, default is None
            kwargs: same keyword args as you would give to ttk.Treeview
        """
        super().__init__(name)
        self.headings = headings
        self.default_values = default_values if default_values is not None else {}
        self.treevw = None
        self.kwargs = kwargs
        self.tvFrame = None
        self.scbVSel = None
        self.widgetMenuOpen = None
        self.contextualMenu = kwargs.get("contextualMenu", None)
        self.f = None

    def _initContextualMenu(self, parent):
        """Initialize the contextual menu for paperclip.
        Args:
            parent: the tkinter parent widget for the contextual menu
        """
        self.contextualMenu = tk.Menu(parent, tearoff=0, background='#A8CF4D',
                                      foreground='white', activebackground='#A8CF4D',
                                      activeforeground='white')
        parent.bind("<Button-3>", self.popup)
        self.contextualMenu.add_command(label="Copy", command=self.copy)
        self.contextualMenu.add_command(label="Close", command=self.close)

    def close(self):
        """Option of the contextual menu : Close the contextual menu by doing nothing
        """
        pass

    def copy(self, _event=None):
        """Option of the contextual menu : Copy entry text to clipboard
        """
        selected = self.treevw.selection()
        texts = []
        for item in selected:
            it = self.treevw.item(item)
            texts.append(it.get("text", "") + " " +
                         " ".join(it.get("values", [])))

        pyperclip.copy("\n".join(texts))

    def popup(self, event):
        """
        Fill the self.widgetMenuOpen and reraise the event in the editing window contextual menu

        Args:
            event: a ttk Treeview event autofilled.
            Contains information on what treeview node was clicked.
        """
        self.widgetMenuOpen = event.widget
        self.contextualMenu.post(event.x_root, event.y_root)
        self.contextualMenu.focus_set()
        self.contextualMenu.bind('<FocusOut>', self.popupFocusOut)

    def popupFocusOut(self, _event=None):
        """Callback for focus out event. Destroy contextual menu
        Args:
            _event: not used but mandatory
        """
        self.contextualMenu.unpost()

    def recurse_insert(self, values, parent='', columnsLen=None, odd=False):
        """Recursive insert of a value in a table:
        Args:
            values: values to insert in the treeview
                    * If it is a dict : Recurse
                    * If it is a list : Add key without value and list values as subchildren
                    * If it is a str : Insert into parent
            parent: the parent node treeview id to insert values into
            columnsLen: a table with the width of each column as list of 2 int
            odd: insert value as an odd value (the line will be tagged odd and change color). Default is False
        Returns:
            Final size of columns as list of two int
        """
        if columnsLen is None:
            columnsLen = [0, 0]
        sorted_keys = sorted(list(values.keys()))
        for sorted_key in sorted_keys:
            key = sorted_key
            value = values[key]
            root = parent
            if isinstance(value, str):
                self.treevw.insert(root, tk.END, None, text=key, values=[
                    str(value)], tags=("odd") if odd else ())
                odd = not odd
                columnsLen[0] = max(columnsLen[0], self.f.measure(key))
                columnsLen[1] = min(
                    1000, max(columnsLen[1], self.f.measure(str(value))))
            elif isinstance(value, list):
                root = self.treevw.insert(
                    root, tk.END, None, text=key, tags=("odd") if odd else ())
                odd = not odd
                columnsLen[0] = max(columnsLen[0], self.f.measure(key))
                child_odd = False
                for listValue in value:
                    self.treevw.insert(root, tk.END, None,
                                       text="", values=[str(listValue)], tags=("odd") if child_odd else ())
                    columnsLen[1] = min(1000, max(
                        columnsLen[1], self.f.measure(str(listValue))))
                    child_odd = not child_odd
            elif isinstance(value, dict):
                parent = self.treevw.insert(
                    root, tk.END, None, text=key, tags=("odd") if odd else ())
                odd = not odd
                columnsLen[0] = max(columnsLen[0], self.f.measure(key))
                columnsLen[1] = min(1000, max(
                    columnsLen[1], self.f.measure(str(value))))
                columnsLen = self.recurse_insert(
                    value, parent=root, columnsLen=columnsLen, odd=odd)
        return columnsLen

    def constructView(self, parent):
        """
        Create the text view inside the parent view given

        Args:
            parent: parent FormPanel.
        """
        if not isinstance(self.default_values, dict):
            self.default_values = {}
        self.tvFrame = ttk.Frame(
            parent.panel, width=self.getKw("width", 600))

        self.treevw = ttk.Treeview(
            self.tvFrame, height=min(self.getKw("height", len(
                self.default_values)+1), self.getKw("max_height", 10)))
        self.treevw.tag_configure("odd", background='light gray')
        self.scbVSel = ttk.Scrollbar(self.tvFrame,
                                     orient=tk.VERTICAL,
                                     command=self.treevw.yview)
        scbHSel = ttk.Scrollbar(
            self.tvFrame, orient=tk.HORIZONTAL, command=self.treevw.xview)
        self.treevw.configure(yscrollcommand=self.scbVSel.set)
        self.treevw.configure(xscrollcommand=scbHSel.set)

        self.treevw.grid(row=0, column=0, sticky=tk.NSEW)
        self.scbVSel.grid(row=0, column=1, sticky=tk.NS)
        scbHSel.grid(row=1, column=0, sticky=tk.EW)
        if len(self.headings) > 1:
            self.treevw['columns'] = self.headings[1:]
        root = tk.Label()
        self.f = tk.font.Font(root, "Sans", bold=True, size=10)
        columnsLen = self.recurse_insert(self.default_values)
        listOfLambdas = [self.column_clicked("#"+str(i), False) for i in range(len(self.headings))]
        for h_i, header in enumerate(self.headings):
            self.treevw.heading("#"+str(h_i), text=header, anchor="w", command=listOfLambdas[h_i])
            self.treevw.column("#"+str(h_i), anchor='w',
                               stretch=tk.YES, minwidth=columnsLen[h_i], width=columnsLen[h_i])
        binds = self.getKw("binds", {})
        for key, val in binds.items():
            self.treevw.bind(key, val)
        emptyRowFound = False
        children = self.treevw.get_children()
        for child in children:
            item = self.treevw.item(child)
            if item["text"] == "":
                emptyRowFound = True
                break
        if self.getKw("status", "none") != "readonly":
            if not emptyRowFound:
                tags = ("odd") if len(children) % 2 == 1 else ()
                self.treevw.insert('', tk.END, None, text="",
                                values=[""], tags=tags)
            self.treevw.bind("<Double-Button-1>", self.OnDoubleClick)
            self.treevw.bind("<Delete>", self.deleteItem)
            self.treevw.bind("<Control-c>", self.copy)
            self._initContextualMenu(self.treevw)
        if parent.gridLayout:
            self.tvFrame.grid(row=self.getKw("row", 0), column=self.getKw(
                "column", 0), sticky=self.getKw("sticky", tk.NSEW))

        else:
            self.tvFrame.pack(side=self.getKw("side", ""), padx=self.getKw(
                "padx", 10), pady=self.getKw("pady", 5), fill=self.getKw("fill", "none"), expand=self.getKw("expand", True))
        self.tvFrame.rowconfigure(0, weight=1)
        self.tvFrame.columnconfigure(0, weight=1)

    def column_clicked(self, col, reverse):
        """A lambda to call the statusbarController.statusbarClicked with the tag name clicked
        Args:
            name: the tag name clicked
        """
        return lambda : self.sort_column(self.treevw, col, reverse)

    def sort_column(self, tv, col, reverse):
        if col != "#0":
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
        else:
            l = [(k, k)for k in tv.get_children('')]
        l.sort(reverse=reverse)
        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)
            if index % 2 != 0:
                tv.item(k, tags=("odd"))
            else:
                tv.item(k, tags=())
           

        # reverse sort next time
        tv.heading(col, command=self.column_clicked(col, not reverse))

    def reset(self):
        """Reset the treeview values (delete all lines)"""
        for item in self.treevw.get_children():
            self.treevw.delete(item)

    def deleteItem(self, _event=None):
        """Callback for <Del> event
        Remove the selected item in the treeview
        Args:
            _event: not used but mandatory"""
        selected = self.treevw.selection()[0]
        item = self.treevw.item(selected)
        if item["text"].strip() != "":
            self.treevw.delete(selected)

    def OnDoubleClick(self, event):
        """Callback for double click event
        Edit value of double clicked item
        Args:
            event: automatically filled when event is triggered.
        """
        item = self.treevw.identify("item", event.x, event.y)
        column = self.treevw.identify_column(event.x)
        columnNb = int(column[1:])
        values = self.treevw.item(item)["values"]
        if columnNb == 0:
            oldVal = self.treevw.item(item)["text"]
        else:
            oldVal = values[columnNb-1]
        newVal = tk.simpledialog.askstring(
            "Modify infos", "New value for "+self.headings[columnNb].lower(), initialvalue=oldVal)
        if newVal is None:
            return
        if newVal.strip() == "" or newVal.strip() == oldVal.strip():
            return
        if columnNb == 0:
            self.treevw.item(item, text=newVal.strip())
        else:
            newVals = list(values)
            newVals[columnNb-1] = newVal.strip()
            self.treevw.item(item, values=newVals)
        emptyRowFound = False
        children = self.treevw.get_children()
        for child in children:
            item = self.treevw.item(child)
            if item["text"] == "":
                emptyRowFound = True
                break
        if not emptyRowFound:
            tags = ("odd") if len(children) % 2 == 1 else ()
            self.treevw.insert('', tk.END, None, text="",
                               values=[""], tags=tags)
            currentHeight = len(self.treevw.get_children())
            if currentHeight < self.getKw("max_height", 5):
                self.treevw.config(height=currentHeight)


    def getValue(self):
        """
        Return the form value. Required for a form.

        Returns:
            Return the entry value as string.
        """
        ret = {}
        children = self.treevw.get_children()
        for child in children:
            item = self.treevw.item(child)
            if not item["values"]:
                children_list = self.treevw.get_children(child)
                for child_list in children_list:
                    ret[item["text"]] = ret.get(item["text"], [])
                    item_child_list = self.treevw.item(child_list)
                    if item_child_list["values"]:
                        ret[item["text"]].append(item_child_list["values"][0])
            else:
                ret[item["text"]] = item["values"]
        return ret
