Module Pollenisator.core.Views.MultipleIpView
=============================================
View for ip list object. Present an multi insertion form to user when interacted with.

Classes
-------

`MultipleIpView(appTw, appViewFrame, mainApp, controller)`
:   View for ip list object. Present an multi insertion form to user when interacted with.
    
    Constructor
    Args:
        appTw: a PollenisatorTreeview instance to put this view in
        appViewFrame: an view frame to build the forms in.
        mainApp: the Application instance
        controller: a CommandController for this view.

    ### Ancestors (in MRO)

    * core.Views.ViewElement.ViewElement

    ### Methods

    `openInsertWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to insert many new Ips