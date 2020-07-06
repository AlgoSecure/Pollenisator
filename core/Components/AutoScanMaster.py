"""Module for orchestrating an automatic scan. Must be run in a separate thread/process."""
import argparse
import re
import signal
import sys
import time
import ssl
from bson.objectid import ObjectId
from celery import Celery
from bson.objectid import ObjectId
import os
import core.Components.Utils as Utils
from core.Components.mongo import MongoCalendar
from core.Components.Monitor import Monitor
from core.Models.Wave import Wave
from core.Models.Tool import Tool

dir_path = os.path.dirname(os.path.realpath(__file__))  # fullpath to this file
ssldir = os.path.join(dir_path, "../../ssl/")  # fullepath to ssl directory
certs = {
    'keyfile': ssldir+'client.pem',
    'certfile': ssldir+'server.pem',
    'ca_certs': ssldir+'ca.pem',
    'cert_reqs': ssl.CERT_REQUIRED
}
try:
    cfg = Utils.loadCfg(os.path.join(dir_path, "../../config/client.cfg"))
except FileNotFoundError:
    print("No client config was found under Pollenisator/config/client.cfg. Create one from the sample provided in this directory.")
    sys.exit(0)
user_string = cfg["user"]+':'+cfg["password"] + \
    '@' if cfg['user'].strip() != "" else ""
if cfg["ssl"] == "True":
    app = Celery('tasks', broker='mongodb://'+user_string+cfg["host"] + ':' + cfg["mongo_port"] +
                 '/broker_pollenisator?authSource=admin&ssl=true&ssl_ca_certs='+certs["ca_certs"]+'&ssl_certfile='+certs["keyfile"])
else:
    app = Celery('tasks', broker='mongodb://' + user_string +
                 cfg["host"] + ':'+cfg["mongo_port"] + '/broker_pollenisator?authSource=admin')

class Reprinter:
    """
    A useful class to erase the precedent print before reprinting. Giving the impression of a static print.
    """

    def __init__(self):
        """
        Constructor
        """
        self.text = ''

    def _moveup(self, lines):
        """
        Put the cursor up by X lines
        Args:
            lines: the X number of lines
        """
        for _ in range(lines):
            sys.stdout.write("\x1b[A")

    def reprint(self, text):
        """
        Erase precedent print and print the new text.
        Args:
            text: The new text to print
        """
        # Clear previous text by overwritig non-spaces with spaces
        self._moveup(self.text.count("\n"))
        sys.stdout.write(re.sub(r"[^\s]", " ", self.text))

        # Print new text
        lines = min(self.text.count("\n"), text.count("\n"))
        self._moveup(lines)
        sys.stdout.write(text)
        self.text = text


class GracefulKiller:
    """
    Signal handler to shut down properly.

    Attributes:
        kill_now: a boolean that can checked to know that it's time to stop.
    """
    kill_now = False

    def __init__(self):
        """
        Constructor. Hook the signals SIGINT and SIGTERM to method exitGracefully
        """
        signal.signal(signal.SIGINT, self.exitGracefully)
        signal.signal(signal.SIGTERM, self.exitGracefully)
        #signal.signal(signal.SIGPIPE, signal.SIG_DFL)

    def exitGracefully(self, _signum, _frame):
        """
        Set the kill_now class attributes to True

        Args:
            _signum: not used. Sent automatically the caller.
            _frame: not used. Sent automatically the caller.
        """
        print('You pressed Ctrl+C!')
        self.kill_now = True


