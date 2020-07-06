Module Pollenisator.core.Components.Modules.Summary
===================================================
Controllers for summary view of notebook

Functions
---------

    
`smart_grid(parent, root, *args, **kwargs)`
:   Grid adapted to each treeview size.
    Adapted from stackoverflow but cannot find it anymore =/

Classes
-------

`ScrollFrame(parent)`
:   A scrollable frame using canvas
    
    Constructor

    ### Ancestors (in MRO)

    * tkinter.Frame
    * tkinter.Widget
    * tkinter.BaseWidget
    * tkinter.Misc
    * tkinter.Pack
    * tkinter.Place
    * tkinter.Grid

    ### Methods

    `onFrameConfigure(self, _event)`
    :   Reset the scroll region to encompass the inner frame

`Summary(root, settings)`
:   Store elements to summarize the ongoing pentest
    
    Constructor
    Args:
        root: the root widget of tkinter

    ### Class variables

    `iconName`
    :

    `tabName`
    :

    ### Methods

    `OnDoubleClick(self, event)`
    :   Callback for treeview double click.
        If a link treeview is defined, open mainview and focus on the item with same iid clicked.
        Args:
            event: used to identified which link was clicked. Auto filled

    `deleteIp(self, ip)`
    :   Remvoe an IP from the summary.
        Args:
            ip: an IP object to be removed

    `initUI(self, parent, nbk, linkTw)`
    :   Initialize widgets of the summary
        Args:
            parent: parent tkinter container widget 
            nbk: a ref to the notebook
            linkTw: the treeview holding more info in the notebook to be displayed after an interaction

    `insertIp(self, ip)`
    :   Insert a new IP in the summary. Also insert its port
        Args:
            ip: an IP object to be inserted

    `insertPort(self, port_o)`
    :   Insert a new port in the summary
        Args:
            port_o: a port object to be inserted

    `loadSummary(self)`
    :   Reload information about IP and Port and reload the view.

    `open(self)`
    :

    `refreshUI(self)`
    :   Refresh information then reloads the view with them.

    `updatePort(self, port_data)`
    :   Update a port line according to a new port_data (just change colors now)
        Args:
            port_data: a port data dictionnary