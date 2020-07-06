Module Pollenisator.core.Controllers.WaveController
===================================================
Controller for Wave object. Mostly handles conversion between mongo data and python objects

Classes
-------

`WaveController(model)`
:   Inherits ControllerElement
    Controller for Wave object. Mostly handles conversion between mongo data and python objects
    
    Constructor
    Args:
        model: Any instance of classe that inherits core.Models.Element

    ### Ancestors (in MRO)

    * core.Controllers.ControllerElement.ControllerElement

    ### Methods

    `doInsert(self, values)`
    :   Insert the Wave represented by this model in the database with the given values.
        
        Args:
            values: A dictionary crafted by WaveView containing all form fields values needed.
        
        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }

    `doUpdate(self, values)`
    :   Update the Wave represented by this model in database with the given values.
        
        Args:
            values: A dictionary crafted by WaveView containg all form fields values needed.
        
        Returns:
            The mongo ObjectId _id of the updated Wave document.

    `getAllTools(self)`
    :   Return all tools being part of this wave as a list of mongo fetched tools dict.
        Differs from getTools as it fetches all tools of the name and not only tools of level wave.
        Returns:
            list of defect raw mongo data dictionnaries

    `getData(self)`
    :   Return wave attributes as a dictionnary matching Mongo stored waves
        Returns:
            dict with keys wave, wave_commands, tags and infos

    `getIntervals(self)`
    :   Return scope assigned intervals as a list of mongo fetched intervals dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getScopes(self)`
    :   Return wave assigned scopes as a list of mongo fetched scopes dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getTools(self)`
    :   Return scope assigned tools as a list of mongo fetched tools dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getType(self)`
    :   Returns a string describing the type of object
        Returns:
            "wave"

    `isLaunchableNow(self)`
    :   Returns True if the tool matches criteria to be launched 
        (current time matches one of interval object assigned to this wave)
        Returns:
            bool