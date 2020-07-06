import os
from shutil import which
import tkinter.messagebox

import core.Components.Utils as Utils
from core.Components.mongo import MongoCalendar

class Terminal:
    iconName = "tab_terminal.png"
    tabName = "  Terminal  "

    def __init__(self, parent, settings):
        self.settings = settings

    def initUI(self, parent, nbk, treevw):
        return

    def open(self):
        mainDir = os.path.normpath(Utils.getMainDir())
        mongoInstance = MongoCalendar.getInstance()
        with open(os.path.join(mainDir, "setupTerminalForPentest.sh"), "r") as f:
            data = f.read()
            lines = data.split("\n")
            lines[0] = "POLLENISATOR_CURRENT_DB="+str(mongoInstance.calendarName)
            data = "\n".join(lines)
            with open(os.path.join(mainDir, "setupTerminalForPentest.sh"), "w") as f:
                f.write(data)
        favorite = self.settings.getFavoriteTerm()
        if favorite is None:
            tkinter.messagebox.showerror("Terminal settings invalid", "None of the terminals given in the settings are installed on this computer.")
            return False

        if which(favorite) is not None:
            terms = self.settings.getTerms()
            terms_dict = {}
            for term in terms:
                terms_dict[term.split(" ")[0]] = term
            command_term = terms_dict.get(favorite, None)
            if command_term is not None:
                Utils.execute(terms_dict[favorite])
                return True
            else:
                tkinter.messagebox.showerror("Terminal settings invalid", "Check your terminal settings")
        else:
            tkinter.messagebox.showerror("Terminal settings invalid", "The selected favorite terminal is not available on this computer.")
        return False
