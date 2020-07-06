Module Pollenisator.core.Application.Dialogs.ChildDialogDate
============================================================
Simple calendar using ttk Treeview together with calendar and datetime
classes.
Adapted from github.

Functions
---------

    
`get_calendar(locale, fwday)`
:   

Classes
-------

`ChildDialogDate(parent=None)`
:   

    ### Instance variables

    `selection`
    :   Return a datetime representing the current selected date.

    ### Methods

    `destroy(self)`
    :   Close the window.

    `initCalendar(self, master=None, **kw)`
    :   WIDGET-SPECIFIC OPTIONS
        
            locale, firstweekday, year, month, selectbackground,
            selectforeground

    `show(self)`
    :   Start displaying this window.