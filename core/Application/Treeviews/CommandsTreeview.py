"""Ttk treeview class with added functions.
"""
import tkinter as tk
from bson.objectid import ObjectId
from core.Models.Command import Command
from core.Models.CommandGroup import CommandGroup
from core.Views.CommandGroupView import CommandGroupView
from core.Views.CommandView import CommandView
from core.Controllers.CommandGroupController import CommandGroupController
from core.Controllers.CommandController import CommandController
from core.Application.Treeviews.PollenisatorTreeview import PollenisatorTreeview
from core.Components.mongo import MongoCalendar


class CommandsTreeview(PollenisatorTreeview):
    """CommandsTreeview class
    Inherit PollenisatorTreeview.
    Ttk treeview class with added functions to handle the command objects.
    """

    def __init__(self, appli, parentFrame):
        """
        Args:
            appli: a reference to the main Application object.
            parentFrame: the parent tkinter window object.
        """
        super().__init__(appli, parentFrame)
        self.commands_node = None  # parent of all commands nodes
        self.group_command_node = None  # parent of all group commands nodes
        self.openedViewFrameId = None  # if of the currently opened object in the view frame

    def initUI(self, _event=None):
        """Initialize the user interface widgets and binds them.
        Args:
            _event: not used but mandatory
        """
        if self.commands_node is not None:
            return
        self._initContextualsMenus()
        self.heading('#0', text='Commands', anchor=tk.W)
        self.column('#0', stretch=tk.YES, minwidth=300, width=300)
        self.bind("<Button-3>", self.doPopup)
        self.bind("<<TreeviewSelect>>", self.onTreeviewSelect)
        #self.bind("<Return>", self.onTreeviewSelect)
        #self.bind("<Button-1>", self.onTreeviewSelect)
        self.bind('<Delete>', self.deleteSelected)
        self.load()

    def onTreeviewSelect(self, event=None):
        """Called when a line is selected on the treeview
        Open the selected object view on the view frame.
        IF it's a parent commands or command_groups node, opens Insert
        ELSE open a modify window
        Args:
            event: filled with the callback, contains data about line clicked
        """
        item = super().onTreeviewSelect(event)
        if isinstance(item, str):
            if str(item) == "commands":
                objView = CommandView(
                    self, self.appli.commandsViewFrame, self.appli, CommandController(Command()))
                objView.openInsertWindow()
            elif str(item) == "command_groups":
                objView = CommandGroupView(
                    self, self.appli.commandsViewFrame, self.appli, CommandGroupController(CommandGroup()))
                objView.openInsertWindow()
        else:
            self.openModifyWindowOf(item)

    def doPopup(self, event):
        """Open the popup 
        Args:
            event: filled with the callback, contains data about line clicked
        """
        self.contextualMenu.selection = self.identify(
            "item", event.x, event.y)
        super().doPopup(event)

    def openModifyWindowOf(self, dbId):
        """
        Retrieve the View of the database id given and open the modifying form for its model and open it.

        Args:
            dbId: the database Mongo Id to modify.
        """
        objView = self.getViewFromId(str(dbId))
        if objView is not None:
            for widget in self.appli.commandsViewFrame.winfo_children():
                widget.destroy()
            objView.form.clear()
            self.openedViewFrameId = str(dbId)
            objView.openModifyWindow()

    def load(self, _searchModel=None):
        """
        Load the treeview with database information

        Args:
            _searchModel: (Deprecated) inherited not used. 
        """
        for widget in self.appli.commandsViewFrame.winfo_children():
            widget.destroy()
        self.delete(*self.get_children())

        self._load()

    def _load(self):
        """
        Load the treeview with database information
        """
        self.commands_node = self.insert(
            "", "end", "commands", text="Commands", image=CommandView.getClassIcon())
        commands = Command.fetchObjects({})
        for command in commands:
            command_vw = CommandView(
                self, self.appli.commandsViewFrame, self.appli, CommandController(command))
            command_vw.addInTreeview()
        self.group_command_node = self.insert("", "end", str(
            "command_groups"), text="Command Groups", image=CommandGroupView.getClassIcon())
        command_groups = CommandGroup.fetchObjects({})
        for command_group in command_groups:
            command_group_vw = CommandGroupView(
                self, self.appli.commandsViewFrame, self.appli, CommandGroupController(command_group))
            command_group_vw.addInTreeview()

    def refresh(self):
        """Alias to self.load method"""
        self.load()

    def notify(self, db, collection, iid, action, parent):
        """
        Callback for the observer pattern implemented in mongo.py.

        Args:
            collection: the collection that has been modified
            iid: the mongo ObjectId _id that was modified/inserted/deleted
            action: update/insert/delete. It was the action performed on the iid
            parent: the mongo ObjectId of the parent. Only if action in an insert.
        """
        if db != "pollenisator":
            return
        # Delete
        mongoInstance = MongoCalendar.getInstance()
        if action == "delete":
            try:
                self.delete(ObjectId(iid))
            except tk.TclError:
                pass  # item was not inserted in the treeview

        # Insert
        if action == "insert":
            res = mongoInstance.findInDb(
                db, collection, {"_id": ObjectId(iid)}, False)
            if collection == "commands":
                view = CommandView(self, self.appli.commandsViewFrame,
                                   self.appli, CommandController(Command(res)))
                parent = None
            elif collection == "group_commands":
                view = CommandGroupView(self, self.appli.commandsViewFrame,
                                        self.appli, CommandGroupController(CommandGroup(res)))
                parent = None
            try:
                view.addInTreeview(parent)
                if view is not None:
                    view.insertReceived()
            except tk.TclError:
                pass

        if action == "update":
            try:
                view = self.getViewFromId(str(iid))
                if view is not None:
                    self.item(str(iid), text=str(
                        view.controller.getModelRepr()), image=view.getIcon())
            except tk.TclError:
                if view is not None:
                    view.addInTreeview()
            if str(self.appli.openedViewFrameId) == str(iid):
                for widget in self.appli.viewframe.winfo_children():
                    widget.destroy()
                view.openModifyWindow()
            if view is not None:
                view.controller.actualize()
                view.updateReceived()
