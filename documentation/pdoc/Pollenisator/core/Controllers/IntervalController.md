Module Pollenisator.core.Controllers.IntervalController
=======================================================
Controller for interval object. Mostly handles conversion between mongo data and python objects

Classes
-------

`IntervalController(model)`
:   Inherits ControllerElement
    Controller for interval object. Mostly handles conversion between mongo data and python objects
    
    Constructor
    Args:
        model: Any instance of classe that inherits core.Models.Element

    ### Ancestors (in MRO)

    * core.Controllers.ControllerElement.ControllerElement

    ### Methods

    `doInsert(self, values)`
    :   Insert the Interval represented by this model in the database with the given values.
        
        Args:
            values: A dictionary crafted by IntervalView containg all form fields values needed.
        
        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }

    `doUpdate(self, values)`
    :   Update the Interval represented by this model in database with the given values.
        
        Args:
            values: A dictionary crafted by IntervalView containg all form fields values needed.
        
        Returns:
            The mongo ObjectId _id of the updated interval document.

    `getData(self)`
    :   Return interval attributes as a dictionnary matching Mongo stored intervals
        Returns:
            dict with keys wave, dated, datef, _id, tags and infos

    `getType(self)`
    :   Return a string describing the type of object
        Returns:
            "interval"