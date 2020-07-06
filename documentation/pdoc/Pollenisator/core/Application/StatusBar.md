Module Pollenisator.core.Application.StatusBar
==============================================
StatusBar class. Show tagged elements numbers to user.

Classes
-------

`StatusBar(master, registeredTags, statusbarController)`
:   StatusBar class. Show tagged numbers to user.
    Inherits ttk.Frame
    
    Constructor of the status bar
    Args:
        master: parent tkinter window
        registeredTags: a list of tag names registred in settings
        statusbarController: a controller to handle clicks on status bar.
                            It has to delcare a statusbarClicked function taking 1 arg : a tag name

    ### Ancestors (in MRO)

    * tkinter.ttk.Frame
    * tkinter.ttk.Widget
    * tkinter.Widget
    * tkinter.BaseWidget
    * tkinter.Misc
    * tkinter.Pack
    * tkinter.Place
    * tkinter.Grid

    ### Methods

    `notify(self, addedTags, removedTags=[])`
    :   Notify is called when tags are added or removed
        Args:
            addedTags: a list of tag names added
            removedTags: a list of tag names removed, default to []

    `reset(self)`
    :   Rest all displayed tags count to 0

    `tagClicked(self, name)`
    :   A lambda to call the statusbarController.statusbarClicked with the tag name clicked
        Args:
            name: the tag name clicked

    `update(self)`
    :   Update all tags label to tags count