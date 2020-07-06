Module Pollenisator.core.Application.Dialogs.ChildDialogNewCalendar
===================================================================
Help the user to create a new pentest database.

Classes
-------

`ChildDialogNewCalendar(parent, default)`
:   Open a child dialog of a tkinter application to ask details about
    a new pentest database to create.
    
    Open a child dialog of a tkinter application to ask details about
    the new pentest.
    
    Args:
        parent: the tkinter parent view to use for this window construction.

    ### Methods

    `onOk(self, _event)`
    :   Called when the user clicked the validation button. Set the rvalue attributes to the value selected and close the window.
        
        Args:
            _event: not used but mandatory