Module Pollenisator.core.Application.Dialogs.ChildDialogCustomCommand
=====================================================================
Deprecated.
Ask the user to enter a command and select a worker and plugin to launch it.

Classes
-------

`ChildDialogCustomCommand(parent, workers, default_worker='localhost')`
:   Open a child dialog of a tkinter application to ask details about
    a custom command to launch on target.
    
    Open a child dialog of a tkinter application to ask details about
    a custom command to launch on target.
    
    Args:
        parent: the tkinter parent view to use for this window construction.
        workers: A list of workers registered.
        default_worker: a worker to be selected by default.

    ### Methods

    `onOk(self)`
    :   Called when the user clicked the validation button. Set the rvalue attributes to the value selected and close the window.