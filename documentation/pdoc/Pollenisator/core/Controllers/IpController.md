Module Pollenisator.core.Controllers.IpController
=================================================
Controller for IP object. Mostly handles conversion between mongo data and python objects

Classes
-------

`IpController(model)`
:   Inherits ControllerElement
    Controller for IP object. Mostly handles conversion between mongo data and python objects
    
    Constructor
    Args:
        model: Any instance of classe that inherits core.Models.Element

    ### Ancestors (in MRO)

    * core.Controllers.ControllerElement.ControllerElement

    ### Methods

    `doInsert(self, values)`
    :   Insert the Ip represented by this model in the database with the given values.
        
        Args:
            values: A dictionary crafted by MultipleIpView or IpView containg all form fields values needed.
        
        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }

    `doUpdate(self, values)`
    :   Update the Ip represented by this model in database with the given values.
        
        Args:
            values: A dictionary crafted by IpView containg all form fields values needed.
        
        Returns:
            The mongo ObjectId _id of the updated Ip document.

    `getData(self)`
    :   Returns ip attributes as a dictionnary matching Mongo stored ips
        Returns:
            dict with keys ip, in_scopes, notes, _id, tags and infos

    `getDefects(self)`
    :   Return ip assigned defects as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getPorts(self)`
    :   Return ip assigned ports as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getTools(self)`
    :   Return ip assigned tools as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getType(self)`
    :   Return a string describing the type of object
        Returns:
            "ip"