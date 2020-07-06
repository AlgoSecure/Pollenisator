Module Pollenisator.core.Views.PortView
=======================================
View for port object. Handle node in treeview and present forms to user when interacted with.

Classes
-------

`PortView(appTw, appViewFrame, mainApp, controller)`
:   View for port object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory
    
    Constructor
    Args:
        appTw: a PollenisatorTreeview instance to put this view in
        appViewFrame: an view frame to build the forms in.
        mainApp: the Application instance
        controller: a CommandController for this view.

    ### Ancestors (in MRO)

    * core.Views.ViewElement.ViewElement

    ### Class variables

    `icon`
    :

    ### Methods

    `addDefectCallback(self, _event)`
    :   Create an empty defect model and its attached view. Open this view insert window.
        
        Args:
            event: Automatically generated with a button Callback, not used but mandatory.

    `addInTreeview(self, parentNode=None, addChildren=True)`
    :   Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            addChildren: If False, skip the tool and defects insert. Useful when displaying search results

    `insertReceived(self)`
    :   Called when a port insertion is received by notification.
        Insert the node in summary.

    `key(self)`
    :   Returns a key for sorting this node
        Returns:
            Tuple of 1 integer valus representing the prot number

    `openInBrowser(self, _event)`
    :   Callback for action open in browser
        Args:
            _event: nut used but mandatory

    `openInsertWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to insert a new Port

    `openModifyWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to update or delete an existing Port

    `updateReceived(self)`
    :   Called when a port update is received by notification.
        Update the port node in summary