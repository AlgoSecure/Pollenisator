Module Pollenisator.core.Views.ScopeView
========================================
View for scope object. Handle node in treeview and present forms to user when interacted with.

Classes
-------

`ScopeView(appTw, appViewFrame, mainApp, controller)`
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

    ### Static methods

    `DbToTreeviewListId(parent_db_id)`
    :   Converts a mongo Id to a unique string identifying a list of scopes given its parent
        Args:
            parent_db_id: the parent node mongo ID
        Returns:
            A string that should be unique to describe the parent list of scope node

    `treeviewListIdToDb(treeview_id)`
    :   Extract from the unique string identifying a list of scopes the parent db ID
        Args:
            treeview_id: the treeview node id of a list of scopes node
        Returns:
            the parent object mongo id as string

    ### Methods

    `addChildrenBaseNodes(self, newNode)`
    :   Add to the given node from a treeview the mandatory childrens.
        For a Scope it is the tools parent node and the ips parent node
        
        Args:
            newNode: the newly created node we want to add children to.

    `addInTreeview(self, parentNode=None, addChildren=True)`
    :   Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            addChildren: If False, skip the tool insert. Useful when displaying search results

    `insertReceived(self)`
    :   Called when a scope insertion is received by notification.
        Tells the parent wave to update itself

    `key(self)`
    :   Returns a key for sorting this node
        Returns:
            Tuple of 5 integer valus representing the scope perimeter if network ip or self directly

    `openModifyWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to update or delete an existing Scope

    `split_ip(self)`
    :   Split a IP address given as string into a 5-tuple of integers.
        Returns:
            If network IP Tuple of 5 integers values representing the 4 parts of an ipv4 string + the /mask integer
            Otherwise returns self