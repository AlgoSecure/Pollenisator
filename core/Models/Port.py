"""Port Model"""

from core.Models.Element import Element
from core.Models.Tool import Tool
from core.Models.Defect import Defect
from core.Components.mongo import MongoCalendar
from bson.objectid import ObjectId


class Port(Element):
    """
    Represents an Port object that defines an Port that will be targeted by port level tools.

    Attributes:
        coll_name: collection name in pollenisator database
    """
    coll_name = "ports"

    def __init__(self, valuesFromDb=None):
        """Constructor
        Args:
            valueFromDb: a dict holding values to load into the object. A mongo fetched interval is optimal.
                        possible keys with default values are : _id (None), parent (None), tags([]), infos({}),
                        ip(""), port(""), proto("tcp"), service(""), product(""), notes("")
        """
        if valuesFromDb is None:
            valuesFromDb = {}
        super().__init__(valuesFromDb.get("_id", None), valuesFromDb.get("parent", None), valuesFromDb.get(
            "tags", []), valuesFromDb.get("infos", {}))
        self.initialize(valuesFromDb.get("ip", ""), valuesFromDb.get("port", ""),
                        valuesFromDb.get("proto", "tcp"), valuesFromDb.get(
                            "service", ""), valuesFromDb.get("product", ""),
                        valuesFromDb.get("notes", ""), valuesFromDb.get("tags", []), valuesFromDb.get("infos", {}))

    def initialize(self, ip, port="", proto="tcp", service="", product="", notes="", tags=None, infos=None):
        """Set values of port
        Args:
            ip: the parent host (ip or domain) where this port is open
            port: a port number as string. Default ""
            proto: a protocol to reach this port ("tcp" by default, send "udp" if udp port.) Default "tcp"
            service: the service running behind this port. Can be "unknown". Default ""
            notes: notes took by a pentester regarding this port. Default ""
            tags: a list of tag. Default is None (empty array)
            infos: a dictionnary of additional info. Default is None (empty dict)
        Returns:
            this object
        """
        self.ip = ip
        self.port = port
        self.proto = proto
        self.service = service
        self.product = product
        self.notes = notes
        self.infos = infos if infos is not None else {}
        self.tags = tags if tags is not None else []
        return self

    def delete(self):
        """
        Deletes the Port represented by this model in database.
        Also deletes the tools associated with this port
        Also deletes the defects associated with this port
        """
        mongoInstance = MongoCalendar.getInstance()
        tools = mongoInstance.find("tools", {"port": self.port, "proto": self.proto,
                                             "ip": self.ip}, True)
        for tool in tools:
            tool_model = Tool(tool)
            tool_model.delete()
        defects = mongoInstance.find("defects", {"port": self.port, "proto": self.proto,
                                                 "ip": self.ip}, True)
        for defect in defects:
            defect_model = Defect(defect)
            defect_model.delete()
        mongoInstance.delete("ports", {"_id":  ObjectId(self._id)})

    def update(self, pipeline_set=None):
        """Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.
        """
        oldPort = Port.fetchObject({"_id": ObjectId(self._id)})
        if oldPort is None:
            return
        oldService = oldPort.service
        mongoInstance = MongoCalendar.getInstance()
        if oldService != self.service:
            mongoInstance.delete("tools", {
                                 "lvl": "port", "ip": self.ip, "port": self.port, "proto": self.proto}, many=True)
            port_commands = mongoInstance.findInDb(
                "pollenisator", "commands", {"lvl": "port"})
            for port_command in port_commands:
                allowed_services = port_command["ports"].split(",")
                for i, elem in enumerate(allowed_services):
                    if not(elem.strip().startswith("tcp/") or elem.strip().startswith("udp/")):
                        allowed_services[i] = "tcp/"+str(elem)
                if self.proto+"/"+str(self.service) in allowed_services:
                    waves = mongoInstance.find("waves", {"wave_commands": {"$elemMatch": {
                        "$eq": port_command["name"].strip()}}})
                    for wave in waves:
                        tool_m = Tool().initialize(port_command["name"], wave["wave"], "",
                                                   self.ip, self.port, self.proto, "port")
                        tool_m.addInDb()
        # Update variable instance. (this avoid to refetch the whole command in database)
        if pipeline_set is None:
            mongoInstance.update("ports", {"_id": ObjectId(self._id)}, {
                "$set": {"service": self.service, "product":self.product, "notes": self.notes, "tags": self.tags, "infos": self.infos}})
        else:
            mongoInstance.update("ports", {"_id": ObjectId(self._id)}, {
                "$set": pipeline_set})

    def addInDb(self):
        """
        Add this Port in database.

        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise 
        """
        base = self.getDbKey()
        mongoInstance = MongoCalendar.getInstance()
        existing = mongoInstance.find("ports", base, False)
        if existing is not None:
            return False, existing["_id"]
        # Inserting port
        parent = self.getParent()
        base["parent"] = parent
        base["service"] = self.service
        base["product"] = self.product
        base["notes"] = self.notes
        base["tags"] = self.tags
        base["infos"] = self.infos
        res = mongoInstance.insert("ports", base, parent)
        ret = res.inserted_id
        self._id = ret
        # adding the appropriate tools for this port.
        # 1. fetching the wave's commands
        waves = mongoInstance.find("waves", {})
        for wave in waves:
            waveName = wave["wave"]
            commands = wave["wave_commands"]
            for commName in commands:
                # 2. finding the command only if lvl is port
                comm = mongoInstance.findInDb(mongoInstance.calendarName, "commands",
                                              {"name": commName, "lvl": "port"}, False)
                if comm is not None:
                    # 3. checking if the added port fit into the command's allowed service
                    # 3.1 first, default the selected port as tcp if no protocole is defined.
                    allowed_ports_services = comm["ports"].split(",")
                    for i, elem in enumerate(allowed_ports_services):
                        if not(elem.strip().startswith("tcp/") or elem.strip().startswith("udp/")):
                            allowed_ports_services[i] = "tcp/"+str(elem.strip())
                    for allowed in allowed_ports_services:
                        protoRange = "udp" if allowed.startswith("udp/") else "tcp"
                        maybeRange = str(allowed)[4:].split("-")
                        startAllowedRange = -1
                        endAllowedRange = -1
                        if len(maybeRange) == 2:
                            try:
                                startAllowedRange = int(maybeRange[0])
                                endAllowedRange = int(maybeRange[1])
                            except ValueError:
                                pass
                        if (self.proto+"/"+self.port == allowed) or \
                        (self.proto+"/"+self.service == allowed) or \
                        (self.proto == protoRange and int(self.port) >= int(startAllowedRange) and int(self.port) <= int(endAllowedRange)):
                            # finally add tool
                            newTool = Tool()
                            newTool.initialize(
                                comm["name"], waveName, "", self.ip, self.port, self.proto, "port")
                            newTool.addInDb()
        return True, ret

    def addAllTool(self, command_name, wave_name, scope, check=True):
        """
        Add the appropriate tools (level check and wave's commands check) for this port.

        Args:
            command_name: The command that we want to create all the tools for.
            wave_name: name of the was to fetch allowed commands from
            scope: a scope matching this tool (should only be used by network level tools)
            check: A boolean to bypass checks. Force adding this command tool to this port if False. Default is True
        """
        if check == False:
            newTool = Tool()
            newTool.initialize(command_name, wave_name, scope,
                               self.ip, self.port, self.proto, "port")
            newTool.addInDb()
            return
        # retrieve wave's command
        mongoInstance = MongoCalendar.getInstance()
        wave = mongoInstance.find(
            "waves", {"wave": wave_name}, False)
        commands = wave["wave_commands"]
        try:
            index = commands.index(command_name)
            # retrieve the command level
            command = mongoInstance.findInDb(mongoInstance.calendarName,
                                             "commands", {"name": commands[index]}, False)
            if command["lvl"] == "port":
                # 3. checking if the added port fit into the command's allowed service
                # 3.1 first, default the selected port as tcp if no protocole is defined.
                allowed_ports_services = command["ports"].split(",")
                for i, elem in enumerate(allowed_ports_services):
                    if not(elem.strip().startswith("tcp/") or elem.strip().startswith("udp/")):
                        allowed_ports_services[i] = "tcp/"+str(elem.strip())
                for allowed in allowed_ports_services:
                    protoRange = "udp" if allowed.startswith("udp/") else "tcp"
                    maybeRange = str(allowed)[4:].split("-")
                    startAllowedRange = -1
                    endAllowedRange = -1
                    if len(maybeRange) == 2:
                        try:
                            startAllowedRange = int(maybeRange[0])
                            endAllowedRange = int(maybeRange[1])
                        except ValueError:
                            pass
                    if (self.proto+"/"+self.port == allowed) or \
                       (self.proto+"/"+self.service == allowed) or \
                       (self.proto == protoRange and
                           int(self.port) >= int(startAllowedRange) and
                            int(self.port) <= int(endAllowedRange)):
                        # finally add tool
                        newTool = Tool()
                        newTool.initialize(
                            command_name, wave_name, scope, self.ip, self.port, self.proto, "port")
                        newTool.addInDb()
        except ValueError:
            pass

    def _getParent(self):
        """
        Return the mongo ObjectId _id of the first parent of this object. For a port it is the ip.

        Returns:
            Returns the parent ip's ObjectId _id".
        """
        mongoInstance = MongoCalendar.getInstance()
        return mongoInstance.find("ips", {"ip": self.ip}, False)["_id"]

    def __str__(self):
        """
        Get a string representation of a port.

        Returns:
            Returns the string protocole/port number.
        """
        return self.proto+"/"+str(self.port)

    def getDetailedString(self):
        """Returns a detailed string describing this port.
        Returns:
            string : ip:proto/port
        """
        return str(self.ip)+":"+str(self)

    def getTools(self):
        """Return port assigned tools as a list of mongo fetched defects dict
        Returns:
            list of tool raw mongo data dictionnaries
        """
        mongoInstance = MongoCalendar.getInstance()
        return mongoInstance.find("tools", {"lvl": "port", "ip": self.ip, "port": self.port, "proto": self.proto})

    def getDefects(self):
        """Return port assigned defects as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries
        """
        mongoInstance = MongoCalendar.getInstance()
        return mongoInstance.find("defects", {"ip": self.ip, "port": self.port, "proto": self.proto})

    def getDbKey(self):
        """Return a dict from model to use as unique composed key.
        Returns:
            A dict (3 keys :"ip", "port", "proto")
        """
        return {"ip": self.ip, "port": self.port, "proto": self.proto}
