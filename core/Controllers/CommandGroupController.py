"""Controller for command group object. Mostly handles conversion between mongo data and python objects"""

from core.Controllers.ControllerElement import ControllerElement


class CommandGroupController(ControllerElement):
    """Inherits ControllerElement
    Controller for command group object. Mostly handles conversion between mongo data and python objects"""

    def doUpdate(self, values):
        """
        Update the command group represented by this model in database with the given values.

        Args:
            values: A dictionary crafted by CommandGroupView containg all form fields values needed.

        Returns:
            The mongo ObjectId _id of the updated command group document.
        """
        # Get form values
        self.model.name = values.get(
            "Name", self.model.name)
        self.model.sleep_between = values.get(
            "Delay", self.model.sleep_between)
        self.model.commands = values.get("Commands", self.model.commands)
        self.model.commands = [
            k for k, v in self.model.commands.items() if v == 1]
        self.model.max_thread = values.get(
            "Shared threads", self.model.max_thread)
        # Update variable instance. (this avoid to refetch the whole command group in database)
        self.model.update()

    def doInsert(self, values):
        """
        Insert the command group represented by this model in the database with the given values.

        Args:
            values: A dictionary crafted by CommandGroupView containg all form fields values needed.

        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }
        """
        # Get form values
        name = values["Name"]
        sleep_between = values["Delay"]
        commands_dict = values["Commands"]
        commands = [k for k, v in commands_dict.items() if v == 1]
        max_thread = values["Shared threads"]
        # Insert in database
        self.model.initialize(name, sleep_between, commands, max_thread)
        ret, _ = self.model.addInDb()
        if not ret:
            # command failed to be inserted, a duplicate exists
            # return None as inserted_id and 1 error
            return None, 1
        return ret, 0  # 0 errors

    def getData(self):
        """Return command attributes as a dictionnary matching Mongo stored commands groups
        Returns:
            dict with keys name, commands,, sleep_between, max_thread, _id, tags and infos
        """
        return {"name": self.model.name, "commands": self.model.commands, "sleep_between": self.model.sleep_between, "max_thread": self.model.max_thread,
                "_id": self.model.getId(), "tags": self.model.tags, "infos": self.model.infos}

    def getType(self):
        """Return a string describing the type of object
        Returns:
            "commandgroup" """
        return "commandgroup"