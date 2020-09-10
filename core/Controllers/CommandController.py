"""Controller for command object. Mostly handles conversion between mongo data and python objects"""
from core.Controllers.ControllerElement import ControllerElement
import bson

class CommandController(ControllerElement):
    """Inherits ControllerElement
    Controller for command object. Mostly handles conversion between mongo data and python objects"""
    def doUpdate(self, values):
        """
        Update the command represented by this self.model in database with the given values.

        Args:
            values: A dictionary crafted by CommandView containg all form fields values needed.

        Returns:
            The mongo ObjectId _id of the updated command document.
        """
        # Get form values
        self.model.sleep_between = values.get(
            "Delay", self.model.sleep_between)
        self.model.max_thread = values.get("Threads", self.model.max_thread)
        self.model.text = values.get("Command line options", self.model.text)
        if values.get("Level", "network") == "port":
            self.model.ports = values.get("Ports/Services", self.model.ports)
        else:
            self.model.ports = ""
        self.model.priority = values.get("Priority", self.model.priority)
        self.model.safe = str(values.get("Safe", self.model.safe))
        self.model.timeout = str(values.get("Timeout", self.model.timeout))
        types = values.get("Types", {})
        types = [k for k, v in types.items() if v == 1]
        self.model.types = list(types)
        # Update in database
        self.model.update()

    def doInsert(self, values):
        """
        Insert the command represented by this model in the database with the given values.

        Args:
            values: A dictionary crafted by CommandView containg all form fields values needed.

        Returns:
            {
                'Command': The Command object associated
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }
        """
        # Get form values
        sleep_between = values["Delay"]
        max_thread = values["Threads"]
        text = values["Command line options"]
        if values["Level"] == "port":
            ports = values["Ports/Services"]
        else:
            ports = ""
        name = values["Name"]
        lvl = values["Level"]
        priority = values["Priority"]
        safe = str(values["Safe"])
        types = values["Types"]
        indb = values["indb"]
        timeout = values["Timeout"]
        types = [k for k, v in types.items() if v == 1]
        self.model.initialize(name, sleep_between, priority, max_thread,
                              text, lvl, ports, safe, list(types), indb, timeout)
        # Insert in database
        ret, _ = self.model.addInDb()
        if not ret:
            # command failed to be inserted, a duplicate exists
            # return None as inserted_id and 1 error
            return None, 1
        # Fetch the instance of this self.model now that it is inserted.
        return ret, 0  # 0 errors

    def getData(self):
        """Return command attributes as a dictionnary matching Mongo stored commands
        Returns:
            dict with keys name, lvl, safe, text, ports, sleep_between, max_thread, priority, types, _id, tags and infos
        """
        return {"name": self.model.name, "lvl": self.model.lvl, "safe": self.model.safe, "text": self.model.text,
                "ports": self.model.ports, "sleep_between": self.model.sleep_between, "timeout": self.model.timeout,
                "max_thread": self.model.max_thread, "priority": self.model.priority, "types": self.model.types, "indb":self.model.indb, "_id": self.model.getId(), "tags": self.model.tags, "infos": self.model.infos}

    def getType(self):
        """Return a string describing the type of object
        Returns:
            "command" """
        return "command"

    def actualize(self):
        """Ask the model to reload its data from database
        """
        if self.model is not None:
            self.model = self.model.__class__.fetchObject(
                {"_id": bson.ObjectId(self.model.getId())}, self.model.indb)