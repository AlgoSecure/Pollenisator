Module Pollenisator.core.Application.Dialogs.ChildDialogInfo
============================================================
Display a simple information for the user.

Classes
-------

`ChildDialogInfo(parent, title, msg)`
:   Open a child dialog of a tkinter application to inform the user.
    
    Open a child dialog of a tkinter application to choose autoscan settings.
    
    Args:
        parent: the tkinter parent view to use for this window construction.
        title: title of the popup window
        msg: Message to show to the user

    ### Methods

    `destroy(self)`
    :   Close the window.

    `show(self)`
    :   Start displaying this window.