"""Celery worker module. Execute code and store results in database, files in the SFTP server.
"""

import errno
import os
import ssl
import sys
import time
from datetime import datetime, timedelta
import io
from bson.objectid import ObjectId
from celery import Celery
from multiprocessing import Process
from core.Components.mongo import MongoCalendar
import core.Components.Utils as Utils
from core.Models.Interval import Interval
from core.Models.Tool import Tool
from core.Models.Wave import Wave
from core.Models.Command import Command
from core.Components.Worker import Worker
# Module variables
dir_path = os.path.dirname(os.path.realpath(__file__))  # fullpath to this file
ssldir = os.path.join(dir_path, "./ssl/")  # fullepath to ssl directory
certs = {
    'keyfile': ssldir+'client.pem',
    'certfile': ssldir+'server.pem',
    'ca_certs': ssldir+'ca.pem',
    'cert_reqs': ssl.CERT_REQUIRED
}
try:
    cfg = Utils.loadCfg(os.path.join(dir_path, "./config/client.cfg"))
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


"""FIX MULTIPROCESING INSIDE CELERY TASK"""
from celery.signals import worker_process_init
from multiprocessing import current_process

@worker_process_init.connect
def fix_multiprocessing(**kwargs):
    try:
        current_process()._config
    except AttributeError:
        current_process()._config = {'semprefix': '/mp'}

def getWaveTimeLimit(waveName):
    """
    Return the latest time limit in which this tool fits. The tool should timeout after that limit

    Args:
        tool: a tool belonging to a wave to get the time limit of.

    Returns:
        Return the latest time limit in which this tool fits.
    """
    intervals = Interval.fetchObjects({"wave": waveName})
    furthestTimeLimit = datetime.now()
    for intervalModel in intervals:
        if Utils.fitNowTime(intervalModel.dated, intervalModel.datef):
            endingDate = intervalModel.getEndingDate()
            if endingDate is not None:
                if endingDate > furthestTimeLimit:
                    furthestTimeLimit = endingDate
    return furthestTimeLimit


def launchTask(calendarName, worker, launchableTool):
    launchableToolId = launchableTool.getId()
    launchableTool.markAsRunning(worker.name)
    # Mark the tool as running (scanner_ip is set and dated is set, datef is "None")
    from AutoScanWorker import executeCommand
    print("Launching command "+str(launchableTool))
    p = Process(target=executeCommand, args=(calendarName, launchableToolId))
    p.start()
    # Append to running tasks this celery result and the corresponding tool id
    return True


def dispatchLaunchableToolsv2(launchableTools, worker):
    """
    Try to launch given tools within the monitor

    Args:
        my_monitor: A Monitor instance which knows what tools are already launched and online workers
        launchableTools: A list of tools within a Wave that passed the Intervals checking.
    """
    mongoInstance = MongoCalendar.getInstance()
    for launchableTool in launchableTools:
        tool = Tool.fetchObject({"_id": ObjectId(launchableTool["_id"])})
        if worker.hasSpaceFor(tool, mongoInstance.calendarName):
            launchTask(mongoInstance.calendarName, worker, tool)

def findLaunchableToolsOnWorker(worker, calendarName):
    """ 
    Try to find tools that matches all criteria.
    Args:
        workerName: the current working worker
    Returns:
        A tuple with two values:
            * A list of launchable tools as dictionary with values _id, name and priority
            * A dictionary of waiting tools with tool's names as keys and integer as value.
    """
    mongoInstance = MongoCalendar.getInstance()
    mongoInstance.connectToDb(calendarName)
    toolsLaunchable = []
    worker_registered = mongoInstance.findInDb("pollenisator", "workers", {"name":worker.name}, False)
    commands_registered = worker_registered["registeredCommands"]
    
    waiting = {}
    time_compatible_waves_id = Wave.searchForAddressCompatibleWithTime()
    for wave_id in time_compatible_waves_id:
        commandsLaunchableWave = Wave.getNotDoneTools(wave_id)
        for tool in commandsLaunchableWave:
            
            toolModel = Tool.fetchObject({"_id": tool})
            if toolModel.name not in commands_registered:
                continue
            if worker.hasRegistered(toolModel):
                
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
                    {"_id": tool, "name": str(toolModel), "priority": prio, "errored": "error" in toolModel.status})

    return toolsLaunchable, waiting



@app.task
def getCommands(calendarName, worker_name):
    """
    CELERY remote task
    List worker registered tools in configuration folder.
    Store the results in mongo database in pollenisator.workers database.
    """
    mongoInstance = MongoCalendar.getInstance()
    mongoInstance.connectToDb(calendarName)
    tools_to_register = Utils.loadToolsConfig()
    print("Registering commands : "+str(list(tools_to_register.keys())))
    mongoInstance.registerCommands(worker_name, list(tools_to_register.keys()))
    return


@app.task
def startAutoScan(calendarName, workerName):
    mongoInstance = MongoCalendar.getInstance()
    mongoInstance.connectToDb(calendarName)
    print("Starting auto scan on "+str(calendarName))
    autoScanv2(calendarName, workerName)
    return

@app.task
def editToolConfig(command_name, remote_bin, plugin):
    tools_to_register = Utils.loadToolsConfig()
    tools_to_register[command_name] = {"bin":remote_bin, "plugin":plugin}
    Utils.saveToolsConfig(tools_to_register)

