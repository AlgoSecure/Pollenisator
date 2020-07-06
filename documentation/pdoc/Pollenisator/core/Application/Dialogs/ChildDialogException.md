Module Pollenisator.core.Application.Dialogs.ChildDialogException
=================================================================
Defines a dialog window to display an error

Functions
---------

    
`postIssue(_err)`
:   Open a tab in a browser to github issues page.
    Args:
        _err: Not used

Classes
-------

`ChildDialogException(parent, title, err)`
:   Open a child dialog of a tkinter application to present the user to an unhandled exception.
    Can be used to report issue to github.
    
    Open a child dialog of a tkinter application to present the user to an unhandled exception.
    Can be used to report issue to github.
    Args:
        parent: the tkinter parent view to use for this window construction.
        title: A title for the new windows
        err: the error that occured causing this window to appear

    ### Methods

    `onError(self)`
    :   Close the dialog and set rvalue to None
        Args:
            _event: not used but mandatory

    `onOk(self)`
    :   Called when the user clicked the validation button. Set the rvalue attributes to the value selected and close the window.
        
        Args:
            _event: not used but mandatory