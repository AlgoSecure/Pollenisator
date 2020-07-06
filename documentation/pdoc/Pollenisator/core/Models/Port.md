Module Pollenisator.core.Models.Port
====================================
Port Model

Classes
-------

`Port(valuesFromDb=None)`
:   Represents an Port object that defines an Port that will be targeted by port level tools.
    
    Attributes:
        coll_name: collection name in pollenisator database
    
    Constructor
    Args:
        valueFromDb: a dict holding values to load into the object. A mongo fetched interval is optimal.
                    possible keys with default values are : _id (None), parent (None), tags([]), infos({}),
                    ip(""), port(""), proto("tcp"), service(""), product(""), notes("")

    ### Ancestors (in MRO)

    * core.Models.Element.Element

    ### Class variables

    `coll_name`
    :

    ### Methods

    `addAllTool(self, command_name, wave_name, scope, check=True)`
    :   Add the appropriate tools (level check and wave's commands check) for this port.
        
        Args:
            command_name: The command that we want to create all the tools for.
            wave_name: name of the was to fetch allowed commands from
            scope: a scope matching this tool (should only be used by network level tools)
            check: A boolean to bypass checks. Force adding this command tool to this port if False. Default is True

    `addInDb(self)`
    :   Add this Port in database.
        
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise

    `delete(self)`
    :   Deletes the Port represented by this model in database.
        Also deletes the tools associated with this port
        Also deletes the defects associated with this port

    `getDbKey(self)`
    :   Return a dict from model to use as unique composed key.
        Returns:
            A dict (3 keys :"ip", "port", "proto")

    `getDefects(self)`
    :   Return port assigned defects as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getDetailedString(self)`
    :   Returns a detailed string describing this port.
        Returns:
            string : ip:proto/port

    `getTools(self)`
    :   Return port assigned tools as a list of mongo fetched defects dict
        Returns:
            list of tool raw mongo data dictionnaries

    `initialize(self, ip, port='', proto='tcp', service='', product='', notes='', tags=None, infos=None)`
    :   Set values of port
        Args:
            ip: the parent host (ip or domain) where this port is open
            port: a port number as string. Default ""
            proto: a protocol to reach this port ("tcp" by default, send "udp" if udp port.) Default "tcp"
            service: the service running behind this port. Can be "unknown". Default ""
            notes: notes took by a pentester regarding this port. Default ""
            tags: a list of tag. Default is None (empty array)
            infos: a dictionnary of additional info. Default is None (empty dict)
        Returns:
            this object

    `update(self, pipeline_set=None)`
    :   Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.