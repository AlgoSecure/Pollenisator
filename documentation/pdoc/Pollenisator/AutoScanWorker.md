Module Pollenisator.AutoScanWorker
==================================
Celery worker module. Execute code and store results in database, files in the SFTP server.

Functions
---------

    
`autoScanv2(databaseName, workerName)`
:   Search tools to launch within defined conditions and attempts to launch them this celery worker.
    Gives a visual feedback on stdout
    
    Args:
        databaseName: The database to search tools in
        endless: a boolean that indicates if the autoscan will be endless or if it will stop at the moment it does not found anymore launchable tools.
        useReprinter: a boolean that indicates if the array outpur will be entirely reprinted or if it will be overwritten.

    
`dispatchLaunchableToolsv2(launchableTools, worker)`
:   Try to launch given tools within the monitor
    
    Args:
        my_monitor: A Monitor instance which knows what tools are already launched and online workers
        launchableTools: A list of tools within a Wave that passed the Intervals checking.

    
`executeCommand(toolId, parser='')`
:   CELERY remote task
    Execute the tool with the given toolId on the given calendar name.
    Then execute the plugin corresponding.
    Any unhandled exception will result in a task-failed event in the Monitor class.
    
    Args:
        calendarName: The calendar to search the given tool id for.
        toolId: the mongo Object id corresponding to the tool to execute.
        parser: plugin name to execute. If empty, the plugin specified in tools.d will be feteched.
    Raises:
        Terminated: if the task gets terminated
        OSError: if the output directory cannot be created (not if it already exists)
        Exception: if an exception unhandled occurs during the bash command execution.
        Exception: if a plugin considered a failure.

    
`findLaunchableToolsOnWorker(worker, calendarName)`
:   Try to find tools that matches all criteria.
    Args:
        workerName: the current working worker
    Returns:
        A tuple with two values:
            * A list of launchable tools as dictionary with values _id, name and priority
            * A dictionary of waiting tools with tool's names as keys and integer as value.

    
`fix_multiprocessing(**kwargs)`
:   

    
`getCommands(worker_name)`
:   CELERY remote task
    List worker registered tools in configuration folder.
    Store the results in mongo database in pollenisator.workers database.

    
`getWaveTimeLimit(waveName)`
:   Return the latest time limit in which this tool fits. The tool should timeout after that limit
    
    Args:
        tool: a tool belonging to a wave to get the time limit of.
    
    Returns:
        Return the latest time limit in which this tool fits.

    
`launchTask(calendarName, worker, launchableTool)`
:   

    
`startAutoScan(workerName)`
: