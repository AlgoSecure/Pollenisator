Module Pollenisator.core.Controllers.CommandController
======================================================
Controller for command object. Mostly handles conversion between mongo data and python objects

Classes
-------

`CommandController(model)`
:   Inherits ControllerElement
    Controller for command object. Mostly handles conversion between mongo data and python objects
    
    Constructor
    Args:
        model: Any instance of classe that inherits core.Models.Element

    ### Ancestors (in MRO)

    * core.Controllers.ControllerElement.ControllerElement

    ### Methods

    `doInsert(self, values)`
    :   Insert the command represented by this model in the database with the given values.
        
        Args:
            values: A dictionary crafted by CommandView containg all form fields values needed.
        
        Returns:
            {
                'Command': The Command object associated
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }

    `doUpdate(self, values)`
    :   Update the command represented by this self.model in database with the given values.
        
        Args:
            values: A dictionary crafted by CommandView containg all form fields values needed.
        
        Returns:
            The mongo ObjectId _id of the updated command document.

    `getData(self)`
    :   Return command attributes as a dictionnary matching Mongo stored commands
        Returns:
            dict with keys name, lvl, safe, text, ports, sleep_between, max_thread, priority, types, _id, tags and infos

    `getType(self)`
    :   Return a string describing the type of object
        Returns:
            "command"