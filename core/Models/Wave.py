"""Wave Model. Stores which command should be launched and associates Interval and Scope"""

from bson.objectid import ObjectId
from core.Models.Tool import Tool
from core.Models.Element import Element
from core.Models.Ip import Ip
from core.Models.Interval import Interval
import core.Components.Utils as Utils
from core.Models.Scope import Scope
from core.Components.mongo import MongoCalendar


class Wave(Element):
    """
    Represents a Wave object. A wave is a series of tools to execute.

    Attributes:
        coll_name: collection name in pollenisator database
    """
    coll_name = "waves"

    def __init__(self, valuesFromDb=None):
        """Constructor
        Args:
            valueFromDb: a dict holding values to load into the object. A mongo fetched interval is optimal.
                        possible keys with default values are : _id(None), parent(None), tags([]), infos({}),
                        wave(""), wave_commands([])
        """
        if valuesFromDb is None:
            valuesFromDb = {}
        super().__init__(valuesFromDb.get("_id", None), valuesFromDb.get("parent", None), valuesFromDb.get(
            "tags", []), valuesFromDb.get("infos", {}))
        self.initialize(valuesFromDb.get("wave", ""),
                        valuesFromDb.get("wave_commands", []), valuesFromDb.get("infos", {}))

    def initialize(self, wave="", wave_commands=None, infos=None):
        """Set values of scope
        Args:
            wave: the wave name, default is ""
            wave_commands: a list of command name that are to be launched in this wave. Defaut is None (empty list)
            infos: a dictionnary of additional info. Default is None (empty dict)
        Returns:
            this object
        """
        self.wave = wave
        self.wave_commands = wave_commands if wave_commands is not None else []
        self.infos = infos if infos is not None else {}
        return self

    def delete(self):
        """
        Delete the wave represented by this model in database.
        Also delete the tools, intervals, scopes associated with this wave
        """
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.delete("tools", {"wave": self.wave}, True)
        mongoInstance.delete("intervals", {"wave": self.wave}, True)
        mongoInstance.delete("waves", {"_id": self._id})

    def addInDb(self):
        """
        Add this wave in database.
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise 
        """
        # Check unicity
        mongoInstance = MongoCalendar.getInstance()
        existing = mongoInstance.find("waves", {"wave": self.wave}, False)
        if existing is not None:
            return False, existing["_id"]
        # Insertion
        res = mongoInstance.insert(
            "waves", {"wave": self.wave, "wave_commands": list(self.wave_commands)})
        ret = res.inserted_id
        self._id = ret
        # Add tools
        for commName in self.wave_commands:
            self.addAllTool(commName)
        return True, ret

    def update(self, pipeline_set=None):
        """Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.
        """
        mongoInstance = MongoCalendar.getInstance()
        if pipeline_set is None:
            mongoInstance.update("waves", {"_id": ObjectId(self._id)}, {
                "$set": {"wave_commands": list(self.wave_commands)}})
        else:
            mongoInstance.update("waves", {"_id": ObjectId(self._id)}, {
                "$set": pipeline_set})

    def addAllTool(self, command_name):
        """
        Kind of recursive operation as it will call the same function in its children ports.
        Add the appropriate tools (level check and wave's commands check) for this wave.
        Also add for all registered scopes the appropriate tools.
        Args:
            command_name: The command that we want to create all the tools for.
        """
        mongoInstance = MongoCalendar.getInstance()
        command = mongoInstance.findInDb(mongoInstance.calendarName, "commands", {
                                         "name": command_name}, False)
        if command["lvl"] == "wave":
            newTool = Tool()
            newTool.initialize(command_name, self.wave, "", "", "", "", "wave")
            newTool.addInDb()
            return
        scopes = mongoInstance.find("scopes", {"wave": self.wave})
        for scope in scopes:
            h = Scope(scope)
            h.addAllTool(command_name)

    def removeAllTool(self, command_name):
        """
        Remove from every member of this wave the old tool corresponding to given command name but only if the tool is not done.
        We preserve history

        Args:
            command_name: The command that we want to remove all the tools.
        """
        tools = Tool.fetchObjects({"name": command_name, "wave": self.wave})
        for tool in tools:
            if "done" not in tool.getStatus():
                tool.delete()

    def __str__(self):
        """
        Get a string representation of a wave.

        Returns:
            Returns the wave id (name).
        """
        return self.wave

    def getTools(self):
        """Return scope assigned tools as a list of mongo fetched tools dict
        Returns:
            list of defect raw mongo data dictionnaries
        """
        return Tool.fetchObjects({"wave": self.wave, "lvl": "wave"})

    def getAllTools(self):
        """Return all tools being part of this wave as a list of mongo fetched tools dict.
        Differs from getTools as it fetches all tools of the name and not only tools of level wave.
        Returns:
            list of defect raw mongo data dictionnaries
        """
        return Tool.fetchObjects({"wave": self.wave})

    def getIntervals(self):
        """Return scope assigned intervals as a list of mongo fetched intervals dict
        Returns:
            list of defect raw mongo data dictionnaries
        """
        mongoInstance = MongoCalendar.getInstance()
        return mongoInstance.find("intervals",
                                  {"wave": self.wave})

    def getScopes(self):
        """Return wave assigned scopes as a list of mongo fetched scopes dict
        Returns:
            list of defect raw mongo data dictionnaries
        """
        mongoInstance = MongoCalendar.getInstance()
        return mongoInstance.find("scopes", {"wave": self.wave})

    def getDbKey(self):
        """Return a dict from model to use as unique composed key.
        Returns:
            A dict (1 key :"wave")
        """
        return {"wave": self.wave}

    def isLaunchableNow(self):
        """Returns True if the tool matches criteria to be launched 
        (current time matches one of interval object assigned to this wave)
        Returns:
            bool
        """
        intervals = Interval.fetchObjects({"wave": self.wave})
        for intervalModel in intervals:
            if Utils.fitNowTime(intervalModel.dated, intervalModel.datef):
                return True
        return False

    @classmethod
    def searchForAddressCompatibleWithTime(cls):
        """
        Return a list of wave which have at least one interval fitting the actual time.

        Returns:
            A set of wave name
        """
        waves_to_launch = set()
        intervals = Interval.fetchObjects({})
        for intervalModel in intervals:
            if Utils.fitNowTime(intervalModel.dated, intervalModel.datef):
                waves_to_launch.add(intervalModel.wave)
        return waves_to_launch

    @classmethod
    def listWaves(cls):
        """Return all waves names as a list 
        Returns:
            list of all wave names
        """
        ret = []
        mongoInstance = MongoCalendar.getInstance()
        waves = mongoInstance.find("waves", {})
        for wave in waves:
            ret.append(wave["wave"])
        return ret

    @classmethod
    def getNotDoneTools(cls, waveName):
        """Returns a set of tool mongo ID that are not done yet.
        """
        notDoneTools = set()
        mongoInstance = MongoCalendar.getInstance()
        tools = mongoInstance.find("tools", {
                                   "wave": waveName, "ip": "", "scanner_ip": "None", "dated": "None", "datef": "None"})
        for tool in tools:
            notDoneTools.add(tool["_id"])
        scopes = Scope.fetchObjects({"wave": waveName})
        for scope in scopes:
            scopeId = scope.getId()
            ips = Ip.getIpsInScope(scopeId)
            for ip in ips:
                tools = mongoInstance.find("tools", {
                                           "wave": waveName, "ip": ip.ip, "scanner_ip": "None", "dated": "None", "datef": "None"})
                for tool in tools:
                    notDoneTools.add(tool["_id"])
        return notDoneTools
