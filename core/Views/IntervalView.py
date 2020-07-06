"""View for interval object. Handle node in treeview and present forms to user when interacted with."""

from core.Views.ViewElement import ViewElement
from tkinter import TclError


class IntervalView(ViewElement):
    """View for interval object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory.
    """

    icon = 'date.png'

    def openModifyWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to update or delete an existing Interval
        """
        modelData = self.controller.getData()
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("Start date")
        top_panel.addFormDate(
            "Start date", self.mainApp, modelData["dated"], column=1)
        top_panel.addFormLabel("End date", row=1)
        top_panel.addFormDate("End date", self.mainApp, modelData["datef"], row=1, column=1)
        top_panel.addFormHelper(
            "Auto scan will only launch if current time fits this interval", row=1, column=2)
        # added in getEmptyModel
        self.form.addFormHidden("waveName", modelData["wave"])
        self.completeModifyWindow()

    def openInsertWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to insert a new Interval
        """
        modelData = self.controller.getData()
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("Start date")
        top_panel.addFormDate("Start date", self.mainApp, "01/01/2000 00:00:00", column=1)
        top_panel.addFormLabel("End date", row=1)
        top_panel.addFormDate(
            "End date", self.mainApp, "31/12/2099 00:00:00", row=1, column=1)
        top_panel.addFormHelper(
            "Auto scan will only launch if current time fits this interval", row=1, column=2)
        # added in getEmptyModel
        self.form.addFormHidden("waveName", modelData["wave"])

        self.completeInsertWindow()

    def addInTreeview(self, parentNode=None, _addChildren=True):
        """Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            _addChildren: not used here
        """
        parentDbId = parentNode
        if parentNode is None:
            parentNode = self.getParent()
        elif "intervals" not in parentNode:
            parentNode = IntervalView.DbToTreeviewListId(parentDbId)
        try:
            parentNode = self.appliTw.insert(
                self.controller.getParent(), 0, parentNode, text="Intervals", image=self.getClassIcon())
        except TclError:  #  trigger if tools list node already exist
            pass
        self.appliTw.views[str(self.controller.getDbId())] = {"view": self}
        self.appliTw.insert(parentNode, "end", str(
            self.controller.getDbId()), text=str(self.controller.getModelRepr()), tags=self.controller.getTags(), image=self.getClassIcon())
        if "hidden" in self.controller.getTags():
            self.hide()

    def updateReceived(self):
        """Called when a interval update is received by notification.
        Update the interval node and tells to the parent wave to update (its tools).
        """
        if self.controller.model is None:
            return
        parentId = self.controller.getParent()
        parentView = self.appliTw.views[str(parentId)]["view"]
        parentView.updateReceived()
        super().updateReceived()

    def insertReceived(self):
        """Called when a interval insertion is received by notification.
        Insert the node in treeview.
        Also tells to the parent wave to update (its tools)
        """
        if self.controller.model is None:
            return
        parentId = self.controller.getParent()
        parentView = self.appliTw.views[str(parentId)]["view"]
        parentView.updateReceived()
        super().insertReceived()

    @classmethod
    def treeviewListIdToDb(cls, treeview_id):
        """Extract from the unique string identifying a list of intervals the parent db ID
        Args:
            treeviewId: the treeview node id of a list of intervals node
        Returns:
            the parent object mongo id as string
        """
        return str(treeview_id).split("|")[1]

    @classmethod
    def DbToTreeviewListId(cls, parent_db_id):
        """Converts a mongo Id to a unique string identifying a list of intervals given its parent
        Args:
            parent_db_id: the parent node mongo ID
        Returns:
            A string that should be unique to describe the parent list of interval node
        """
        return "intervals|"+str(parent_db_id)
