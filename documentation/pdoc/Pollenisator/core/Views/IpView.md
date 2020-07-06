Module Pollenisator.core.Views.IpView
=====================================
View for ip object. Handle node in treeview and present forms to user when interacted with.

Classes
-------

`IpView(appTw, appViewFrame, mainApp, controller)`
:   View for ip object. Handle node in treeview and present forms to user when interacted with.
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

    ### Methods

    `addDefectCallback(self, _event)`
    :   Create an empty defect model and its attached view. Open this view insert window.
        
        Args:
            _event: Automatically generated with a button Callback, not used.

    `addInTreeview(self, parentNode=None, addChildren=True)`
    :   Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            _addChildren: not used here

    `addPortCallback(self, _event)`
    :   Create an empty port model and its attached view. Open this view insert window.
        
        Args:
            _event: Automatically generated with a button Callback, not used.

    `getParent(self)`
    :   Return the id of the parent node in treeview.
        
        Returns:
            return the parent ips_node of application treeview

    `insertReceived(self)`
    :   Called when a IP insertion is received by notification.
        Insert the node in summary.
        Can also insert in treeview with OOS tags.

    `key(self)`
    :   Returns a key for sorting this node
        Returns:
            Tuple of 4 integers values representing the 4 parts of an ipv4 string, key to sort ips properly

    `openModifyWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to update or delete an existing Ip

    `split_ip(self)`
    :   Split a IP address given as string into a 4-tuple of integers.
        Returns:
            Tuple of 4 integers values representing the 4 parts of an ipv4 string

    `updateReceived(self)`
    :   Called when a IP update is received by notification.
        Update the ip node OOS status tags and add/remove it from summary.