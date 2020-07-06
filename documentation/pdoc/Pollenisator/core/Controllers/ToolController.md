Module Pollenisator.core.Controllers.ToolController
===================================================
Controller for Tool object. Mostly handles conversion between mongo data and python objects

Classes
-------

`ToolController(model)`
:   Inherits ControllerElement
    Controller for Tool object. Mostly handles conversion between mongo data and python objects
    
    Constructor
    Args:
        model: Any instance of classe that inherits core.Models.Element

    ### Ancestors (in MRO)

    * core.Controllers.ControllerElement.ControllerElement

    ### Methods

    `doUpdate(self, values)`
    :   Update the Tool represented by this model in database with the given values.
        
        Args:
            values: A dictionary crafted by ToolView containg all form fields values needed.
        
        Returns:
            The mongo ObjectId _id of the updated Tool document.

    `getData(self)`
    :   Return scope attributes as a dictionnary matching Mongo stored scopes
        Returns:
            dict with keys name, wave, scope, ip, port, proto, lvl, text, dated, datef, scanner_ip, notes, status, _id, tags and infos

    `getName(self)`
    :   Returns the model tool name
        Returns: 
            string

    `getOutputDir(self, calendarName)`
    :   Returns directory of the tool file output 
        Args:
            calendarName: the pentest database name
        Returns:
            string (path)

    `getResultFile(self)`
    :   Returns path of the tool resulting file output
        Returns:
            string (path)

    `getStatus(self)`
    :   Returns a string describing the tool current status
        Returns:
            string with possible values : "OOS"/"OOT"/"running"/"done". OOS = Out of Scope, OOT = Out of Time range

    `getType(self)`
    :   Returns a string describing the type of object
        Returns:
            "tool"

    `markAsNotDone(self)`
    :   Change this model tool to status not done. (resets dates and scanner)

    `setStatus(self, status)`
    :   Set the tool model status
        Args:
            status: string with possible values : "OOS"/"OOT"/"running"/"done". OOS = Out of Scope, OOT = Out of Time range