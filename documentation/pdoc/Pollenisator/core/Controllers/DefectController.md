Module Pollenisator.core.Controllers.DefectController
=====================================================
Controller for defect object. Mostly handles conversion between mongo data and python objects

Classes
-------

`DefectController(model)`
:   Inherits ControllerElement
    Controller for defect object. Mostly handles conversion between mongo data and python objects
    
    Constructor
    Args:
        model: Any instance of classe that inherits core.Models.Element

    ### Ancestors (in MRO)

    * core.Controllers.ControllerElement.ControllerElement

    ### Methods

    `addAProof(self, formValues, index)`
    :   Add a proof file to model defect.
        Args:
            formValues: the view form values as a dict. Key "Proof "+str(index) must exist
            index: the proof index in the form to insert

    `deleteProof(self, ind)`
    :   Delete a proof file given a proof index
        Args:
            ind: the proof index in the form to delete

    `doInsert(self, values)`
    :   Insert the Defect represented by this model in the database with the given values.
        
        Args:
            values: A dictionary crafted by DefectView containing all form fields values needed.
        
        Returns:
            {
                '_id': The mongo ObjectId _id of the inserted command document.
                'nbErrors': The number of objects that has not been inserted in database due to errors.
            }

    `doUpdate(self, values)`
    :   Update the Defect represented by this model in database with the given values.
        
        Args:
            values: A dictionary crafted by DefectView containg all form fields values needed.
        
        Returns:
            The mongo ObjectId _id of the updated Defect document.

    `getData(self)`
    :   Return defect attributes as a dictionnary matching Mongo stored defects
        Returns:
            dict with keys title, ease, ipact, risk, redactor, type, notes, ip, port, proto, proofs, _id, tags, infos

    `getProof(self, ind)`
    :   Returns proof file to model defect.
        Args:
            ind: the proof index in the form to get
        Returns:
            the local path of the downloaded proof (string)

    `getType(self)`
    :   Returns a string describing the type of object
        Returns:
            "defect"

    `isAssigned(self)`
    :   Checks if the defect model is assigned to an IP or is global
        Returns:    
            bool