Module Pollenisator.core.Components.Monitor
===========================================
Keep track of all celery workers. Also launchs, monitors and stops celery tasks.

Classes
-------

`Monitor(calendar)`
:   Keep track of all celery workers. Also launchs, monitors and stops celery tasks.
    
    Constructor. Connect to Celery and start the thread receiving celery worker's events.
    Args:
        calendar: the pentest database name to monitor

    ### Methods

    `addOnlineWorker(self, worker_hostname)`
    :   Register a celery worker on the worker's list. Also deletes old queues and messages
        
        Args:
            worker_hostname: the worker hostname to register on worker's list

    `announce_failed_tasks(self, event)`
    :   Called when a celery task fails. Is used to reset dates and scanner of the targeted tool.
        
        Args:
            event: created automatically when the event occurs. Contains some info about the task

    `announce_heartbeat_worker(self, event)`
    :   Called when a celery worker sends a heartbeat. Is used to register this worker in the worker_list if not already in.
        Online event is only sent once. If celery workers were already launched, this will not be resend.
        
        Args:
            event: created automatically when the event occurs. Contains some info about the worker

    `announce_offline_worker(self, event)`
    :   Called when a celery worker gets offline nicely. Is used to remove this worker from the worker_list
        
        Args:
            event: created automatically when the event occurs. Contains some info about the worker

    `announce_online_worker(self, event)`
    :   Called when a celery worker get online. Is used to register this worker in the worker_list
        
        Args:
            event: created automatically when the event occurs. Contains some info about the worker

    `getWorkerList(self)`
    :   Return the worker list
        
        Returns:
            Return the workers name list

    `hasWorkers(self)`
    :   Check if any worker is availiable
        
        Returns:
            Return True if at least one worker is availiable, False otherwise.

    `launchTask(self, calendarName, launchableTool, parser='', checks=True, workerName='')`
    :   launch the celery task corresponding to the given tool
        
        Args:
            calendarNamse: the calendar where the tool given is
            launchableTool: a Tool document instance to launch.
            parser: the plugin to use when the tool will be over, default to "" which means let the worker conf file decides.
            checks: will check if worker selected has registered the launchable tool, default to True.
            workerName: (Opt.) a worker name to use ("localhost" is valid)
        
        Returns:
            False if no worker was found capable of launching the given tool, True otherwise

    `on_event(self, event)`
    :   Capture all other events.
        
        Args:
            event: created automatically when the event occurs. Contains some info about the event

    `removeInactiveWorkers(self)`
    :   Remove inactive workers every 30s

    `removeWorker(self, worker_hostname)`
    :   Remove a worker from database
        Args:
            worker_hostname: the worker name to be removed

    `run(self, calendar)`
    :   Start monitoring celery events
        Will stop when receiving a KeyboardInterrupt
        Args:
            calendar: the pentest database name to monitor

    `stop(self)`
    :   Stop monitoring the celery events and revoke all celery tasks

    `stopTask(self, launchableTool)`
    :   Stop the celery task corresponding to the given tool
        
        Args:
            launchableTool: a Tool document instance that was presumably launched.
        
        Returns:
            Return True if a tasks has been stopped, False otherwise.

    `stopWorkersTimer(self)`
    :   Stops the removing of inactive workers.

    `updateWorkerLastHeartbeat(self, worker_hostname)`
    :   Update the given worker last hearthbeat
        Args:
            worker_hostname: the worker name to be refreshed

    `workerRegisterCommands(self, worker_hostname)`
    :   Force a worker to register its configured command in database
        Args:
            worker_hostname: the worker name to be forced to register its commands