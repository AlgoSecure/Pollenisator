"""StatusBar class. Show tagged elements numbers to user.
"""
import tkinter as tk
import tkinter.ttk as ttk


class StatusBar(ttk.Frame):
    """StatusBar class. Show tagged numbers to user.
    Inherits ttk.Frame
    """

    def tagClicked(self, name):
        """A lambda to call the statusbarController.statusbarClicked with the tag name clicked
        Args:
            name: the tag name clicked
        """
        return lambda _event: self.statusbarController.statusbarClicked(name)

    def __init__(self, master, registeredTags, statusbarController):
        """
        Constructor of the status bar
        Args:
            master: parent tkinter window
            registeredTags: a list of tag names registred in settings
            statusbarController: a controller to handle clicks on status bar.
                                It has to delcare a statusbarClicked function taking 1 arg : a tag name
        """
        # Cannot be imported at module level as tkinter will not have loaded.
        import tkinter.font
        super().__init__(master)
        label = ttk.Label(self, text="Tagged:", relief=None,
                                style="Important.TLabel")
        label.grid(column=0, row=0)
        self.registeredTags = registeredTags
        self.statusbarController = statusbarController
        self.tagsCount = {}
        self.labelsTags = {}
        column = 1
        keys = list(self.registeredTags.keys())
        listOfLambdas = [self.tagClicked(keys[i]) for i in range(len(keys))]
        for registeredTag, color in registeredTags.items():
            self.tagsCount[registeredTag] = 0
            self.labelsTags[registeredTag] = ttk.Label(self, text=registeredTag+" : "+str(self.tagsCount[registeredTag]), relief=tk.SUNKEN, anchor=tk.W, background=color, foreground="black")
            self.labelsTags[registeredTag].grid(column=column, row=0, padx=1)
            self.labelsTags[registeredTag].bind('<Button-1>', listOfLambdas[column-1])
            column += 1

    def notify(self, addedTags, removedTags=[]):
        """
        Notify is called when tags are added or removed
        Args:
            addedTags: a list of tag names added
            removedTags: a list of tag names removed, default to []
        """
        if not "hidden" in addedTags:
            for tag in addedTags:
                if tag in self.tagsCount:
                    self.tagsCount[tag] += 1
        for tag in removedTags:
            if tag in self.tagsCount:
                self.tagsCount[tag] -= 1

    def reset(self):
        """
        Rest all displayed tags count to 0
        """
        for registeredTag in self.registeredTags:
            self.tagsCount[registeredTag] = 0
        self.update()

    def update(self):
        """
        Update all tags label to tags count
        """
        for tag, label in self.labelsTags.items():
            label.config(text=tag+" : "+str(self.tagsCount[tag]))
            label.update_idletasks()

