Module Pollenisator.core.Models.CommandGroup
============================================
Command Group Model.

Classes
-------

`CommandGroup(valuesFromDb=None)`
:   Represents a command group object that defines settings and ressources shared by many Commands.
    
    Attributes:
        coll_name: collection name in pollenisator database
    
    Constructor
    Args:
        valueFromDb: a dict holding values to load into the object. A mongo fetched command group is optimal.
                    possible keys with default values are : _id (None), parent (None), tags([]), infos({}),
                    name(""), sleep_between("0"), commands([]),
                    max_thread("1")

    ### Ancestors (in MRO)

    * core.Models.Element.Element

    ### Class variables

    `coll_name`
    :

    ### Static methods

    `fetchObject(pipeline)`
    :   Fetch one command from database and return the CommandGroup object 
        Args:
            pipeline: a Mongo search pipeline (dict)
        Returns:
            Returns a CommandGroup or None if nothing matches the pipeline.

    `fetchObjects(pipeline)`
    :   Fetch many commands from database and return a Cursor to iterate over CommandGroup objects
        Args:
            pipeline: a Mongo search pipeline (dict)
        Returns:
            Returns a cursor to iterate on CommandGroup objects

    `getList()`
    :   Get all group of command's name registered on database
        
        Returns:
            Returns the list of command groups name found inside the database. List may be empty.

    ### Methods

    `addInDb(self)`
    :   Add a new command group to pollenisator database.
        
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise

    `delete(self)`
    :   Delete the command group represented by this model in database.

    `getDbKey(self)`
    :   Return a dict from model to use as unique composed key.
        Returns:
            A dict (1 key: "_id")

    `initialize(self, name, sleep_between='0', commands=None, max_thread='1', infos=None)`
    :   Set values of command group
        Args:
            name: the command group name
            sleep_between: delay to wait between two call to this command. Default is "0".
            commands: list of command names that are part of this group. Default is None and stores an empty array
            max_thread: number of parallel execution possible of this command. Default is "1".
            infos: a dictionnary with key values as additional information. Default to None
        Returns:
            this object

    `update(self, pipeline_set=None)`
    :   Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.