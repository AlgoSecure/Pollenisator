"""Controller for IP object. Mostly handles conversion between mongo data and python objects"""

from core.Controllers.ControllerElement import ControllerElement
from core.Models.Ip import Ip


class IpController(ControllerElement):
    """Inherits ControllerElement
    Controller for IP object. Mostly handles conversion between mongo data and python objects"""

    def doUpdate(self, values):
        """
        Update the Ip represented by this model in database with the given values.

        Args:
            values: A dictionary crafted by IpView containg all form fields values needed.

        Returns:
            The mongo ObjectId _id of the updated Ip document.
        """
        self.model.notes = values.get("Notes", self.model.notes)
        self.model.tags = values.get("Tags", self.model.tags)
        self.model.infos = values.get("Infos", self.model.infos)
        for info in self.model.infos:
            self.model.infos[info] = self.model.infos[info][0]
        self.model.update()

    def doInsert(self, values):
        """
        Insert the Ip represented by this model in the database with the given values.

        Args:
            values: A dictionary crafted by MultipleIpView or IpView containg all form fields values needed.

        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }
        """
        # Only multi insert exists at the moment for IP
        try:
            multi = True
        except KeyError:
            multi = False

        if multi:
            # Get form values
            ret = []
            total = 0
            accepted = 0
            for line in values["IPs"].split("\n"):
                if line != "":
                    # Insert in database
                    model = Ip().initialize(line)
                    inserted, iid = model.addInDb()
                    if inserted:
                        ret.append(iid)
                        accepted += 1
                    total += 1
            return ret, total-accepted  # nb errors = total - accepted

    def getData(self):
        """Returns ip attributes as a dictionnary matching Mongo stored ips
        Returns:
            dict with keys ip, in_scopes, notes, _id, tags and infos
        """
        return {"ip": self.model.ip, "in_scopes": self.model.in_scopes, "notes": self.model.notes, "_id": self.model.getId(), "tags": self.model.tags, "infos": self.model.infos}

    def getDefects(self):
        """Return ip assigned defects as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries
        """
        return self.model.getDefects()

    def getTools(self):
        """Return ip assigned tools as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries
        """
        return self.model.getTools()

    def getPorts(self):
        """Return ip assigned ports as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries
        """
        return self.model.getPorts()

    def getType(self):
        """Return a string describing the type of object
        Returns:
            "ip" """
        return "ip"