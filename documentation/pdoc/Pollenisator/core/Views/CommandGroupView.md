Module Pollenisator.core.Views.CommandGroupView
===============================================
View for command group object. Handle node in treeview and present forms to user when interacted with.

Classes
-------

`CommandGroupView(appTw, appViewFrame, mainApp, controller)`
:   View for command group object. Handle node in treeview and present forms to user when interacted with.
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

    `addInTreeview(self, parentNode=None)`
    :   Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: not used

    `getParent(self)`
    :   Return the id of the parent node in treeview.
        
        Returns:
            return the saved group_command_node node inside the Appli class.

    `openInsertWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to insert a new CommandGroup

    `openModifyWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to update or delete an existing CommandGroup