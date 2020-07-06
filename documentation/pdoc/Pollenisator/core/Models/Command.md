Module Pollenisator.core.Models.Command
=======================================
Command Model.

Classes
-------

`Command(valuesFromDb=None)`
:   Represents a command object to be run on designated scopes/ips/ports.
    
    Attributes:
        coll_name: collection name in pollenisator database
    
    Constructor
    Args:
        valueFromDb: a dict holding values to load into the object. A mongo fetched command is optimal.
                    possible keys with default values are : _id (None), parent (None), tags([]), infos({}), name(""), sleep_between("0"), priority("0),
                    max_thread("1"), text(""), lvl("network"), ports(""), safe("True"), types([])

    ### Ancestors (in MRO)

    * core.Models.Element.Element

    ### Class variables

    `coll_name`
    :

    ### Static methods

    `fetchObject(pipeline)`
    :   Fetch one command from database and return the Command object 
        Args:
            pipeline: a Mongo search pipeline (dict)
        Returns:
            Returns a Command or None if nothing matches the pipeline.

    `fetchObjects(pipeline)`
    :   Fetch many commands from database and return a Cursor to iterate over Command objects
        Args:
            pipeline: a Mongo search pipeline (dict)
        Returns:
            Returns a cursor to iterate on Command objects

    `getList(pipeline=None)`
    :   Get all command's name registered on database
        Args:
            pipeline: default to None. Condition for mongo search.
        Returns:
            Returns the list of commands name found inside the database. List may be empty.

    ### Methods

    `addInDb(self)`
    :   Add this command to pollenisator database
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise

    `delete(self)`
    :   Delete the command represented by this model in database.
        Also delete it from every group_commands.
        Also delete it from every waves's wave_commands
        Also delete every tools refering to this command.

    `getDbKey(self)`
    :   Return a dict from model to use as unique composed key.
        Returns:
            A dict (1 key :"name")

    `initialize(self, name, sleep_between='0', priority='0', max_thread='1', text='', lvl='network', ports='', safe='True', types=None, infos=None)`
    :   Set values of command
        Args:
            name: the command name
            sleep_between: delay to wait between two call to this command. Default is "0".
            priority: priority of the command ("0" is highest). Default is "0".
            max_thread: number of parallel execution possible of this command. Default is "1".
            text: the command line options. Default is "".
            lvl: level of the command. Must be either "wave", "network", "domain", "ip", "port". Default is "network"
            ports: allowed proto/port, proto/service or port-range for this command
            safe: "True" or "False" with "True" as default. Indicates if autoscan is authorized to launch this command.
            types: type for the command. Lsit of string. Default to None.
            infos: a dictionnary with key values as additional information. Default to None
        Returns:
            this object

    `update(self, pipeline_set=None)`
    :   Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.