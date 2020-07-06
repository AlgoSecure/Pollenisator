Module Pollenisator.core.Application.Dialogs.ChildDialogFileParser
==================================================================
Ask the user to select a file or directory and then parse it with the selected parser

Functions
---------

    
`md5(fname)`
:   Compute md5 hash of the given file name.
    Args:
        fname: path to the file you want to compute the md5 of.
    Return:
        The digested hash of the file in an hexadecimal string format.

Classes
-------

`ChildDialogFileParser(parent)`
:   Open a child dialog of a tkinter application to ask details about
    existing files parsing.
    
    Open a child dialog of a tkinter application to ask details about
    existing files parsing.
    
    Args:
        parent: the tkinter parent view to use for this window construction.

    ### Methods

    `onOk(self)`
    :   Called when the user clicked the validation button.
        launch parsing with selected parser on selected file/directory.
        Close the window.
        
        Args:
            _event: not used but mandatory