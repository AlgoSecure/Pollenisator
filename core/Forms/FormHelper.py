"""Widget with a button that display an helping message when hovered"""

import tkinter as tk
import tkinter.ttk as ttk
from core.Forms.Form import Form
from PIL import ImageTk, Image
from core.Components.Utils import getIconDir


class FormHelper(Form):
    """
    Form field representing a helper button.
    Default setted values: 
        state="readonly"
        if pack : padx = pady = 5, side = "right"
        if grid: row = column = 0 sticky = "west"
        entry "width"=  20
    """
    img_class = None

    def __init__(self, name, text, **kwargs):
        """
        Constructor for a form button

        Args:
            name: the helper name. Should not matter as it does not return data
            text: the helping message to be displayed
            kwargs: same keyword args as you would give to ttk.Label
        """
        super().__init__(name)
        FormHelper.img_class = ImageTk.PhotoImage(
            Image.open(getIconDir()+"help.png"))
        self.text = text
        self.kwargs = kwargs
        self.lbl = None
        self.tw = None

    def constructView(self, parent):
        """
        Create the button view inside the parent view given

        Args:
            parent: parent form panel.
        """
        self.lbl = ttk.Label(
            parent.panel, image=FormHelper.img_class)
        self.lbl.bind("<Enter>", self.enter)
        self.lbl.bind("<Leave>", self.close)
        if parent.gridLayout:
            self.lbl.grid(row=self.getKw("row", 0), column=self.getKw(
                "column", 0), sticky=self.getKw("sticky", tk.W))
        else:
            self.lbl.pack(side=self.getKw("side", "right"), padx=self.getKw(
                "padx", 5), pady=self.getKw("pady", 5))

    def enter(self, _event=None):
        """Callback for the <Enter> event
        Starts displaying the help message
        Args:
            _event: not used but mandatory
        """
        x = y = 0
        x, y, _, _ = self.lbl.bbox("insert")
        x += self.lbl.winfo_rootx() + 25
        y += self.lbl.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.lbl)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                         background='light yellow', relief='solid', borderwidth=1,
                         font=("times", "12", "normal"))
        label.pack(ipadx=1)

    def close(self, _event=None):
        """Callback for the <Leave> event
        Stops displaying the help message
        Args:
            _event: not used but mandatory
        """
        if self.tw:
            self.tw.destroy()
