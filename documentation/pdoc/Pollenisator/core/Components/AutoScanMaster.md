Module Pollenisator.core.Components.AutoScanMaster
==================================================
Module for orchestrating an automatic scan. Must be run in a separate thread/process.

Functions
---------

    
`autoScan(databaseName, endless, useReprinter=False)`
:   Search tools to launch within defined conditions and attempts to launch them on celery workers.
    Gives a visual feedback on stdout
    
    Args:
        databaseName: The database to search tools in
        endless: a boolean that indicates if the autoscan will be endless or if it will stop at the moment it does not found anymore launchable tools.
        useReprinter: a boolean that indicates if the array outpur will be entirely reprinted or if it will be overwritten.

    
`dispatchLaunchableTools(my_monitor, launchableTools)`
:   Try to launch given tools within the monitor
    
    Args:
        my_monitor: A Monitor instance which knows what tools are already launched and online workers
        launchableTools: A list of tools within a Wave that passed the Intervals checking.

    
`findLaunchableTools()`
:   Try to find tools that matches all criteria.
    
    Returns:
        A tuple with two values:
            * A list of launchable tools as dictionary with values _id, name and priority
            * A dictionary of waiting tools with tool's names as keys and integer as value.

    
`main()`
:   May be used to start an automatic scan without having to launch a GUI.

    
`printStatus(max_tabulation, waiting, reprinter=None)`
:   Print to stdout the ongoing scan information.
    Args:
        max_tabulation: The longest column content length
        waiting: a dictionnary filled with commands that are not launched yet.
        reprinter: a reprinter object instance. If none, a normal print will be used. Default to None.

    
`sendStartAutoScan(calendarName)`
:   

Classes
-------

`GracefulKiller()`
:   Signal handler to shut down properly.
    
    Attributes:
        kill_now: a boolean that can checked to know that it's time to stop.
    
    Constructor. Hook the signals SIGINT and SIGTERM to method exitGracefully

    ### Class variables

    `kill_now`
    :

    ### Methods

    `exitGracefully(self, _signum, _frame)`
    :   Set the kill_now class attributes to True
        
        Args:
            _signum: not used. Sent automatically the caller.
            _frame: not used. Sent automatically the caller.

`Reprinter()`
:   A useful class to erase the precedent print before reprinting. Giving the impression of a static print.
    
    Constructor

    ### Methods

    `reprint(self, text)`
    :   Erase precedent print and print the new text.
        Args:
            text: The new text to print