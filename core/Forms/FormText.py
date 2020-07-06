"""Describe tkinter Text with default common args and an attached scrollbar"""

import tkinter as tk
import tkinter.scrolledtext
import pyperclip
from core.Forms.Form import Form

class FormText(Form):
    """
    Form field representing a multi-lined input.
    Default setted values:
        width=20, height=20
        if pack : padx = pady = 5, side = left
        if grid: row = column = 0 sticky = "East"
    """

    def __init__(self, name, regexValidation="", default="", contextualMenu=None, **kwargs):
        """
        Constructor for a form text

        Args:
            name: the entry name (id).
            regexValidation: a regex used to check the input
                             in the checkForm function. default is ""
            default: a default value for the Entry, default is ""
            contextualMenu: (Opt.) a contextualMenu to open when right clicked. default is None
            kwargs: same keyword args as you would give to ttk.Text
        """
        super().__init__(name)
        self.regexValidation = regexValidation
        self.default = default
        self.contextualMenu = contextualMenu
        self.kwargs = kwargs
        self.text = None
        self.widgetMenuOpen = None

    def _initContextualMenu(self, parent):
        """Initialize the contextual menu for paperclip.
        Args:
            parent: the tkinter parent widget for the contextual menu
        """
        # FIXME Add to given menu instead of Overriding given contextual menu
        self.contextualMenu = tk.Menu(parent, tearoff=0, background='#A8CF4D',
                                      foreground='white', activebackground='#A8CF4D',
                                      activeforeground='white')
        parent.bind("<Button-3>", self.popup)
        self.contextualMenu.add_command(label="Copy", command=self.copy)
        self.contextualMenu.add_command(label="Cut", command=self.cut)
        self.contextualMenu.add_command(label="Paste", command=self.paste)
        self.contextualMenu.add_command(label="Close", command=self.close)

    def close(self):
        """Option of the contextual menu : Close the contextual menu by doing nothing
        """
        pass

    def copy(self):
        """Option of the contextual menu : Copy entry text to clipboard
        """
        ranges = self.text.tag_ranges(tk.SEL)
        if ranges:
            pyperclip.copy(self.text.get(*ranges))

    def cut(self):
        """Option of the contextual menu : Cut entry text to clipboard
        """
        ranges = self.text.tag_ranges(tk.SEL)
        if ranges:
            pyperclip.copy(self.text.get(*ranges))
            self.text.delete(*ranges)

    def paste(self):
        """Option of the contextual menu : Paste clipboard content to entry
        """
        buff = pyperclip.paste()
        if buff:
            insertIndex = self.text.index(tk.INSERT)
            self.text.insert(insertIndex, buff)

    def constructView(self, parent):
        """
        Create the text view inside the parent view given

        Args:
            parent: parent FormPanel.
        """

        self.text = tkinter.scrolledtext.ScrolledText(
            parent.panel, relief=tk.SUNKEN, height=self.getKw("height", 20))
        self._initContextualMenu(self.text)
        self.text.bind('<Control-a>', self.selectAll)
        try:
            self.text.insert(tk.INSERT, self.default)
        except tk.TclError as e:
            self.text.insert(tk.INSERT, "Error :\n"+str(e))
        if parent.gridLayout:
            self.text.grid(row=self.getKw("row", 0), column=self.getKw(
                "column", 0), sticky=self.getKw("sticky", tk.EW), **self.kwargs)
        else:
            self.text.pack(side=self.getKw("side", "left"), padx=self.getKw(
                "padx", 10), pady=self.getKw("pady", 5), expand=self.getKw("expand", True), fill=self.getKw("fill", "both"), **self.kwargs)

    def selectAll(self, _event):
        """Callback to select all the text in the date Entry.
        Args:
            _event: mandatory but not used
        Returns:
            Returns the string "break" to prevent the event to be treated by the Entry, thus inserting unwanted value.
        """
        self.text.tag_add('sel', '1.0', 'end')
        return "break"

    def getValue(self):
        """
        Return the form value. Required for a form.

        Returns:
            Return the entry value as string.
        """
        return self.text.get('1.0', 'end-1c')

    def checkForm(self):
        """
        Check if this form is correctly filled.
        Check with the regex validation given in constructor.

        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }
        """
        import re
        if re.match(self.regexValidation, self.getValue(), re.MULTILINE) is None:
            return False, self.name+" value is incorrect."
        return True, ""

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

    def setFocus(self):
        """Set the focus to the ttk entry widget.
        """
        self.text.focus_set()
