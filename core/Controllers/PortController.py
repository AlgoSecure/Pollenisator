"""Controller for Port object. Mostly handles conversion between mongo data and python objects"""

from core.Controllers.ControllerElement import ControllerElement


class PortController(ControllerElement):
    """Inherits ControllerElement
    Controller for Port object. Mostly handles conversion between mongo data and python objects"""

    def doUpdate(self, values):
        """
        Update the Port represented by this model in database with the given values.

        Args:
            values: A dictionary crafted by PortView containg all form fields values needed.

        Returns:
            The mongo ObjectId _id of the updated Port document.
        """
        self.model.service = values.get("Service", self.model.service)
        self.model.product = values.get("Product", self.model.product)
        self.model.notes = values.get("Notes", self.model.notes)
        self.model.tags = values.get("Tags", self.model.tags)
        self.model.infos = values.get("Infos", self.model.infos)
        for info in self.model.infos:
            self.model.infos[info] = self.model.infos[info][0]
        self.model.update()

    def doInsert(self, values):
        """
        Insert the Port represented by this model in the database with the given values.

        Args:
            values: A dictionary crafted by PortView containg all form fields values needed.

        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }
        """
        # get form values
        port = values["Number"]
        proto = values["Proto"]
        service = values["Service"]
        product = values["Product"]
        notes = values["Product"]
        # Add the port in database
        self.model.initialize(values["ip"], port, proto, service, product, notes=notes)
        ret = self.model.addInDb()
        return ret, 0  # 0 errors

    def getData(self):
        """Return port attributes as a dictionnary matching Mongo stored ports
        Returns:
            dict with keys ip, port, proto, service, product, notes, _id, tags and infos
        """
        if self.model is None:
            return None
        return {"ip": self.model.ip, "port": self.model.port, "proto": self.model.proto,
                "service": self.model.service, "product": self.model.product, "notes": self.model.notes, "_id": self.model.getId(), "tags": self.model.tags, "infos": self.model.infos}

    def addAllTool(self, toolname, wavename, scope, check):
        """Add tool name to the model 
        Args:
            toolname: the tool name to be added to the port
            wavename: the tool wave name
            scope: the tool is launched through a scope, this is the scope string
            check: boolean to indicate if the tool must be checked against port infos (matching services or port number)
        """
        self.model.addAllTool(toolname, wavename, scope, check)

    def getDefects(self):
        """Return port assigned defects as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries
        """
        return self.model.getDefects()

    def getTools(self):
        """Return port assigned tools as a list of mongo fetched tools dict
        Returns:
            list of defect raw mongo data dictionnaries
        """
        return self.model.getTools()

    def getType(self):
        """Returns a string describing the type of object
        Returns:
            "port" """
        return "port"