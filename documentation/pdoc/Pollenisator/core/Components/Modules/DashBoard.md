Module Pollenisator.core.Components.Modules.DashBoard
=====================================================
Dashboard module to display pentest info

Classes
-------

`DashBoard(parent, settings)`
:   Shows information about ongoing pentest. 
    
    Constructor

    ### Class variables

    `conName`
    :

    `tabName`
    :

    ### Methods

    `displayData(self)`
    :   Display loaded data in treeviews

    `initUI(self, parent, nbk, treevw)`
    :   Initialize Dashboard widgets
        Args:
            parent: its parent widget

    `loadData(self)`
    :   Fetch data from database

    `mycallback(self, event)`
    :

    `open(self)`
    :

    `refreshUI(self)`
    :   Reload data and display them