def autoScanv2(databaseName, workerName):
    """
    Search tools to launch within defined conditions and attempts to launch them this celery worker.
    Gives a visual feedback on stdout

    Args:
        databaseName: The database to search tools in
        endless: a boolean that indicates if the autoscan will be endless or if it will stop at the moment it does not found anymore launchable tools.
        useReprinter: a boolean that indicates if the array outpur will be entirely reprinted or if it will be overwritten.
    """
    mongoInstance = MongoCalendar.getInstance()
    mongoInstance.connectToDb(databaseName)
    time_compatible_waves_id = Wave.searchForAddressCompatibleWithTime()
    worker = Worker(workerName)
    while True:
        # Extract commands with compatible time and not yet done
        launchableTools, waiting = findLaunchableToolsOnWorker(worker, databaseName)
        # Sort by command priority
        launchableTools.sort(key=lambda tup: (tup["errored"], int(tup["priority"])))
        # print(str(launchableTools))
        dispatchLaunchableToolsv2(launchableTools, worker)
        
        time.sleep(3)

@app.task
def executeCommand(calendarName, toolId, parser=""):
    """
    CELERY remote task
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
    """
    # Connect to given calendar
    mongoInstance = MongoCalendar.getInstance()
    mongoInstance.connectToDb(calendarName)
    msg = ""
    # retrieve tool from tool sid
    toolModel = Tool.fetchObject({"_id": ObjectId(toolId)})
    if toolModel is None:
        raise Exception("Tool does not exist : "+str(toolId))
    command = Command.fetchObject({"name": toolModel.name}, calendarName)
    # Get time limit and output directory
    if toolModel.wave == "Custom commands":
        timeLimit = None
    else:
        timeLimit = getWaveTimeLimit(toolModel.wave)
    timeLimit = min(datetime.now()+timedelta(0, int(command.timeout)), timeLimit)
    outputRelDir = toolModel.getOutputDir(calendarName)
    abs_path = os.path.dirname(os.path.abspath(__file__))
    outputDir = os.path.join(abs_path, "./results", outputRelDir)
    # Create the output directory
    try:
        os.makedirs(outputDir)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(outputDir):
            pass
        else:
            raise exc
    # Read Tool config file
    tools_infos = Utils.loadToolsConfig()
    comm = toolModel.getCommandToExecute(outputDir)

    if parser.strip() == "":
        if toolModel.name not in list(tools_infos.keys()):
            msg = "TASK FAILED Received tool that was not registered : " + \
                str(toolModel.name)+" not in "+str(list(tools_infos.keys()))
            raise Exception(msg)
    # Fetch the command to execute
    if tools_infos.get(toolModel.name, None) is None:
        bin_path = ""
    else:
        bin_path = tools_infos[toolModel.name].get("bin")
        if bin_path is not None:
            if not bin_path.endswith(" "):
                bin_path = bin_path+" "
    comm = bin_path+comm
    if comm != "":
        try:

            # Load the plugin
            if parser.strip() == "":
                mod = Utils.loadPlugin(tools_infos[toolModel.name]["plugin"])
            elif parser.strip() == "auto-detect":
                mod = Utils.loadPluginByBin(toolModel.name.split("::")[0])
            else:
                mod = Utils.loadPlugin(parser)
            # Complete command with file output
            toolFileName = toolModel.name+"_" + \
                str(time.time())+mod.getFileOutputExt()
            comm = mod.changeCommand(comm, outputDir, toolFileName)
            print(('TASK STARTED:'+toolModel.name))
            print("Will timeout at "+str(timeLimit))
            # Execute the command with a timeout
            returncode = Utils.execute(comm, timeLimit, True)
        except Exception as e:
            raise e
        # Execute found plugin if there is one
        if mod is not None:
            filepath = mod.getFileOutputPath(comm)
            try:
                # Open generated file as utf8
                with io.open(filepath, "r", encoding="utf-8", errors='ignore') as file_opened:
                    # Check return code by plugin (can be always true if the return code is inconsistent)
                    if mod.checkReturnCode(returncode):
                        notes, tags, _, _ = mod.Parse(file_opened)
                        if notes is None:
                            notes = "No results found by plugin."
                        if tags is None:
                            tags = []
                        if isinstance(tags, str):
                            tags = [tags]
                        # Success could be change to False by the plugin function (evaluating the return code for exemple)
                        # if the success is validated, mark tool as done
                        toolModel.markAsDone(
                            os.path.join(outputRelDir, os.path.basename(filepath)))
                        # And update the tool in database
                        toolModel.notes = notes
                        toolModel.tags = tags
                        toolModel.update()
                        # Upload file to SFTP
                        mod.centralizeFile(filepath, outputDir)
                        msg = "TASK SUCCESS : "+toolModel.name
                    else:  # BAS RESULT OF PLUGIN
                        msg = "TASK FAILED (says the mod) : "+toolModel.name
                        msg += "The return code was not the expected one. ("+str(
                            returncode)+")."
                        toolModel.markAsError()
                        raise Exception(msg)
            except IOError as e:
                toolModel.tags = ["todo"]
                toolModel.notes = "Failed to read results file"
                toolModel.markAsDone()
        else:
            msg = "TASK FAILED (no plugin found) : "+toolModel.name
            toolModel.markAsNotDone()
            raise Exception(msg)
        # Delay
        if command is not None:
            if float(command.sleep_between) > 0.0:
                msg += " (will sleep for " + \
                    str(float(command.sleep_between))+")"
            print(msg)
            time.sleep(float(command.sleep_between))
        return
