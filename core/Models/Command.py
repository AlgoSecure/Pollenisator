"""Command Model."""
from core.Models.Element import Element
from core.Components.mongo import MongoCalendar
from bson.objectid import ObjectId


class Command(Element):
    """Represents a command object to be run on designated scopes/ips/ports.

    Attributes:
        coll_name: collection name in pollenisator or pentest database
    """

    coll_name = "commands"

    def __init__(self, valuesFromDb=None):
        """Constructor
        Args:
            valueFromDb: a dict holding values to load into the object. A mongo fetched command is optimal.
                        possible keys with default values are : _id (None), parent (None), tags([]), infos({}), name(""), sleep_between("0"), priority("0),
                        max_thread("1"), text(""), lvl("network"), ports(""), safe("True"), types([]), indb="pollenisator", timeout="300"
        """
        if valuesFromDb is None:
            valuesFromDb = dict()
        super().__init__(valuesFromDb.get("_id", None), valuesFromDb.get("parent", None),  valuesFromDb.get(
            "tags", []), valuesFromDb.get("infos", {}))
        self.initialize(valuesFromDb.get("name", ""), valuesFromDb.get("sleep_between", "0"),
                        valuesFromDb.get("priority", "0"), valuesFromDb.get(
                            "max_thread", "1"),
                        valuesFromDb.get("text", ""), valuesFromDb.get(
                            "lvl", "network"),
                        valuesFromDb.get("ports", ""),
                        valuesFromDb.get("safe", "True"), valuesFromDb.get("types", []), valuesFromDb.get("indb", "pollenisator"), valuesFromDb.get("timeout", "300"), valuesFromDb.get("infos", {}))

    def initialize(self, name, sleep_between="0", priority="0", max_thread="1", text="", lvl="network", ports="", safe="True", types=None, indb=False, timeout="300", infos=None):
        """Set values of command
        Args:
            name: the command name
            sleep_between: delay to wait between two call to this command. Default is "0".
            priority: priority of the command ("0" is highest). Default is "0".
            max_thread: number of parallel execution possible of this command. Default is "1".
            text: the command line options. Default is "".
            lvl: level of the command. Must be either "wave", "network", "domain", "ip", "port". Default is "network"
            ports: allowed proto/port, proto/service or port-range for this command
            safe: "True" or "False" with "True" as default. Indicates if autoscan is authorized to launch this command.
            types: type for the command. Lsit of string. Default to None.
            indb: db name : global (pollenisator database) or  local pentest database
            timeout: a timeout to kill stuck tools and retry them later
            infos: a dictionnary with key values as additional information. Default to None
        Returns:
            this object
        """
        self.name = name
        self.sleep_between = sleep_between
        self.priority = priority
        self.max_thread = max_thread
        self.text = text
        self.lvl = lvl
        self.ports = ports
        self.safe = safe
        self.infos = infos if infos is not None else {}
        self.indb = indb
        self.timeout = timeout
        self.types = types if types is not None else []
        return self

    def delete(self):
        """
        Delete the command represented by this model in database.
        Also delete it from every group_commands.
        Also delete it from every waves's wave_commands
        Also delete every tools refering to this command.
        """
        ret = self._id
        mongoInstance = MongoCalendar.getInstance()
        # Remove from all group of commands this command name if they have it.
        mongoInstance.updateInDb(self.indb, "group_commands", {}, {
            "$pull": {"commands": self.name}}, True, True)
        # Remove from all waves this command.
        if self.indb == "pollenisator":
            calendars = mongoInstance.listCalendars()
        else:
            calendars = [self.indb]
        for calendar in calendars:
            waves = mongoInstance.findInDb(calendar, "waves")
            for wave in waves:
                toBeUpdated = wave["wave_commands"]
                if self.name in wave["wave_commands"]:
                    toBeUpdated.remove(self.name)
                    mongoInstance.updateInDb(calendar, "waves", {"_id": wave["_id"]}, {
                        "$set": {"wave_commands": toBeUpdated}}, False)
            # Remove all tools refering to this command's name.
            mongoInstance.deleteFromDb(calendar,
                                    "tools", {"name": self.name}, True, True)
        mongoInstance.deleteFromDb(self.indb, "commands", {
                                   "_id": ret}, False, True)

    def addInDb(self):
        """Add this command to pollenisator database
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise 
        """
        mongoInstance = MongoCalendar.getInstance()
        existing = mongoInstance.findInDb(
            self.indb, "commands", {"name": self.name}, False)
        if existing is not None:
            return False, existing["_id"]
        ins_result = mongoInstance.insertInDb(self.indb, "commands", {"name": self.name, "lvl": self.lvl, "priority": self.priority,
                                                                           "sleep_between": self.sleep_between, "max_thread": self.max_thread, "text": self.text,
                                                                           "ports": self.ports, "safe": self.safe, "types": self.types, "indb": self.indb, "timeout": self.timeout}, '', True)
        self._id = ins_result.inserted_id
        return True, self._id

    def update(self, pipeline_set=None):
        """Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.
        """
        mongoInstance = MongoCalendar.getInstance()
        if pipeline_set is None:
            mongoInstance.updateInDb(self.indb, "commands", {"_id": ObjectId(self._id)}, {
                "$set": {"priority": self.priority, "sleep_between": self.sleep_between, "max_thread": self.max_thread, "timeout": self.timeout,
                         "text": self.text, "ports": self.ports, "safe": self.safe, "types": self.types}}, False, True)
        else:
            mongoInstance.updateInDb(self.indb, "commands", {"_id": ObjectId(self._id)}, {
                "$set": pipeline_set}, False, True)

    @classmethod
    def getList(cls, pipeline=None, targetdb="pollenisator"):
        """
        Get all command's name registered on database
        Args:
            pipeline: default to None. Condition for mongo search.
        Returns:
            Returns the list of commands name found inside the database. List may be empty.
        """
        if pipeline is None:
            pipeline = {}
        return [command.name for command in Command.fetchObjects(pipeline, targetdb)]

    @classmethod
    def fetchObject(cls, pipeline, targetdb="pollenisator"):
        """Fetch one command from database and return the Command object 
        Args:
            pipeline: a Mongo search pipeline (dict)
        Returns:
            Returns a Command or None if nothing matches the pipeline.
        """
        mongoInstance = MongoCalendar.getInstance()
        d = mongoInstance.findInDb(targetdb, "commands", pipeline, False)
        if d is None:
            return None
        return Command(d)

    @classmethod
    def fetchObjects(cls, pipeline, targetdb="pollenisator"):
        """Fetch many commands from database and return a Cursor to iterate over Command objects
        Args:
            pipeline: a Mongo search pipeline (dict)
        Returns:
            Returns a cursor to iterate on Command objects
        """
        mongoInstance = MongoCalendar.getInstance()
        ds = mongoInstance.findInDb(targetdb, "commands", pipeline, True)
        for d in ds:
            yield Command(d)

    def __str__(self):
        """
        Get a string representation of a command.

        Returns:
            Returns the command's name string.
        """
        return self.name

    def getDbKey(self):
        """Return a dict from model to use as unique composed key.
        Returns:
            A dict (1 key :"name")
        """
        return {"name": self.name}
