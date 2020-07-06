Module Pollenisator.core.Controllers.CommandGroupController
===========================================================
Controller for command group object. Mostly handles conversion between mongo data and python objects

Classes
-------

`CommandGroupController(model)`
:   Inherits ControllerElement
    Controller for command group object. Mostly handles conversion between mongo data and python objects
    
    Constructor
    Args:
        model: Any instance of classe that inherits core.Models.Element

    ### Ancestors (in MRO)

    * core.Controllers.ControllerElement.ControllerElement

    ### Methods

    `doInsert(self, values)`
    :   Insert the command group represented by this model in the database with the given values.
        
        Args:
            values: A dictionary crafted by CommandGroupView containg all form fields values needed.
        
        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }

    `doUpdate(self, values)`
    :   Update the command group represented by this model in database with the given values.
        
        Args:
            values: A dictionary crafted by CommandGroupView containg all form fields values needed.
        
        Returns:
            The mongo ObjectId _id of the updated command group document.

    `getData(self)`
    :   Return command attributes as a dictionnary matching Mongo stored commands groups
        Returns:
            dict with keys name, commands,, sleep_between, max_thread, _id, tags and infos

    `getType(self)`
    :   Return a string describing the type of object
        Returns:
            "commandgroup"