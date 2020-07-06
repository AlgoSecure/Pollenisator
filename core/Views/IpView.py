"""View for ip object. Handle node in treeview and present forms to user when interacted with."""

from core.Models.Port import Port
from core.Models.Tool import Tool
from core.Models.Defect import Defect
from core.Models.Ip import Ip
from core.Views.PortView import PortView
from core.Views.ToolView import ToolView
from core.Views.DefectView import DefectView
from core.Controllers.PortController import PortController
from core.Controllers.DefectController import DefectController
from core.Controllers.IpController import IpController
from core.Controllers.ToolController import ToolController
from core.Views.ViewElement import ViewElement
from tkinter import TclError
from bson.objectid import ObjectId


class IpView(ViewElement):
    """View for ip object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory."""
    icon = 'ip.png'

    def openModifyWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to update or delete an existing Ip
        """
        modelData = self.controller.getData()
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("Ip")
        top_panel.addFormStr(
            "Ip", '', modelData["ip"], None, column=1, state="readonly")
        notes = modelData.get("notes", "")
        top_panel = self.form.addFormPanel()
        top_panel.addFormLabel("Notes", side="top")
        top_panel.addFormText("Notes", r"", notes, None, side="top", height=10)
        top_panel.addFormLabel("Infos", side="left")
        top_panel.addFormTreevw("Infos", ("Infos", "Values"),
                                modelData["infos"], side="left", fill="both", width=300, height=8,
                                binds={"<Enter>": self.mainApp.unboundToMousewheelMain, "<Leave>": self.mainApp.boundToMousewheelMain})
        buttons_panel = self.form.addFormPanel(grid=True)
        buttons_panel.addFormButton("Add a port", self.addPortCallback)
        buttons_panel.addFormButton(
            "Add a security defect", self.addDefectCallback, column=1)
        self.completeModifyWindow()

    def addPortCallback(self, _event):
        """
        Create an empty port model and its attached view. Open this view insert window.

        Args:
            _event: Automatically generated with a button Callback, not used.
        """
        for widget in self.appliViewFrame.winfo_children():
            widget.destroy()
        modelData = self.controller.getData()
        pv = PortView(self.appliTw, self.appliViewFrame,
                      self.mainApp, PortController(Port(modelData)))
        pv.openInsertWindow()

    def addDefectCallback(self, _event):
        """
        Create an empty defect model and its attached view. Open this view insert window.

        Args:
            _event: Automatically generated with a button Callback, not used.
        """
        for widget in self.appliViewFrame.winfo_children():
            widget.destroy()
        modelData = self.controller.getData()
        dv = DefectView(self.appliTw, self.appliViewFrame, self.mainApp,
                        DefectController(Defect(modelData)))
        dv.openInsertWindow(modelData.get("notes", ""))

    def _insertChildrenDefects(self):
        """Insert every children defect in database as DefectView under this node"""
        defects = self.controller.getDefects()
        for defect in defects:
            defect_o = DefectController(Defect(defect))
            defect_vw = DefectView(
                self.appliTw, self.appliViewFrame, self.mainApp, defect_o)
            defect_vw.addInTreeview(str(self.controller.getDbId()))

    def _insertChildrenTools(self):
        """Create a tools list node and insert every children tools in database as ToolView under this node"""
        tools = self.controller.getTools()
        for tool in tools:
            tool_o = ToolController(Tool(tool))
            tool_vw = ToolView(
                self.appliTw, self.appliViewFrame, self.mainApp, tool_o)
            tool_vw.addInTreeview(str(self.controller.getDbId()))

    def _insertChildrenPorts(self, ip_node):
        """Insert every children port in database as DefectView under this node directly"""
        ports = self.controller.getPorts()
        for port in ports:
            port_o = PortController(Port(port))
            port_vw = PortView(
                self.appliTw, self.appliViewFrame, self.mainApp, port_o)
            port_vw.addInTreeview(ip_node)

    def addInTreeview(self, parentNode=None, addChildren=True):
        """Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            _addChildren: not used here
        """
        if parentNode is None:
            parentNode = self.getParent()
        ip_node = None
        try:
            if isinstance(parentNode, ObjectId):
                ip_parent_o = Ip.fetchObject({"_id": parentNode})
                if ip_parent_o is not None:
                    parent_view = IpView(self.appliTw, self.appliViewFrame,
                                         self.mainApp, IpController(ip_parent_o))
                    parent_view.addInTreeview(None, False)
            ip_node = self.appliTw.insert(parentNode, "end", str(
                self.controller.getDbId()), text=str(self.controller.getModelRepr()), tags=self.controller.getTags(), image=self.getClassIcon())
        except TclError:
            pass
        self.appliTw.views[str(self.controller.getDbId())] = {"view": self}
        if addChildren and ip_node is not None:
            self._insertChildrenDefects()
            self._insertChildrenTools()
            self._insertChildrenPorts(ip_node)
        # self.appliTw.sort(parentNode)
        if "hidden" in self.controller.getTags():
            self.hide()
        modelData = self.controller.getData()
        if not modelData["in_scopes"]:
            self.controller.addTag("OOS")

    def split_ip(self):
        """Split a IP address given as string into a 4-tuple of integers.
        Returns:
            Tuple of 4 integers values representing the 4 parts of an ipv4 string"""
        modelData = self.controller.getData()
        try:
            ret = tuple(int(part) for part in modelData["ip"].split('.'))
        except ValueError:
            ret = tuple([0])+tuple(ord(chrDomain)
                                   for chrDomain in modelData["ip"])
        return ret

    def key(self):
        """Returns a key for sorting this node
        Returns:
            Tuple of 4 integers values representing the 4 parts of an ipv4 string, key to sort ips properly
        """
        return self.split_ip()

    def insertReceived(self):
        """Called when a IP insertion is received by notification.
        Insert the node in summary.
        Can also insert in treeview with OOS tags.
        """
        modelData = self.controller.getData()
        if modelData.get("in_scopes", []):
            self.mainApp.summary.insertIp(modelData["ip"])
        else:
            self.appliTw.item(str(self.controller.getDbId()), text=str(
                self.controller.getModelRepr()), image=self.getIcon())
            self.controller.addTag("OOS")

    def updateReceived(self):
        """Called when a IP update is received by notification.
        Update the ip node OOS status tags and add/remove it from summary.
        """
        if self.controller.model is not None:
            modelData = self.controller.getData()
            if not modelData["in_scopes"]:
                self.controller.addTag("OOS")
                self.mainApp.summary.deleteIp(modelData["ip"])
            else:
                self.controller.delTag("OOS")
                self.mainApp.summary.insertIp(modelData["ip"])
            super().updateReceived()

    def getParent(self):
        """
        Return the id of the parent node in treeview.

        Returns:
            return the parent ips_node of application treeview
        """
        #parent = self.controller.getParent()
        #if parent is None:
        parent = self.appliTw.ips_node
        return parent
