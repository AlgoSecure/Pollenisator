Module Pollenisator.core.Application.Treeviews.PollenisatorTreeview
===================================================================
PollenisatorTreeview abstract class
Ttk treeview abstract class to be inherited added functions.

Classes
-------

`PollenisatorTreeview(appli, parentFrame)`
:   PollenisatorTreeview class
    Defines common treeview features not implemented by ttk.
    Deletion, expand, collapse, contextualMenu, selection.
    Object stored in a tree view must have a unique iid.
    To make it easier, treeview iid used are their mongo database ID.
    For lists it is given by the view DbToTreeview method.
    
    Args:
        appli: a reference to the main Application object.
        parentFrame: the parent tkinter window object.

    ### Ancestors (in MRO)

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

    ### Class variables

    `dir_path`
    :

    ### Methods

    `closeMenu(self)`
    :   Does nothing. Used to close the contextual menu.

    `collapse(self)`
    :   Collapse all children recursivly of a treeview node.

    `deleteSelected(self, _event)`
    :   Interface to delete a database object from an event.
        Prompt the user a confirmation window.
        Args:
            _event: not used, a ttk Treeview event autofilled. Contains information on what treeview node was clicked.

    `deleteState(self, name)`
    :   Delete the given name state file
        file name is given in arguments and it must be stored as an hidden file in Pollenisator/local/states/ folder.
        Args:
            name: the name of this treeview to delete.
                  The full path to local/states folder and a Dot (".") will be prepended to the name.

    `doPopup(self, event)`
    :   Open the popup contextual menu of the treeview.
        
        Args:
            event: a ttk Treeview event autofilled. Contains information on what treeview node was clicked.

    `expand(self)`
    :   Expand all children recursivly of a treeview node.

    `filterTreeview(self, query, settings=None)`
    :   Deattach objects in the treeview that does not match the query and search settings.
        Args:
            query: filter query string
            settings: a dict of options:
                * "search_exact_match": for exact matching, default to False
                *  "search_show_hidden" : to enable showing hidden objects, default to False
             Default is None.
        Returns:
            True if the filter is done, else if an error occured. Most probably if the query is bad.

    `getViewFromId(self, dbId)`
    :   Craft a specific Molde from the Models classes with just a valid Mongo Object Id.
        
        Args:
            dbId: the database Mongo Id to return a view of.

    `load(self)`
    :   To be overriden
        Args:
            _event: not used, a ttk Treeview event autofilled. Contains information on what treeview node was clicked.

    `loadState(self, name)`
    :   Load opened nodes list state from a file.
        Restore the state if its exists.
        file name is given in arguments and it must be stored as an hidden file in Pollenisator/local/states/ folder.
        Args:
            name: the name of this treeview to save.
                  The full path to local/states folder and a Dot (".") will be prepended to the name.

    `onTreeviewSelect(self)`
    :   Return ObjectId of selection if it is a valid bson objectid.
        Else return the string of teeview iid.
        Make the viewframe empty.
        Args:
            _event: the treeview node clicked. Not used
        Returns:
            If selection is empty, returns None
            Return ObjectId of selection if it is a valid bson objectid.
            Else return the string of teeview iid.

    `popupFocusOut(self)`
    :   Called when the contextual menu loses focus. Closes it.
        Args:
            _event: default to None

    `resetTags(self, dbId)`
    :   Remove all tags of the node with given id.
        Args:
            dbId: The databaseID of the object to remove tags of

    `restoreTreeItemState(self, state)`
    :   Restore the given state.
        Args:
            state: a list of iid to open in the treeview.

    `saveState(self, name)`
    :   Save opened nodes list state to a file.
        file name is given in arguments and stored as an hidden file in Pollenisator/local/states/ folder.
        Args:
            name: the name of this treeview to save.
                  A Dot (".") will be prepended to the name to make the resulting file hidden on linux.

    `sort(self, node=None)`
    :   Sort the children node of a treeview node. The sorting key is the node's text.
        Args:
            node: the parent node to sort children of. 
                If none is given, will sort last right clicked node.
                Default is None.

    `switchExpandCollapse(self, openAction=True)`
    :   Expand or collapse all children recursivly of a treeview node.
        Args:
            openAction: Expand if True, Collapse if False.

    `unfilter(self)`
    :   Reattach all detached objects and reposition them.

    `unhideTemp(self)`
    :   Reattach all hidden objects but keep in memory that they are hidden.