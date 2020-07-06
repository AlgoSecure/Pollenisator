Module Pollenisator.core.Views.MultiSelectionView
=================================================
View for multi selected object clicked. Present an multi modify form to user when interacted with.

Classes
-------

`MultiSelectionView(appliTw, appViewFrame, mainApp)`
:   View for multi selected object clicked. Present an multi modify form to user when interacted with.
    
    Constructor
    Args:
        appTw: a PollenisatorTreeview instance to put this view in
        appViewFrame: an view frame to build the forms in.
        mainApp: the Application instance
        controller: a CommandController for this view.

    ### Ancestors (in MRO)

    * core.Views.ViewElement.ViewElement

    ### Methods

    `openModifyWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to update or perform actions on multiple different objects common properties like tags.

    `tagClicked(self, name)`
    :   Separate callback to apply when a tag button is clicked
        Applies the clicked tag to all selected objects
        Args:
            name: tag name clicked