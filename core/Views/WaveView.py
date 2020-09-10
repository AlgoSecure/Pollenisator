"""View for wavr object. Handle node in treeview and present forms to user when interacted with."""

from core.Views.ViewElement import ViewElement
from core.Models.Command import Command
from core.Models.Interval import Interval
from core.Views.IntervalView import IntervalView
from core.Models.Scope import Scope
from core.Views.ScopeView import ScopeView
from core.Views.ToolView import ToolView
from core.Controllers.IntervalController import IntervalController
from core.Controllers.ScopeController import ScopeController
from core.Controllers.ToolController import ToolController
from core.Components.mongo import MongoCalendar



class WaveView(ViewElement):
    """View for wavr object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory"""

    icon = 'wave.png'

    def openModifyWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to update or delete an existing Wave
        """
        modelData = self.controller.getData()
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("Wave", modelData["wave"])
        self.form.addFormHelper(
            "If you select a previously unselected command,\n it will be added to every object of its level.\nIf you unselect a previously selected command,\n it will remove only tools that are not already done.")
        self.form.addFormChecklist(
            "Commands", Command.getList(None, MongoCalendar.getInstance().calendarName), modelData["wave_commands"])
        self.completeModifyWindow()

    def openInsertWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to insert a new Wave
        """
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("Wave")
        top_panel.addFormStr("Wave", r".+", "", column=1)
        self.form.addFormHelper("Only selected commands will be launchable.")
        self.form.addFormChecklist("Commands", Command.getList(None, MongoCalendar.getInstance().calendarName), [])
        self.completeInsertWindow()

    def addChildrenBaseNodes(self, newNode):
        """
        Add to the given node from a treeview the mandatory childrens.
        For a wave it is the intervals parent node and the copes parent node.

        Args:
            newNode: the newly created node we want to add children to.
        Returns:
            * the created Intervals parent node
            * the created Scope parent node
        """
        d = self.appliTw.insert(newNode, "end", IntervalView.DbToTreeviewListId(
            self.controller.getDbId()), text="Intervals", image=IntervalView.getClassIcon())
        s = self.appliTw.insert(newNode, "end", ScopeView.DbToTreeviewListId(
            self.controller.getDbId()), text="Scopes", image=ScopeView.getClassIcon())
        return d, s

    def addInTreeview(self, parentNode=None, addChildren=True):
        """Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            addChildren: If False: skip interval, tools and scope insert. Useful when displaying search results.
        """
        parentNode = self.getParent()
        self.appliTw.views[str(self.controller.getDbId())] = {
            "view": self, 'parent': ''}
        wave_node = self.appliTw.insert(parentNode, "end", str(self.controller.getDbId()), text=str(
            self.controller.getModelRepr()), tags=self.controller.getTags(), image=self.getClassIcon())
        if addChildren:
            dates_node, scopes_node = self.addChildrenBaseNodes(wave_node)
            intervals = self.controller.getIntervals()
            for interval in intervals:
                interval_vw = IntervalView(
                    self.appliTw, self.appliViewFrame, self.mainApp, IntervalController(Interval(interval)))
                interval_vw.addInTreeview(dates_node)
            tools = self.controller.getTools()
            for tool in tools:
                tool_o = ToolController(tool)
                tool_vw = ToolView(
                    self.appliTw, self.appliViewFrame, self.mainApp, tool_o)
                tool_vw.addInTreeview(str(self.controller.getDbId()))
            scopes = self.controller.getScopes()
            for scope in scopes:
                scope_o = ScopeController(Scope(scope))
                scope_vw = ScopeView(
                    self.appliTw, self.appliViewFrame, self.mainApp, scope_o)
                scope_vw.addInTreeview(scopes_node)
        if "hidden" in self.controller.getTags():
            self.hide()

    def getParent(self):
        """
        Return the id of the parent node in treeview.

        Returns:
            return the saved waves_node inside the Appli class.
        """
        return self.appliTw.waves_node


