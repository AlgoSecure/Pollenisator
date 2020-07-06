Module Pollenisator.core.Application.Dialogs.ChildDialogCombo
=============================================================
Defines a dialog window for choosing 1 between option many thourgh a combobox

Classes
-------

`ChildDialogCombo(parent, options, displayMsg='Choose a database to open:', default=None)`
:   Open a child dialog of a tkinter application to ask a user a calendar name.
    
    Open a child dialog of a tkinter application to ask a combobox option.
    
    Args:
        parent: the tkinter parent view to use for this window construction.
        options: A list of string correspondig to options of the combobox
        displayMsg: The message that will explain to the user what he is choosing.
        default: Choose a default selected option (one of the string in options). default is None

    ### Methods

    `onError(self)`
    :   Close the dialog and set rvalue to None

    `onOk(self)`
    :   Called when the user clicked the validation button. Set the rvalue attributes to the value selected and close the window.