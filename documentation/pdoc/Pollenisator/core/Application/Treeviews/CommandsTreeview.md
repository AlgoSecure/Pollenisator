Module Pollenisator.core.Application.Treeviews.CommandsTreeview
===============================================================
Ttk treeview class with added functions.

Classes
-------

`CommandsTreeview(appli, parentFrame)`
:   CommandsTreeview class
    Inherit PollenisatorTreeview.
    Ttk treeview class with added functions to handle the command objects.
    
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

    `doPopup(self, event)`
    :   Open the popup 
        Args:
            event: filled with the callback, contains data about line clicked

    `initUI(self)`
    :   Initialize the user interface widgets and binds them.
        Args:
            _event: not used but mandatory

    `load(self)`
    :   Load the treeview with database information
        
        Args:
            _searchModel: (Deprecated) inherited not used.

    `notify(self, db, collection, iid, action, parent)`
    :   Callback for the observer pattern implemented in mongo.py.
        
        Args:
            collection: the collection that has been modified
            iid: the mongo ObjectId _id that was modified/inserted/deleted
            action: update/insert/delete. It was the action performed on the iid
            parent: the mongo ObjectId of the parent. Only if action in an insert.

    `onTreeviewSelect(self, event=None)`
    :   Called when a line is selected on the treeview
        Open the selected object view on the view frame.
        IF it's a parent commands or command_groups node, opens Insert
        ELSE open a modify window
        Args:
            event: filled with the callback, contains data about line clicked

    `openModifyWindowOf(self, dbId)`
    :   Retrieve the View of the database id given and open the modifying form for its model and open it.
        
        Args:
            dbId: the database Mongo Id to modify.

    `refresh(self)`
    :   Alias to self.load method