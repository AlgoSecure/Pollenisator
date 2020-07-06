Module Pollenisator.core.Application.Treeviews.CalendarTreeview
===============================================================
CalendarTreeview class
Ttk treeview class with added functions.

Classes
-------

`CalendarTreeview(appli, parentFrame)`
:   Inherit PollenisatorTreeview.
    Ttk treeview class with added functions to handle the main view objects.
    
    Args:
        appli: a reference to the main Application object.
        parentFrame: the parent tkinter window object.

    ### Ancestors (in MRO)

    * core.Application.Treeviews.PollenisatorTreeview.PollenisatorTreeview
    * tkinter.ttk.Treeview
    * tkinter.ttk.Widget
    * tkinter.Widget
    * tkinter.BaseWidget
    * tkinter.Misc
    * tkinter.Pack
    * tkinter.Place
    * tkinter.Grid
    * tkinter.XView
    * tkinter.YView

    ### Methods

    `closeMenu(self)`
    :   Close the contextual menu. Does nothing, just an empty callback
        Args:
            - _event: not used but mandatory

    `customCommand(self)`
    :   Ask the user for a custom tool to launch and which parser it will use.
        Args:
            _event: not used but mandatory

    `doPopup(self, event)`
    :   Called when a right click is received by the tree view.
        Open the contextual menu at the clicked position.
        Args:
            - event: sent automatically though an event on treeview

    `doPopupTag(self, event)`
    :   Called when a middle click is received by the tree view.
        Open the tag menu at the clicked position.
        Args:
            - event: sent automatically though an event on treeview

    `exportSelection(self)`
    :   Popup a window to help a user to export some data from treeview.
        Args:
            _event: not used but mandatory

    `getRows(self, startNode='')`
    :   Returns all child nodes of the given startNode iid as a list.
        Args:
            - startNode: node to recursively get children. Default to '' which is rhe treeview root.
        Returns:
            - List of all children iid of given node.

    `hide(self, node=None, updateTags=False)`
    :   Hide given node object in the treeview and can store this effect in its tag.
        Args:
            - node: node to hide. If none is given, the contextualMenu.selection value will be used.
                    Default to None.
            - updateTags: mark the object as hidden in its tags. Default to False

    `hideAndUpdate(self)`
    :   Hide object with contextualMenu attached in the treeview and store this effect in its tags.

    `hideSelection(self)`
    :   Hide selected objects in the treeview and store this effect in their tags.

    `initUI(self)`
    :   Initialize the user interface widgets and binds them.

    `load(self, searchModel=None)`
    :   Load the treeview with database information
        Args:
            searchModel: (DEPRECATED) a search object default to None

    `notify(self, db, collection, iid, action, _parent)`
    :   Callback for the observer implemented in mongo.py.
        Each time an object is inserted, updated or deleted the standard way, this function will be called.
        
        Args:
            collection: the collection that has been modified
            iid: the mongo ObjectId _id that was modified/inserted/deleted
            action: string "update" or "insert" or "delete". It was the action performed on the iid
            _parent: Not used. the mongo ObjectId of the parent. Only if action in an insert. Not used anymore

    `onTreeviewSelect(self, event=None)`
    :   Called when a line is selected on the treeview
        Open the selected object view on the view frame.
        Args:
            _event: not used but mandatory

    `openModifyWindowOf(self, dbId)`
    :   Retrieve the View of the database id given and open the modifying form for its model.
        Args:
            dbId: the Mongo Id to open the modification form on.

    `openNextSameTypeNode(self, _event)`
    :   Open the first node of the same type below the currently selected object on the tree view.
        Args:
            - _event: not used but mandatory
        Return:
            return the string "break" to stop processing the event

    `openPrevSameTypeNode(self, _event)`
    :   Open the first node of the same type above the currently selected object on the tree view.
        Args:
            - _event: not used but mandatory
        Return:
            return the string "break" to stop processing the event

    `popupFocusOutTag(self)`
    :   Called when the tag contextual menu is unfocused.
        Close the tag contextual menu.

    `refresh(self)`
    :   Alias to load function

    `setTagFromMenubar(self, name)`
    :   Change the tags of every selected object in the treeview to the one selected in the tag contextual menu.
        Args:
            - name: the tag name clicked

    `showInTreeview(self)`
    :   Unfilter the treeview and focus the node stored in the contextualMenu.selection variable0
        Also select it.

    `tagClicked(self, name)`
    :   Callback for an event. If the function was called directly it would not work.
        Args:
            - name: the tag name clicked

    `unhide(self, node=None)`
    :   Unhide children of given node.
        Args:
            - node: the node which we want to unhide the children.
                    If this value is None, use the contextualMenu.selection value
                    Default to None.