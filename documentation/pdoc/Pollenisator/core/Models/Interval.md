Module Pollenisator.core.Models.Interval
========================================
Interval Model. Useful to limit in a time frame some tools

Classes
-------

`Interval(valuesFromDb=None)`
:   Represents an interval object that defines an time interval where a wave can be executed.
    
    Attributes:
        coll_name: collection name in pollenisator database
    
    Constructor
    Args:
        valueFromDb: a dict holding values to load into the object. A mongo fetched interval is optimal.
                    possible keys with default values are : _id (None), parent (None), tags([]), infos({}),
                    wave(""), dated("None"), datef("None")

    ### Ancestors (in MRO)

    * core.Models.Element.Element

    ### Class variables

    `coll_name`
    :

    ### Methods

    `addInDb(self)`
    :   Add this interval in database.
        
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise

    `delete(self)`
    :   Delete the Interval represented by this model in database.

    `getDbKey(self)`
    :   Return a dict from model to use as unique composed key.
        Returns:
            A dict (1 key :"wave")

    `getEndingDate(self)`
    :   Returns the ending date and time of this interval
        Returns:
            a datetime object.

    `initialize(self, wave, dated='None', datef='None', infos=None)`
    :   Set values of interval
        Args:
            wave: the parent wave name
            dated: a starting date and tiem for this interval in format : '%d/%m/%Y %H:%M:%S'. or the string "None"
            datef: an ending date and tiem for this interval in format : '%d/%m/%Y %H:%M:%S'. or the string "None"
            infos: a dictionnary with key values as additional information. Default to None
        Returns:
            this object

    `setToolsInTime(self)`
    :   Get all OOT (Out of Time) tools in this wave and checks if this Interval makes them in time. 
        If it is the case, set them in time.

    `update(self, pipeline_set=None)`
    :   Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.