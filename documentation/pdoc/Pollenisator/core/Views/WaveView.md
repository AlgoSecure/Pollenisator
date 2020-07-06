Module Pollenisator.core.Views.WaveView
=======================================
View for wavr object. Handle node in treeview and present forms to user when interacted with.

Classes
-------

`WaveView(appTw, appViewFrame, mainApp, controller)`
:   View for wavr object. Handle node in treeview and present forms to user when interacted with.
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

    `addChildrenBaseNodes(self, newNode)`
    :   Add to the given node from a treeview the mandatory childrens.
        For a wave it is the intervals parent node and the copes parent node.
        
        Args:
            newNode: the newly created node we want to add children to.
        Returns:
            * the created Intervals parent node
            * the created Scope parent node

    `addInTreeview(self, parentNode=None, addChildren=True)`
    :   Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            addChildren: If False: skip interval, tools and scope insert. Useful when displaying search results.

    `getParent(self)`
    :   Return the id of the parent node in treeview.
        
        Returns:
            return the saved waves_node inside the Appli class.

    `openInsertWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to insert a new Wave

    `openModifyWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to update or delete an existing Wave