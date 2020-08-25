"""View for scope object. Handle node in treeview and present forms to user when interacted with."""

from core.Controllers.ToolController import ToolController
from core.Models.Tool import Tool
from core.Views.IpView import IpView
from core.Views.ToolView import ToolView
from core.Views.ViewElement import ViewElement
from tkinter import TclError

class ScopeView(ViewElement):
    """View for port object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory"""

    icon = 'scope.png'

    def openModifyWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to update or delete an existing Scope
        """
        modelData = self.controller.getData()
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("Scope", column=0)
        top_panel.addFormStr("Scope", '', modelData["scope"], None, column=1, state="readonly")
        notes = modelData.get("notes", "")
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("Notes")
        self.form.addFormText("Notes", r"", notes, None, side="top")
        self.completeModifyWindow()

    def addChildrenBaseNodes(self, newNode):
        """
        Add to the given node from a treeview the mandatory childrens.
        For a Scope it is the tools parent node and the ips parent node

        Args:
            newNode: the newly created node we want to add children to.
        """

        return self.appliTw.insert(newNode, "end", IpView.DbToTreeviewListId(newNode), text="IPs", image=IpView.getClassIcon())

    def addInTreeview(self, parentNode=None, addChildren=True):
        """Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            addChildren: If False, skip the tool insert. Useful when displaying search results
        """
        parentDbId = parentNode
        if parentNode is None:
            parentNode = self.getParent()
        elif 'scopes' not in parentNode:
            parentNode = ScopeView.DbToTreeviewListId(parentDbId)
        self.appliTw.views[str(self.controller.getDbId())] = {"view":self}
        try:
            parentNode = self.appliTw.insert(
                self.controller.getParent(), 0, parentNode, text="Scopes", image=self.getClassIcon())
        except TclError:  #  trigger if tools list node already exist
            pass
        self.appliTw.insert(parentNode, "end", str(
            self.controller.getDbId()), text=str(self.controller.getModelRepr()), tags=self.controller.getTags(), image=self.getClassIcon())
        if addChildren:
            tools = self.controller.getTools()
            for tool in tools:
                tool_o = ToolController(Tool(tool))
                tool_vw = ToolView(self.appliTw, self.appliViewFrame, self.mainApp, tool_o)
                tool_vw.addInTreeview(str(
                   self.controller.getDbId()))
        if "hidden" in self.controller.getTags():
            self.hide()

    @classmethod
    def treeviewListIdToDb(cls, treeview_id):
        """Extract from the unique string identifying a list of scopes the parent db ID
        Args:
            treeview_id: the treeview node id of a list of scopes node
        Returns:
            the parent object mongo id as string
        """
        return str(treeview_id).split("|")[1]

    @classmethod
    def DbToTreeviewListId(cls, parent_db_id):
        """Converts a mongo Id to a unique string identifying a list of scopes given its parent
        Args:
            parent_db_id: the parent node mongo ID
        Returns:
            A string that should be unique to describe the parent list of scope node
        """
        return "scopes|"+str(parent_db_id)

    def split_ip(self):
        """Split a IP address given as string into a 5-tuple of integers.
        Returns:
            If network IP Tuple of 5 integers values representing the 4 parts of an ipv4 string + the /mask integer
            Otherwise returns self"""
        modelData = self.controller.getData()
        try:
            ret = tuple(int(part) for part in modelData["scope"].split('.'))
            ret = ret + tuple(int(modelData["scope"].split('/')[1]))
        except ValueError:
            ret = tuple(str(part) for part in modelData["scope"].split('.'))
        return ret

    def insertReceived(self):
        """Called when a scope insertion is received by notification.
        Tells the parent wave to update itself
        """
        if self.controller.model is None:
            return
        parentId = self.controller.getParent()
        parentView = self.appliTw.views[str(parentId)]["view"]
        parentView.updateReceived()
        super().insertReceived()

    def key(self):
        """Returns a key for sorting this node
        Returns:
            Tuple of 5 integer valus representing the scope perimeter if network ip or self directly
        """
        return self.split_ip()
