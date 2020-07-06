Module Pollenisator.core.Components.ScanManager
===============================================
Hold functions to interact form the scan tab in the notebook

Functions
---------

    
`autoscan_execute(calendarName)`
:   Call the autoScan function with given pentest name as endless and no reprint.
    
    Args:
        calendarName: the pentest database name to auto scan.

Classes
-------

`ScanManager(nbk, linkedTreeview, calendarToScan, settings)`
:   Scan model class
    
    Constructor, initialize a Monitor object

    ### Methods

    `OnDoubleClick(self, event)`
    :   Callback for a double click on ongoing scan tool treeview. Open the clicked tool in main view and focus on it.
        Args:
            event: Automatically filled when event is triggered. Holds info about which line was double clicked

    `initUI(self, parent)`
    :   Create widgets and initialize them
        Args:
            parent: the parent tkinter widget container.

    `notify(self, _iid, _action)`
    :   Reload UI when notified

    `parseFiles(self)`
    :   Ask user to import existing files to import.

    `refreshUI(self)`
    :   Reload informations and renew widgets

    `startAutoscan(self)`
    :   Start an automatic scan. Will try to launch all undone tools.

    `stop(self)`
    :   Stop an automatic scan. Will try to stop running tools.

    `stopAutoscan(self)`
    :   Stop an automatic scan. Will terminate celery running tasks.