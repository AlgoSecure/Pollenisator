Module Pollenisator.core.Views.MultipleScopeView
================================================
View for scope list object. Present an multi insertion form to user when interacted with.

Classes
-------

`MultipleScopeView(appTw, appViewFrame, mainApp, controller)`
:   View for scope list object. Present an multi insertion form to user when interacted with.
    
    Constructor
    Args:
        appTw: a PollenisatorTreeview instance to put this view in
        appViewFrame: an view frame to build the forms in.
        mainApp: the Application instance
        controller: a CommandController for this view.

    ### Ancestors (in MRO)

    * core.Views.ViewElement.ViewElement

    ### Methods

    `addChildrenBaseNodes(self, newNode)`
    :   Add to the given node from a treeview the mandatory childrens.
        For a scope it is the tools parent node and the ips parent node.
        
        Args:
            newNode: the newly created node we want to add children to.

    `openInsertWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to insert many new Scopes