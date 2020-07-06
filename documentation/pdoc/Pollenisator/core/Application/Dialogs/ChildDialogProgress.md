Module Pollenisator.core.Application.Dialogs.ChildDialogProgress
================================================================
Show a progess bar for the user.

Classes
-------

`ChildDialogProgress(parent, title, msg, length=200, progress_mode='indeterminate')`
:   Open a child dialog of a tkinter application to inform the user about a ongoing process.
    
    Open a child dialog of a tkinter application to display a progress bar.
    
    Args:
        parent: the tkinter parent view to use for this window construction.
        title: Title for the new window
        msg: Message to display on the window to inform about a progession.
        length: Length of the progress bar, default to 200
        progress_mode: mode of progression. Either "determinate" or "inderterminate". Default to the second.
                       indeterminate: bouncing progress bar.
                       determinate: Show progression of a value against a max value.

    ### Methods

    `destroy(self)`
    :   Close the window and stop the progressbar.

    `show(self, maximum=None, startValue=0)`
    :   Start displaying the progressbar.
        Args:
            - maximum: only for determinate mode. Set the goal value. Default to None.
            - startValue: only for determinate mode. Set the starting value. Default to None.

    `update(self, value=None)`
    :   Update the progressbar and show progression value.
        Call this regularly if on inderminate mode.
        Args:
            - value: The new value for the progressbar. Default to None.