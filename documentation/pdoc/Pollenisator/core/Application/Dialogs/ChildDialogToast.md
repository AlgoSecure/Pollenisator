Module Pollenisator.core.Application.Dialogs.ChildDialogToast
=============================================================
Show a message to the user for a limited amount of time

Classes
-------

`ChildDialogToast(parent, text, *args, **kwargs)`
:   floating basic window with info text inside, fading away after a short time.
        
    
    create the floating window but do not display it
    
    Args:
        parent: the tkinter parent view to use for this window construction.
        text: the text to display inside the toast
        args: not used
        kwargs: 
            - if fadingTime is defined, delay before fading starts. Default to 1.0s
            - if x is defined, x position of the toast top left corner, else default to parent x +25 .
            - if y is defined, y position of the toast top left corner, else default to parent botoom - 100.

    ### Ancestors (in MRO)

    * tkinter.Toplevel
    * tkinter.BaseWidget
    * tkinter.Misc
    * tkinter.Wm

    ### Methods

    `fade(self)`
    :

    `show(self)`
    :   show the floating window, fading on 1.0 sec