"""Controller for interval object. Mostly handles conversion between mongo data and python objects"""

from core.Controllers.ControllerElement import ControllerElement


class IntervalController(ControllerElement):
    """Inherits ControllerElement
    Controller for interval object. Mostly handles conversion between mongo data and python objects"""

    def doUpdate(self, values):
        """
        Update the Interval represented by this model in database with the given values.

        Args:
            values: A dictionary crafted by IntervalView containg all form fields values needed.

        Returns:
            The mongo ObjectId _id of the updated interval document.
        """
        self.model.dated = values.get("Start date", self.model.dated)
        self.model.datef = values.get("End date", self.model.datef)
        self.model.update()

    def doInsert(self, values):
        """
        Insert the Interval represented by this model in the database with the given values.

        Args:
            values: A dictionary crafted by IntervalView containg all form fields values needed.

        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }
        """
        # Get form values
        dated = values["Start date"]
        datef = values["End date"]
        # Insert in database
        self.model.initialize(values["waveName"], dated, datef)
        ret, _ = self.model.addInDb()
        return ret, 0  # 0 errors

    def getData(self):
        """Return interval attributes as a dictionnary matching Mongo stored intervals
        Returns:
            dict with keys wave, dated, datef, _id, tags and infos
        """
        return {"wave": self.model.wave, "dated": self.model.dated, "datef": self.model.datef, "_id": self.model.getId(), "tags": self.model.tags, "infos": self.model.infos}

    def getType(self):
        """Return a string describing the type of object
        Returns:
            "interval" """
        return "interval"