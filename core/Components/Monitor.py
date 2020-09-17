"""
Keep track of all celery workers. Also launchs, monitors and stops celery tasks.
"""
from celery import Celery
import threading
import multiprocessing
from core.Components.Worker import Worker
import core.Components.Utils as Utils
import json
import os
from bson.objectid import ObjectId
from bson.errors import InvalidId
import ssl
from core.Models.Tool import Tool
from core.Components.mongo import MongoCalendar
import AutoScanWorker as slave


class Monitor:
    """
    Keep track of all celery workers. Also launchs, monitors and stops celery tasks.
    """
    def __init__(self, calendar):
        """
        Constructor. Connect to Celery and start the thread receiving celery worker's events.
        Args:
            calendar: the pentest database name to monitor
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        ssldir = os.path.join(dir_path, "../../ssl/")
        certs = {
            'keyfile': ssldir+'client.pem',
            'certfile': ssldir+'server.pem',
            'ca_certs': ssldir+'ca.pem',
            'cert_reqs': ssl.CERT_REQUIRED
        }
        # manager = multiprocessing.Manager()
        # self.worker_list = manager.dict()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cfg = Utils.loadClientConfig()
        userString = cfg["user"]+':'+cfg["password"] + \
            '@' if cfg['user'].strip() != "" else ""
        if cfg["ssl"] == "True":
            self.app = Celery('tasks', broker='mongodb://' + userString + cfg["host"] + ":"+cfg["mongo_port"] +
                              '/broker_pollenisator?authSource=admin&ssl=true&ssl_ca_certs='+certs["ca_certs"]+'&ssl_certfile='+certs["keyfile"], connect_timeout=5000)
        else:
            self.app = Celery('tasks', broker='mongodb://' + userString + cfg["host"] + ":"+cfg["mongo_port"] +
                              '/broker_pollenisator?authSource=admin', connect_timeout=5000)

        self.state = self.app.events.State()
        self.tasks_running = []
        self.recv = None
        self.calendar = calendar
        # Shared worker list between the child process and main.
        self.willStop = False
        self.removeInactiveWorkersTimer = threading.Timer(
            30, self.removeInactiveWorkers)
        self.removeInactiveWorkersTimer.start()
        self.processEvent = None
        self.processEvent = threading.Thread(
            target=self.run, args=(str(calendar), ))  #  This a thread not a process as it needs to catch this app Ctrl+C
        self.processEvent.start()

    def removeInactiveWorkers(self):
        """
        Remove inactive workers every 30s
        """
        print("Time to remove inactive workers !")
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.removeInactiveWorkers()
        # if not self.willStop:
        #     self.removeInactiveWorkersTimer = threading.Timer(
        #         30, self.removeInactiveWorkers)
        #     self.removeInactiveWorkersTimer.start()

    def stopWorkersTimer(self):
        """
        Stops the removing of inactive workers.
        """
        self.willStop = True
        if self.removeInactiveWorkers is not None:
            self.removeInactiveWorkersTimer.cancel()

    def stopTask(self, launchableTool):
        """
        Stop the celery task corresponding to the given tool

        Args:
            launchableTool: a Tool document instance that was presumably launched.

        Returns:
            Return True if a tasks has been stopped, False otherwise.
        """
        for task_running in self.tasks_running:
            if task_running[1] == launchableTool["_id"]:
                task_running[0].revoke(terminate=True)
                del task_running

                return True
        return False

    
    def launchTask(self, calendarName, launchableTool, parser="", checks=True, workerName=""):
        """
        launch the celery task corresponding to the given tool

        Args:
            calendarNamse: the calendar where the tool given is
            launchableTool: a Tool document instance to launch.
            parser: the plugin to use when the tool will be over, default to "" which means let the worker conf file decides.
            checks: will check if worker selected has registered the launchable tool, default to True.
            workerName: (Opt.) a worker name to use ("localhost" is valid)

        Returns:
            False if no worker was found capable of launching the given tool, True otherwise
        """
        mongoInstance = MongoCalendar.getInstance()
        # Check all workers to see if any space is availiable
        from AutoScanWorker import executeCommand
        if workerName == "":
            workers = mongoInstance.getWorkers()
            for worker in workers:
                if launchableTool is None:
                    continue
                worker = Worker(worker["name"])
                if worker.hasRegistered(launchableTool):
                    if checks == False:
                        workerName = worker.name
                    else:
                        if launchableTool is None:
                            continue
                        if worker.hasSpaceFor(launchableTool, mongoInstance.calendarName):
                            workerName = worker.name
                            break
        # If no workers are availiable, stop there
        if workerName == "":
            return False

        launchableToolId = launchableTool.getId()
        launchableTool.markAsRunning(workerName)
        # Mark the tool as running (scanner_ip is set and dated is set, datef is "None")
        # Add a queue to the selected worker for this tool, So that only this worker will receive this task
        if workerName != "localhost":
            queueName = str(mongoInstance.calendarName)+"&" + \
                workerName+"&"+launchableTool.name
            self.app.control.add_consumer(
                queue=queueName,
                reply=True,
                exchange="celery",
                exchange_type="direct",
                routing_key="transient",
                destination=[workerName])
            result_async = executeCommand.apply_async(args=[calendarName, str(
                launchableToolId), parser], queue=queueName, retry=False, serializer="json")
            # Append to running tasks this celery result and the corresponding tool id
            self.tasks_running.append([result_async, launchableToolId])
        else:
            thread = None
            thread = multiprocessing.Process(target=slave.executeCommand, args=(
                mongoInstance.calendarName, str(launchableToolId), parser))
            thread.start()

        # Execute this celery task
        return True

    def getWorkerList(self):
        """
        Return the worker list

        Returns:
            Return the workers name list
        """
        mongoInstance = MongoCalendar.getInstance()
        l = []
        workers = mongoInstance.getWorkers()
        for worker in workers:
            l.append(worker["name"])
        return l

    def hasWorkers(self):
        """
        Check if any worker is availiable

        Returns:
            Return True if at least one worker is availiable, False otherwise.
        """
        return len(self.getWorkerList()) > 0

    def stop(self):
        """
        Stop monitoring the celery events and revoke all celery tasks
        """

        for task_running in self.tasks_running:
            task_running[0].revoke(terminate=True)
        self.stopWorkersTimer()
        if self.processEvent is not None:
            self.app.control.purge()
            self.app.connection()
            # if self.processEvent._popen is not None:  # pylint: disable=protected-access
            print("Stopping monitoring... ")
            self.recv.should_stop = True
            print("Stopped monitoring")

    def addOnlineWorker(self, worker_hostname):
        """
        Register a celery worker on the worker's list. Also deletes old queues and messages

        Args:
            worker_hostname: the worker hostname to register on worker's list
        """
        mongoInstance = MongoCalendar.getInstance()
        agg_queues = mongoInstance.aggregateFromDb("broker_pollenisator", "messages.routing", [{"$group": {"_id": "$queue"}}, {
            "$match": {"_id": {"$regex": "^.*&"+worker_hostname+"&.*$"}}}])
        mongoInstance.deleteFromDb("broker_pollenisator", "messages.routing", {
            "queue": {"$regex": "^.*&"+worker_hostname+"&.*$"}}, True)
        for agg_queue in agg_queues:
            Utils.execute("celery -A slave purge -f -Q '" +

                          agg_queue["_id"]+"'", None, False)
        
        self.workerRegisterCommands(worker_hostname)

    def updateWorkerLastHeartbeat(self, worker_hostname):
        """Update the given worker last hearthbeat
        Args:
            worker_hostname: the worker name to be refreshed
        """
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.updateWorkerLastHeartbeat(worker_hostname)

    def workerRegisterCommands(self, worker_hostname):
        """Force a worker to register its configured command in database
        Args:
            worker_hostname: the worker name to be forced to register its commands
        """
        mongoInstance = MongoCalendar.getInstance()
        queueName = str(worker_hostname)+"&getcommands"
        self.app.control.add_consumer(
            queue=queueName,
            reply=True,
            exchange="celery",
            exchange_type="direct",
            routing_key="transient",
            destination=[worker_hostname])
        # print "adding get command"
        from AutoScanWorker import getCommands
        getCommands.apply_async(
            args=[mongoInstance.calendarName, worker_hostname], queue=queueName, retry=True, serializer="json")
        return

    def removeWorker(self, worker_hostname):
        """Remove a worker from database
        Args:
            worker_hostname: the worker name to be removed
        """
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.removeWorker(worker_hostname)

    ########################################################
    ############# CELERY EVENTS CALLBACK BLOCK #############
    ########################################################

    def announce_failed_tasks(self, event):
        """
        Called when a celery task fails. Is used to reset dates and scanner of the targeted tool.

        Args:
            event: created automatically when the event occurs. Contains some info about the task
        """
        self.state.event(event)
        task = self.state.tasks.get(event['uuid'])  # get task
        # Get tasks arguments
        try:
            argsWere = json.loads(task.info()["args"].replace("'", "\""))
            args = argsWere[0]
            toolId = ObjectId(args[1])  # args[1] is the tool_id
            for task_running in self.tasks_running:
                if str(task_running[1]) == str(toolId):
                    task_running[0].revoke(terminate=True)
                    del task_running
            tool = Tool.fetchObject({"_id": ObjectId(toolId)})
            tool.markAsNotDone()
        except InvalidId:
            pass
        except json.decoder.JSONDecodeError:
            pass
        except KeyError:
            pass  # Plugin failed so "args" does not exist

    def announce_online_worker(self, event):
        """
        Called when a celery worker get online. Is used to register this worker in the worker_list

        Args:
            event: created automatically when the event occurs. Contains some info about the worker
        """
        print("RECEIVED ONLINE EVENT")
        worker_hostname = event["hostname"].strip()
        workers = self.getWorkerList()
        # print "WORKER ONLINE :"+str(worker_hostname)
        if worker_hostname not in list(workers):
            self.addOnlineWorker(worker_hostname)

    def announce_offline_worker(self, event):
        """
        Called when a celery worker gets offline nicely. Is used to remove this worker from the worker_list

        Args:
            event: created automatically when the event occurs. Contains some info about the worker
        """
        worker_hostname = event["hostname"].strip()
        workers = self.getWorkerList()
        print("RECEIVE OFFLINE WORKER "+str(worker_hostname))

        if worker_hostname in list(workers):
            toolsToReset = Tool.fetchObjects(
                {"datef": "None", "scanner_ip": worker_hostname})
            for tool in toolsToReset:
                tool.markAsNotDone()
            self.removeWorker(worker_hostname)

    def announce_heartbeat_worker(self, event):
        """
        Called when a celery worker sends a heartbeat. Is used to register this worker in the worker_list if not already in.
        Online event is only sent once. If celery workers were already launched, this will not be resend.

        Args:
            event: created automatically when the event occurs. Contains some info about the worker
        """
        worker_hostname = event["hostname"].strip()
        workers = self.getWorkerList()
        # print "WORKER Heartbeat, can be received without having online if worker was already live :"+worker_hostname
        if worker_hostname not in workers:
            # datef "added worker already up"
            self.addOnlineWorker(worker_hostname)
        else:
            self.updateWorkerLastHeartbeat(worker_hostname)

    def on_event(self, event):
        """
        Capture all other events.

        Args:
            event: created automatically when the event occurs. Contains some info about the event
        """
        # pass

    def run(self, calendar):
        """
        Start monitoring celery events
        Will stop when receiving a KeyboardInterrupt
        Args:
            calendar: the pentest database name to monitor
        """
        print("Starting monitor thread")
        try:
            self.recv = None
            self.calendar = calendar
            with self.app.connection() as connection:
                self.recv = self.app.events.Receiver(connection, handlers={
                    'task-failed': self.announce_failed_tasks,
                    'worker-online': self.announce_online_worker,
                    'worker-offline': self.announce_offline_worker,
                    'worker-heartbeat': self.announce_heartbeat_worker,
                    '*': self.on_event,
                })
                self.recv.capture(limit=None, timeout=None, wakeup=True)
        except(KeyboardInterrupt, SystemExit):
            self.recv.should_stop = True
            print("Should stop received...")
            self.stop()
        self.recv.should_stop = True
        print("Should stop received...")
        self.stop()
        print("Ending monitor thread")
