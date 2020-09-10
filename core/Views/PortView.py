"""View for port object. Handle node in treeview and present forms to user when interacted with."""

import webbrowser
from core.Models.Tool import Tool
from core.Models.Defect import Defect
from core.Models.Command import Command
from core.Views.ToolView import ToolView
from core.Views.ViewElement import ViewElement
from core.Views.DefectView import DefectView
from core.Controllers.DefectController import DefectController
from core.Controllers.ToolController import ToolController
from core.Components.mongo import MongoCalendar
from tkinter import TclError


class PortView(ViewElement):
    """View for port object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory"""

    icon = 'port.png'

    def __init__(self, appTw, appViewFrame, mainApp, controller):
        """Constructor
        Args:
            appTw: a PollenisatorTreeview instance to put this view in
            appViewFrame: an view frame to build the forms in.
            mainApp: the Application instance
            controller: a CommandController for this view.
        """
        super().__init__(appTw, appViewFrame, mainApp, controller)
        self.tool_panel = None

    def openInsertWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to insert a new Port
        """
        modelData = self.controller.getData()
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("Number")
        top_panel.addFormStr("Number", r"\d+", "", column=1)
        top_panel.addFormLabel("Proto", row=1)
        top_panel.addFormCombo("Proto", ["tcp", "udp"], "tcp", row=1, column=1)
        top_panel.addFormLabel("Service", row=2)
        top_panel.addFormStr("Service", r"", "", row=2, column=1)
        top_panel.addFormLabel("Product", row=3)
        top_panel.addFormStr("Product", r"", "", row=3, column=1)
        self.form.addFormHidden("ip", modelData["ip"])
        self.completeInsertWindow()

    def openModifyWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to update or delete an existing Port
        """
        modelData = self.controller.getData()
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("IP", row=0, column=0)
        top_panel.addFormStr(
            "IP", '', modelData["ip"], None, column=1, row=0, state="readonly")
        top_panel.addFormLabel("Number", column=0, row=1)
        top_panel.addFormStr(
            "Number", '', modelData["port"], None, column=1, row=1, state="readonly")
        top_panel.addFormLabel("Proto", row=2, column=0)
        top_panel.addFormStr(
            "Proto", '', modelData["proto"], None, column=1, row=2, state="readonly")
        top_panel.addFormLabel("Service", row=3)
        top_panel.addFormStr(
            "Service", r"", modelData["service"], column=1, row=3)
        if "http" in modelData["service"]:
            top_panel.addFormButton(
                "Open in browser", self.openInBrowser, column=2, row=3)
        top_panel.addFormLabel("Product", row=4)
        top_panel.addFormStr("Product", r"", modelData["product"], width=40, row=4, column=1)
        top_panel = self.form.addFormPanel()
        top_panel.addFormLabel("Notes", side="top")
        top_panel.addFormText(
            "Notes", r"", modelData["notes"], None, side="top", height=10)
        top_panel.addFormLabel("Infos", side="left")
        top_panel.addFormTreevw("Infos", ("Infos", "Values"),
                                modelData["infos"], side="left", width=300, fill="both", height=8, binds={"<Enter>": self.mainApp.unboundToMousewheelMain, "<Leave>": self.mainApp.boundToMousewheelMain})
        command_list = Command.fetchObjects({"lvl": "port"}, MongoCalendar.getInstance().calendarName)
        command_names = ["None"]
        for command_doc in command_list:
            command_names.append(command_doc.name)
        self.tool_panel = self.form.addFormPanel(grid=True)
        self.tool_panel.addFormLabel("Tool to add")
        self.tool_panel.addFormCombo(
            "Tool to add", command_names, "None", column=1)
        self.tool_panel.addFormButton("Add tool", self._addTool, column=2)
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormButton("Add a security defect",
                                self.addDefectCallback)
        self.form.addFormHidden("ip", modelData["ip"])
        self.completeModifyWindow()

    def openInBrowser(self, _event):
        """Callback for action open in browser
        Args:
            _event: nut used but mandatory
        """
        modelData = self.controller.getData()
        if modelData["service"] == "http":
            webbrowser.open_new_tab(
                "http://"+modelData["ip"]+":"+modelData["port"])
        else:
            webbrowser.open_new_tab(
                "https://"+modelData["ip"]+":"+modelData["port"])

    def addDefectCallback(self, _event):
        """
        Create an empty defect model and its attached view. Open this view insert window.

        Args:
            event: Automatically generated with a button Callback, not used but mandatory.
        """
        for widget in self.appliViewFrame.winfo_children():
            widget.destroy()
        modelData = self.controller.getData()
        dv = DefectView(self.appliTw, self.appliViewFrame,
                        self.mainApp, DefectController(Defect(modelData)))
        dv.openInsertWindow()

    def _addTool(self, _event=None):
        """Callback for add tool action
        Add a tool without any check to port.
        Args:
            _event: not used but mandatory
        """
        toolname_values = self.tool_panel.getValue()
        toolname = ViewElement.list_tuple_to_dict(toolname_values)[
            "Tool to add"]
        self.controller.addAllTool(toolname, 'Custom tools', '', False)

    def addInTreeview(self, parentNode=None, addChildren=True):
        """Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            addChildren: If False, skip the tool and defects insert. Useful when displaying search results
        """
        if parentNode is None:
            parentNode = self.getParent()
            nodeText = str(self.controller.getModelRepr())
        elif parentNode == '':
            nodeText = self.controller.getDetailedString()
        else:
            nodeText = str(self.controller.getModelRepr())
        self.appliTw.views[str(self.controller.getDbId())] = {"view": self}
        try:
            self.appliTw.insert(parentNode, "end", str(
                self.controller.getDbId()), text=nodeText, tags=self.controller.getTags(), image=self.getClassIcon())
        except TclError:
            pass
        if addChildren:
            defects = self.controller.getDefects()
            for defect in defects:
                defect_o = DefectController(Defect(defect))
                defect_vw = DefectView(
                    self.appliTw, self.appliViewFrame, self.mainApp, defect_o)
                defect_vw.addInTreeview(str(self.controller.getDbId()))

            tools = self.controller.getTools()
            for tool in tools:
                tool_o = ToolController(Tool(tool))
                tool_vw = ToolView(
                    self.appliTw, self.appliViewFrame, self.mainApp, tool_o)
                tool_vw.addInTreeview(str(self.controller.getDbId()))
        tools = self.controller.getTools()
        atleastone = False
        for tool in tools:  # SALE
            atleastone = True
            break
        if not atleastone:
            if len(self.controller.getTags()) == 0:
                self.controller.addTag("unscanned")
        self.appliTw.sort(parentNode)
        if "hidden" in self.controller.getTags():
            self.hide()

    def key(self):
        """Returns a key for sorting this node
        Returns:
            Tuple of 1 integer valus representing the prot number
        """
        return tuple([int(self.controller.getData()["port"])])

    def updateReceived(self):
        """Called when a port update is received by notification.
        Update the port node in summary
        """
        for module in self.mainApp.modules:
            if callable(getattr(module["object"], "updatePort", None)):
                module["object"].updatePort(self.controller.getData())
        super().updateReceived()

    def insertReceived(self):
        """Called when a port insertion is received by notification.
        Insert the node in summary.
        """
        for module in self.mainApp.modules:
            if callable(getattr(module["object"], "insertPort", None)):
                module["object"].insertPort(self.controller.getData())
