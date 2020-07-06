Module Pollenisator.core.Views.IntervalView
===========================================
View for interval object. Handle node in treeview and present forms to user when interacted with.

Classes
-------

`IntervalView(appTw, appViewFrame, mainApp, controller)`
:   View for interval object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory.
    
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

    ### Static methods

    `DbToTreeviewListId(parent_db_id)`
    :   Converts a mongo Id to a unique string identifying a list of intervals given its parent
        Args:
            parent_db_id: the parent node mongo ID
        Returns:
            A string that should be unique to describe the parent list of interval node

    `treeviewListIdToDb(treeview_id)`
    :   Extract from the unique string identifying a list of intervals the parent db ID
        Args:
            treeviewId: the treeview node id of a list of intervals node
        Returns:
            the parent object mongo id as string

    ### Methods

    `addInTreeview(self, parentNode=None)`
    :   Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            _addChildren: not used here

    `insertReceived(self)`
    :   Called when a interval insertion is received by notification.
        Insert the node in treeview.
        Also tells to the parent wave to update (its tools)

    `openInsertWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to insert a new Interval

    `openModifyWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to update or delete an existing Interval

    `updateReceived(self)`
    :   Called when a interval update is received by notification.
        Update the interval node and tells to the parent wave to update (its tools).