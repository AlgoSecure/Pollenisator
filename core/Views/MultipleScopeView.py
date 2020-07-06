"""View for scope list object. Present an multi insertion form to user when interacted with."""

from core.Views.ViewElement import ViewElement
from core.Views.ScopeView import ScopeView


class MultipleScopeView(ViewElement):
    """View for scope list object. Present an multi insertion form to user when interacted with."""


    def openInsertWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to insert many new Scopes
        """
        modelData = self.controller.getData()
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("Scopes")
        top_panel.addFormHelper(
            "Add Network IP 'XXX.XXX.XXX.XXX/XX' or domain names to the pentest's scope\nEach network/domain name must on a separated line", column=1)
        top_panel = self.form.addFormPanel()
        top_panel.addFormText("Scopes", r"^(?!https?://).+$", "", None, side="top")
        top_panel = self.form.addFormPanel()
        top_panel.addFormCheckbox(
            "Split", "Make ip range split into /24 at most", False, side="left")
        top_panel.addFormHelper(
            "This will split big ranges in smaller one. May slow pollenisator opening.\nBut you will have scan results quicker", side="left")
        top_panel = self.form.addFormPanel()
        top_panel.addFormCheckbox(
            "Settings", "Check domain scope", True, side="left")
        top_panel.addFormHelper(
            "If you want to insert a brand new scope in the scope, you will have to disable this security", side="left")
        self.form.addFormHidden("wave", modelData["wave"])
        self.completeInsertWindow()

    def addChildrenBaseNodes(self, newNode):
        """
        Add to the given node from a treeview the mandatory childrens.
        For a scope it is the tools parent node and the ips parent node.

        Args:
            newNode: the newly created node we want to add children to.
        """
        ScopeView(self.appliTw, self.appliViewFrame, self.mainApp,
                  self.controller).addChildrenBaseNodes(newNode)
