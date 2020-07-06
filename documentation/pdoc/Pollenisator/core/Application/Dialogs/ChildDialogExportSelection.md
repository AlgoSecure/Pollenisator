Module Pollenisator.core.Application.Dialogs.ChildDialogExportSelection
=======================================================================
ChildDialogExportSelection class
Ask the user to select fields and returns the selected options

Classes
-------

`ChildDialogExportSelection(parent, keys)`
:   Open a child dialog of a tkinter application to ask the user to select fields between many.
    
    Open a child dialog of a tkinter application to ask details about
    an export of treeview items.
    
    Args:
        parent: the tkinter parent view to use for this window construction.
        keys: The keys to export

    ### Methods

    `onOk(self)`
    :   Called the the Export button is pressed.
        return a list of strings corresponding to the selected fields.
        
        Args:
            _event: not used but mandatory