Module Pollenisator.core.Controllers.ScopeController
====================================================
Controller for Scope object. Mostly handles conversion between mongo data and python objects

Classes
-------

`ScopeController(model)`
:   Inherits ControllerElement
    Controller for Scope object. Mostly handles conversion between mongo data and python objects
    
    Constructor
    Args:
        model: Any instance of classe that inherits core.Models.Element

    ### Ancestors (in MRO)

    * core.Controllers.ControllerElement.ControllerElement

    ### Methods

    `doInsert(self, values)`
    :   Insert the Scope represented by this model in the database with the given values.
        
        Args:
            values: A dictionary crafted by MultipleScopeView or ScopeView containg all form fields values needed.
        
        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }

    `doUpdate(self, values)`
    :   Update the Scope represented by this model in database with the given values.
        
        Args:
            values: A dictionary crafted by ScopeView containg all form fields values needed.
        
        Returns:
            The mongo ObjectId _id of the updated Scope document.

    `getData(self)`
    :   Return scope attributes as a dictionnary matching Mongo stored scopes
        Returns:
            dict with keys wave, scope, notes, _id, tags and infos

    `getTools(self)`
    :   Return scope assigned tools as a list of mongo fetched tools dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getType(self)`
    :   Returns a string describing the type of object
        Returns:
            "scope"