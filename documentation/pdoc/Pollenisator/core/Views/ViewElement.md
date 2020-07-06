Module Pollenisator.core.Views.ViewElement
==========================================
View parent object. Handle node in treeview and present forms to user when interacted with.

Classes
-------

`ViewElement(appTw, appViewFrame, mainApp, controller)`
:   Defines a basic view to be inherited. Those functions are generic entry points to models.
    Most of them should not be redefined in other Views.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory
        cachedClassIcon: a cached loaded PIL image icon of ViewElement.icon. Starts as None.
    
    Constructor
    Args:
        appTw: a PollenisatorTreeview instance to put this view in
        appViewFrame: an view frame to build the forms in.
        mainApp: the Application instance
        controller: a CommandController for this view.

    ### Class variables

    `cachedClassIcon`
    :

    `icon`
    :

    ### Static methods

    `DbToTreeviewListId(parent_db_id)`
    :   Converts a mongo Id to a unique string identifying a list of view elemnt given its parent
        Args:
            parent_db_id: the parent node mongo ID
        Returns:
            A string that should be unique to describe the parent list of viewelement node

    `getClassIcon()`
    :   Load the class icon in cache if it is not yet done, and returns it
        
        Return:
            Returns the ImageTk.PhotoImage icon representing this class .

    `list_tuple_to_dict(list_of_tuple)`
    :   Transforms a list of 2-tuple to a dictionnary
        Args:
            list_of_tuple: a 2-tuple with (key, value)
        Returns:
            A dictionnary with all key-values pair inserted

    ### Methods

    `addChildrenBaseNodes(self, newNode)`
    :   Add to the given node from a treeview the mandatory childrens.
        Will be redefined in children.
        
        Args:
            newNode: the newly created node we want to add children to.

    `completeInsertWindow(self)`
    :   Add the button for an insert window.
            -Insert button that validate the form with the insert function.

    `completeModifyWindow(self)`
    :   Add the buttons for an update window.
            -Submit button that validates the form with the update function.
            -Delete button that asks the user to delete the object with the delete function.

    `delete(self, showWarning=True)`
    :   Entry point to the model doDelete function.
        
        Args:
            _event: automatically filled if called by an event. Not used
            showWarning: a boolean. If true, the user will be asked a confirmation before supression. Default to True.

    `getIcon(self)`
    :   Load the object icon in cache if it is not yet done, and returns it
        
        Return:
            Returns the icon representing this object.

    `getParent(self)`
    :   Return the id of the parent node in treeview.
        
        Returns:
            return the model parent id DbToTreeviewListId

    `hide(self)`
    :   Tells the application treeview to hide this node

    `insert(self)`
    :   Entry point to the model doInsert function.
        
        Args:
            _event: automatically filled if called by an event. Not used
        Returns:
            * a boolean to shwo success or failure
            * an empty message on success, an error message on failure

    `insertReceived(self)`
    :   Called when any view element insert is received by notificaiton
        To be overriden

    `key(self)`
    :   Returns a key for sorting this node
        Returns:
            string, basic key: string so alphanumerical sorting will be used

    `showForm(self)`
    :   Resets the application view frame and start displaying the form in it

    `tagButtonClicked(self, name)`
    :   Callback for tag button clicked
        Ensure that the tag name clicked is set to View item
        Args:
            name: a tag name

    `tagClicked(self, name)`
    :   Callback intermediate for tag clicked
        Ensure that the tag name clicked is added to View item
        Args:
            name: a tag name

    `unhide(self)`
    :   Tells the application treeview to unhide this node

    `update(self, event=None)`
    :   Entry point to the model doUpdate function.
        
        Args:
            event: automatically filled if called by an event. Holds info on update clicked widget.
        Returns:
            * a boolean to shwo success or failure
            * an empty message on success, an error message on failure

    `updateReceived(self)`
    :   Called when any view element update is received by notification.
        Resets the node tags according to database and hide it if "hidden" is in tags