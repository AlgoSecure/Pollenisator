"""Handle Workers specific work"""
from core.Models.Command import Command
from core.Models.CommandGroup import CommandGroup

from core.Components.mongo import MongoCalendar


class Worker:
    """
    Represents one worker state.
    """

    def __init__(self, name):
        """
        Constructor.
        Args:
            name: The celery worker name
        """
        self.name = name

    def getNbOfLaunchedCommand(self, commandName):
        """
        Get the total number of running commands which have the given command name

        Args:
            commandName: The command name to count running tools.

        Returns:
            Return the total of running tools with this command's name as an integer.
        """
        mongoInstance = MongoCalendar.getInstance()
        t = mongoInstance.find("tools", {"name": commandName, "scanner_ip": self.name, "dated": {
                               "$ne": "None"}, "datef": {"$eq": "None"}}).count()
        return t

    def hasRegistered(self, launchableTool):
        """
        Returns a bool indicating if the worker has registered a given tool
        Args:
            launchableTool: the tool object to check registration of.
        Returns:
            Return bool.
        """
        mongoInstance = MongoCalendar.getInstance()
        list_registered_command = mongoInstance.getRegisteredCommands(
            self.name)
        if list_registered_command is None:
            return False
        return (launchableTool.name in list_registered_command)

    def hasSpaceFor(self, launchableTool):
        """
        Check if this worker has space for the given tool. (this checks the command and every group of commands max_thred settings)

        Args:
            launchableTool: a tool documents fetched from database that has to be launched

        Returns:
            Return True if a command of the tool's type can be launched on this worker, False otherwise.
        """

        # 1. Find command with command id
        command = Command.fetchObject({"name": launchableTool.name})
        if command.safe == "False":
            return False
        # 2. Calculate individual command limit for the server
        nb = self.getNbOfLaunchedCommand(command.name) + 1
        if nb > int(command.max_thread):
            # print "Can't launch "+command["name"]+" on worker cause command max_trhad "+str(nb)+" > "+str(int(command["max_thread"]))
            return False
        # 3. Get groups of command incorporation command id
        command_groups = CommandGroup.fetchObjects(
            {"commands": {"$elemMatch": {"$eq": command.name}}})
        # 4. Calculate limites for the group
        for group in command_groups:
            tots = 0
            for commandName in group.commands:
                tots += self.getNbOfLaunchedCommand(commandName)
            if tots + 1 > int(group.max_thread):
                # print "Can't launch "+command["name"]+" on worker cause group_max_thread "+str(tots + 1)+" > "+str(int(group["max_thread"]))
                return False
        return True