def main():
    """May be used to start an automatic scan without having to launch a GUI.
    """
    #######################################
    ############## MAIN ###################
    #######################################

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="Launch commands described in a database stored in a mongodb for each scope also in this file")
    parser.add_argument("database", metavar="databaseName", type=str,
                        help="The database's name to launch in the mongodb")
    parser.add_argument("--backup", dest="backup", metavar="backupName", type=str,
                        help="The name of the backup database that will be written (overwrite if file name already exists) in the mongodb as the input database is completed")
    parser.add_argument("-y", dest="autooverride",
                        action="store_true", help="Accept all user input asked")
    parser.add_argument("--endless", dest="endless", action="store_true")
    #parser.add_argument("-p", dest="port" , metavar="port", type=int, help="The port on which to join the slaves")

    args = parser.parse_args()
    # Connect to database
    mongoInstance = MongoCalendar.getInstance()
    mongoInstance.connect()
    # backup database if the parser caught this argument and agreement has been done
    if args.backup is not None and args.backup in mongoInstance.listCalendars():
        if args.backup in mongoInstance.forbiddenNames:
            print(args.backup+" is a restricted name")
            sys.exit(0)
        if not args.autooverride:
            print("You are going to overwrite an existing db (" +
                  args.backup+"), proceed ? (n/Y)")
            res = input()
        else:
            res = "Y"
        if res == "Y":
            mongoInstance.client.drop_database(args.backup)
        else:
            print("The autorization to write to the output database was not provided.")
            sys.exit(0)
    else:
        if mongoInstance.client is None:
            mongoInstance.connect()
        mongoInstance.insertInDb(
            "pollenisator", "calendars", {"nom": args.backup})
    if args.backup is not None:
        mongoInstance.client.admin.command('copydb',
                                           fromdb=args.database,
                                           todb=args.backup)
    # Start autoscan with settings
    autoScan(args.database, args.endless, False)


def sendStartAutoScan(calendarName):
    mongoInstance = MongoCalendar.getInstance()
    mongoInstance.connectToDb(calendarName)
    workers = mongoInstance.getWorkers()
    launchedTasks = []
    for worker in workers:
        worker = worker["name"]
        if worker != "localhost":
            queueName = str(mongoInstance.calendarName)+"&" + \
                worker
            app.control.add_consumer(
                queue=queueName,
                reply=True,
                exchange="celery",
                exchange_type="direct",
                routing_key="transient",
                destination=[worker])
            from AutoScanWorker import startAutoScan
            result_async = startAutoScan.apply_async(args=[calendarName, worker], queue=queueName, retry=False, serializer="json")
            launchedTasks.append(result_async)
            # Append to running tasks this celery result and the corresponding tool id
    return launchedTasks


def autoScan(databaseName, endless, useReprinter=False):
    """
    Search tools to launch within defined conditions and attempts to launch them on celery workers.
    Gives a visual feedback on stdout

    Args:
        databaseName: The database to search tools in
        endless: a boolean that indicates if the autoscan will be endless or if it will stop at the moment it does not found anymore launchable tools.
        useReprinter: a boolean that indicates if the array outpur will be entirely reprinted or if it will be overwritten.
    """
    mongoInstance = MongoCalendar.getInstance()
    mongoInstance.connectToDb(databaseName)
    my_monitor = Monitor(databaseName)
    Utils.resetUnfinishedTools()
    time_compatible_waves_id = Wave.searchForAddressCompatibleWithTime()
    killer = GracefulKiller()
    if not endless:
        killer.kill_now = len(time_compatible_waves_id) <= 0
        print("No wave compatible")
    else:
        killer.kill_now = False
    if useReprinter:
        reprinter = Reprinter()
    else:
        reprinter = None
    max_tabulation = _getMaxColumnLen()
    while not killer.kill_now:
        # Extract commands with compatible time and not yet done
        launchableTools, waiting = findLaunchableTools()
        # Sort by command priority
        launchableTools.sort(key=lambda tup: int(tup["priority"]))
        dispatchLaunchableTools(my_monitor, launchableTools)
        printStatus(max_tabulation, waiting, reprinter)
        time.sleep(3)
    my_monitor.stop()


