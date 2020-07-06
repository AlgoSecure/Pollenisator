"""Widget with an entry to type a file path and a '...' button to pick from file explorer."""

import tkinter as tk
import tkinter.ttk as ttk
from core.Forms.Form import Form
import tkinter.filedialog


class FormFile(Form):
    """
    Form field representing a path input.
    Default setted values: 
        state="readonly"
        if pack : padx = pady = 5, side = "right"
        if grid: row = column = 0 sticky = "west"
        entry "width"=  20
    Additional values to kwargs:
        modes: either "file" or "directory" to choose which type of path picker to open
    """

    def __init__(self, name, regexValidation="", default="", **kwargs):
        """
        Constructor for a form file

        Args:
            name: the entry name (id).
            regexValidation: a regex used to check the input in the checkForm function., default is ""
            default: a default value for the Entry, default is ""
            kwargs: same keyword args as you would give to ttk.Frame + "modes" which is either "file" or "directory" 
                    to choose which type of path picker to open
        """
        super().__init__(name)
        self.regexValidation = regexValidation
        self.default = default
        self.kwargs = kwargs
        self.entry = None

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
        self.entry = tk.Entry(frame, textvariable=self.val,
                              width=self.getKw("width", 20))
        self.entry.bind("<Control-a>", self.selectAll)
        self.entry.grid(column=1, row=0)
        self.val.set(self.default)
        modes = self.getKw("mode", "file").split("|")
        column = 2
        if "file" in modes:
            text = "..." if len(modes) == 1 else "file"
            search_btn = ttk.Button(
                frame, text=text, command=self.on_click, width=4)
            search_btn.grid(column=column, row=0)
            column += 1
        if "directory" in modes:
            text = "..." if len(modes) == 1 else "directory"
            search_btn = ttk.Button(
                frame, text=text, command=self.on_click_dir)
            search_btn.grid(column=column, row=0)
            column += 1
        if parent.gridLayout:
            frame.grid(row=self.getKw("row", 0),
                       column=self.getKw("column", 0), **self.kwargs)
        else:
            frame.pack(fill=self.getKw("fill", "x"), side=self.getKw(
                "side", "top"), pady=self.getKw("pady", 5), padx=self.getKw("padx", 10), **self.kwargs)

    def on_click(self, _event=None):
        """Callback when '...' is clicked and modes Open a file selector (tkinter.filedialog.askopenfilename)
        Args:
            _event: not used but mandatory
        Returns:
            None if no file name is picked,
            the selected file full path otherwise.
        """
        f = tkinter.filedialog.askopenfilename(title="Select a file")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        if f != "":
            filename = str(f)
            self.val.set(filename)

    def on_click_dir(self, _event=None):
        """Callback when '...' is clicked and modes="directory" was set.
        Open a directory selector (tkinter.filedialog.askdirectory)
        Args:
            _event: not used but mandatory
        Returns:
            None if no directory is picked,
            the selected directory full path otherwise.
        """
        f = tkinter.filedialog.askdirectory(title="Select a directory")
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        if f != "":
            filename = str(f)
            self.val.set(filename)

    def selectAll(self, _event):
        """Callback to select all the text in the date Entry.
        Args:
            _event: mandatory but not used
        Returns:
            Returns the string "break" to prevent the event to be treated by the Entry, thus inserting unwanted value.
        """
        # select text
        self.entry.select_range(0, 'end')
        # move cursor to the end
        self.entry.icursor('end')
        return "break"

    def getValue(self):
        """
        Return the form value. Required for a form.

        Returns:
            Return the entry value as string.
        """
        return self.val.get()

    def checkForm(self):
        """
        Check if this form is correctly filled. Check with the regex validation given in constructor.

        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }
        """
        import re
        if re.match(self.regexValidation, self.getValue()) is not None:
            return True, ""
        return False, self.name+" value is incorrect."

    def setFocus(self):
        """Set the focus to the ttk entry part of the widget.
        """
        self.entry.focus_set()
