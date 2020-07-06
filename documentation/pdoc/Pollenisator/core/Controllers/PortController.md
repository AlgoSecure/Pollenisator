Module Pollenisator.core.Controllers.PortController
===================================================
Controller for Port object. Mostly handles conversion between mongo data and python objects

Classes
-------

`PortController(model)`
:   Inherits ControllerElement
    Controller for Port object. Mostly handles conversion between mongo data and python objects
    
    Constructor
    Args:
        model: Any instance of classe that inherits core.Models.Element

    ### Ancestors (in MRO)

    * core.Controllers.ControllerElement.ControllerElement

    ### Methods

    `addAllTool(self, toolname, wavename, scope, check)`
    :   Add tool name to the model 
        Args:
            toolname: the tool name to be added to the port
            wavename: the tool wave name
            scope: the tool is launched through a scope, this is the scope string
            check: boolean to indicate if the tool must be checked against port infos (matching services or port number)

    `doInsert(self, values)`
    :   Insert the Port represented by this model in the database with the given values.
        
        Args:
            values: A dictionary crafted by PortView containg all form fields values needed.
        
        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }

    `doUpdate(self, values)`
    :   Update the Port represented by this model in database with the given values.
        
        Args:
            values: A dictionary crafted by PortView containg all form fields values needed.
        
        Returns:
            The mongo ObjectId _id of the updated Port document.

    `getData(self)`
    :   Return port attributes as a dictionnary matching Mongo stored ports
        Returns:
            dict with keys ip, port, proto, service, product, notes, _id, tags and infos

    `getDefects(self)`
    :   Return port assigned defects as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getTools(self)`
    :   Return port assigned tools as a list of mongo fetched tools dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getType(self)`
    :   Returns a string describing the type of object
        Returns:
            "port"