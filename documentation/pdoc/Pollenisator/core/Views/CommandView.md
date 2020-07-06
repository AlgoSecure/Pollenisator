Module Pollenisator.core.Views.CommandView
==========================================
View for command object. Handle node in treeview and present forms to user when interacted with.

Classes
-------

`CommandView(appTw, appViewFrame, mainApp, controller)`
:   View for command object. Handle node in treeview and present forms to user when interacted with.
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
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.

    `addIpDirVariable(self)`
    :   insert the ip_dir variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.

    `addIpReseauDirVariable(self)`
    :   insert the scope_dir variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.

    `addIpReseauVariable(self)`
    :   insert the scope variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.

    `addIpVariable(self)`
    :   insert the ip variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.

    `addParentDomainVariable(self)`
    :   insert the scope variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.

    `addPortVariable(self)`
    :   insert the port variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.

    `addWaveVariable(self)`
    :   insert the wave variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.

    `getParent(self)`
    :   Return the id of the parent node in treeview.
        
        Returns:
            return the saved command_node node inside the Appli class.

    `key(self)`
    :   Returns a key for sorting this node
        Returns:
            string, key to sort

    `openInsertWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to insert a new Command

    `openModifyWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to update or delete an existing Command

    `popup(self, event)`
    :   Fill the self.widgetMenuOpen and reraise the event in the editing window contextual menu
        
        Args:
            event: a ttk Treeview event autofilled. Contains information on what treeview node was clicked.

    `popupFocusOut(self)`
    :   Called when the contextual menu is unfocused
        Args:
            _event: a ttk event autofilled. not used but mandatory.