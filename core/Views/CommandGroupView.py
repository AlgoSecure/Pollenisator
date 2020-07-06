"""View for command group object. Handle node in treeview and present forms to user when interacted with."""

from core.Views.ViewElement import ViewElement
import core.Models.Command as Command
import tkinter as tk

class CommandGroupView(ViewElement):
    """
    View for command group object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory.
    """
    icon = 'group_command.png'

    def openModifyWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to update or delete an existing CommandGroup
        """
        modelData = self.controller.getData()
        panel = self.form.addFormPanel(grid=True)
        panel.addFormLabel("Name")
        panel.addFormStr("Name", r".*\S.*", modelData["name"], column=1)
        panel = self.form.addFormPanel()
        panel.addFormChecklist(
            "Commands", Command.Command.getList(), modelData["commands"], side=tk.LEFT)
        panel = self.form.addFormPanel(grid=True)
        panel.addFormLabel("Delay")
        panel.addFormStr(
            "Delay", r"\d+", modelData["sleep_between"], width=5, column=1)
        panel.addFormHelper(
            "Delay in-between two launch of each command of ths group (in seconds).\nIf a command is in two groups, the highest delay will be used", column=2)
        panel.addFormLabel("Shared threads", row=1)
        panel.addFormStr("Shared threads", r"\d+",
                         modelData["max_thread"], width=2, row=1, column=1)
        panel.addFormHelper(
            "Number of parallel execution allowed for every command in this group at any given moment.", row=1, column=2)
        self.completeModifyWindow()

    def openInsertWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to insert a new CommandGroup
        """
        panel = self.form.addFormPanel(grid=True)
        panel.addFormLabel("Name")
        panel.addFormStr("Name", r".*\S.*", "", column=1)
        panel = self.form.addFormPanel()
        panel.addFormChecklist("Commands", Command.Command.getList(), [] ,side=tk.LEFT)
        panel = self.form.addFormPanel(grid=True)
        panel.addFormLabel("Delay")
        panel.addFormStr("Delay", r"\d+", "0", width=5, column=1)
        panel.addFormHelper(
            "Delay in-between two launch of each command of ths group (in seconds).\nIf a command is in two groups, the highest delay will be used", column=2)
        panel.addFormLabel("Shared threads", row=1)
        panel.addFormStr("Shared threads", r"\d+",
                         "1", width=2, row=1, column=1)
        panel.addFormHelper(
            "Number of parallel execution allowed for every command in this group at any given moment.", row=1, column=2)
        self.completeInsertWindow()

    def addInTreeview(self, parentNode=None):
        """Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: not used
        """
        parentNode = self.getParent()
        self.appliTw.views[str(self.controller.getDbId())] = {"view": self}
        self.appliTw.insert(parentNode, "end", str(self.controller.getDbId()), text=str(
            self.controller.getModelRepr()), tags=self.controller.getTags(), image=self.getClassIcon())
        if "hidden" in self.controller.getTags():
            self.hide()

    def getParent(self):
        """
        Return the id of the parent node in treeview.

        Returns:
            return the saved group_command_node node inside the Appli class.
        """
        return self.appliTw.group_command_node