def printStatus(max_tabulation, waiting, reprinter=None):
    """
    Print to stdout the ongoing scan information.
    Args:
        max_tabulation: The longest column content length
        waiting: a dictionnary filled with commands that are not launched yet.
        reprinter: a reprinter object instance. If none, a normal print will be used. Default to None.
    """
    mongoInstance = MongoCalendar.getInstance()
    commandsRunning = mongoInstance.aggregate("tools", [{"$match": {"datef": "None", "dated": {
        "$ne": "None"}, "scanner_ip": {"$ne": "None"}}}, {"$group": {"_id": "$name", "count": {"$sum": 1}}}])
    total = 0
    treated = []
    buff = "Commands" + \
        _getEnoughTabulations(
            "Commands", max_tabulation)+"Running\tWaiting\n"
    buff += "--------" + \
        _getEnoughTabulations(
            "--------", max_tabulation)+"-------\t-------\n"
    for running in commandsRunning:
        try:
            w = waiting[running["_id"]]
        except KeyError:
            w = 0
        nom = str(running["_id"])
        buff += nom + \
            _getEnoughTabulations(nom, max_tabulation) + \
            str(running["count"])+"\t\t"+str(w)+"\t\t"+"\n"
        treated.append(str(running["_id"]))
        total += int(running["count"])
    for wi in list(waiting.keys()):
        if wi not in treated:
            buff += str(wi)+_getEnoughTabulations(str(wi),
                                                  max_tabulation)+str(0)+"\t\t"+str(waiting[wi])+"\t\t"+"\n"
    buff += "--------" + \
        _getEnoughTabulations(
            "--------", max_tabulation)+"-------\t-------\n"
    buff += "Total Running: "+str(total)+"\n"
    if reprinter is not None:
        reprinter.reprint(buff)
    else:
        print(buff)


def _getEnoughTabulations(name, max_tabulation):
    """
    Return enough spaces to have a proper indentation for a tool name
    Args:
        name: The tool name that will change the number of spaces needed to reach an equal level of space
        max_tabulation: The number of space for the maximum tool name length.

    Returns:
        Return a string with enough spaces to align every column.
    """
    return " "*(max_tabulation-len(name))


def _getMaxColumnLen():
    """
    Returns the maximal tool name length +2
    Returns:
        Return the maximal tool name length +2
    """
    mongoInstance = MongoCalendar.getInstance()
    commands = mongoInstance.findInDb(
        "pollenisator", "commands", {"safe": "True"})
    maxLen = 0
    for c in commands:
        if len(c["name"]) > maxLen:
            maxLen = len(c["name"])
    mustReach = maxLen+2
    return mustReach


def dispatchLaunchableTools(my_monitor, launchableTools):
    """
    Try to launch given tools within the monitor

    Args:
        my_monitor: A Monitor instance which knows what tools are already launched and online workers
        launchableTools: A list of tools within a Wave that passed the Intervals checking.
    """
    mongoInstance = MongoCalendar.getInstance()
    for launchableTool in launchableTools:
        tool = Tool.fetchObject({"_id": ObjectId(launchableTool["_id"])})
        my_monitor.launchTask(mongoInstance.calendarName, tool)





def findLaunchableTools():
    """
    Try to find tools that matches all criteria.

    Returns:
        A tuple with two values:
            * A list of launchable tools as dictionary with values _id, name and priority
            * A dictionary of waiting tools with tool's names as keys and integer as value.
    """
    toolsLaunchable = []
    waiting = {}
    time_compatible_waves_id = Wave.searchForAddressCompatibleWithTime()
    for wave_id in time_compatible_waves_id:
        commandsLaunchableWave = Wave.getNotDoneTools(wave_id)
        for tool in commandsLaunchableWave:
            toolModel = Tool.fetchObject({"_id": tool})
            try:
                waiting[str(toolModel)] += 1
            except KeyError:
                waiting[str(toolModel)] = 1
            command = toolModel.getCommand()
            if command is None:
                prio = 0
            else:
                prio = int(command.get("priority", 0))
            toolsLaunchable.append(
                {"_id": tool, "name": str(toolModel), "priority": prio})

    return toolsLaunchable, waiting


if __name__ == '__main__':
    main()
