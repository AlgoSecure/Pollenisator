Module Pollenisator.core.Models.Wave
====================================
Wave Model. Stores which command should be launched and associates Interval and Scope

Classes
-------

`Wave(valuesFromDb=None)`
:   Represents a Wave object. A wave is a series of tools to execute.
    
    Attributes:
        coll_name: collection name in pollenisator database
    
    Constructor
    Args:
        valueFromDb: a dict holding values to load into the object. A mongo fetched interval is optimal.
                    possible keys with default values are : _id(None), parent(None), tags([]), infos({}),
                    wave(""), wave_commands([])

    ### Ancestors (in MRO)

    * core.Models.Element.Element

    ### Class variables

    `coll_name`
    :

    ### Static methods

    `getNotDoneTools(waveName)`
    :   Returns a set of tool mongo ID that are not done yet.

    `listWaves()`
    :   Return all waves names as a list 
        Returns:
            list of all wave names

    `searchForAddressCompatibleWithTime()`
    :   Return a list of wave which have at least one interval fitting the actual time.
        
        Returns:
            A set of wave name

    ### Methods

    `addAllTool(self, command_name)`
    :   Kind of recursive operation as it will call the same function in its children ports.
        Add the appropriate tools (level check and wave's commands check) for this wave.
        Also add for all registered scopes the appropriate tools.
        Args:
            command_name: The command that we want to create all the tools for.

    `addInDb(self)`
    :   Add this wave in database.
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise

    `delete(self)`
    :   Delete the wave represented by this model in database.
        Also delete the tools, intervals, scopes associated with this wave

    `getAllTools(self)`
    :   Return all tools being part of this wave as a list of mongo fetched tools dict.
        Differs from getTools as it fetches all tools of the name and not only tools of level wave.
        Returns:
            list of defect raw mongo data dictionnaries

    `getDbKey(self)`
    :   Return a dict from model to use as unique composed key.
        Returns:
            A dict (1 key :"wave")

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

    `initialize(self, wave='', wave_commands=None, infos=None)`
    :   Set values of scope
        Args:
            wave: the wave name, default is ""
            wave_commands: a list of command name that are to be launched in this wave. Defaut is None (empty list)
            infos: a dictionnary of additional info. Default is None (empty dict)
        Returns:
            this object

    `isLaunchableNow(self)`
    :   Returns True if the tool matches criteria to be launched 
        (current time matches one of interval object assigned to this wave)
        Returns:
            bool

    `removeAllTool(self, command_name)`
    :   Remove from every member of this wave the old tool corresponding to given command name but only if the tool is not done.
        We preserve history
        
        Args:
            command_name: The command that we want to remove all the tools.

    `update(self, pipeline_set=None)`
    :   Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.