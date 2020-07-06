Module Pollenisator.core.Models.Ip
==================================
Ip Model. Describes Hosts (not just IP now but domains too)

Classes
-------

`Ip(valuesFromDb=None)`
:   Represents an Ip object that defines an Ip or a domain that will be targeted by ip tools.
    
    Attributes:
        coll_name: collection name in pollenisator database
    
    Constructor
    Args:
        valueFromDb: a dict holding values to load into the object. A mongo fetched interval is optimal.
                    possible keys with default values are : _id (None), parent (None), tags([]), infos({}),
                    ip(""), notes(""), in_scopes(None)

    ### Ancestors (in MRO)

    * core.Models.Element.Element

    ### Class variables

    `coll_name`
    :

    ### Static methods

    `checkIpScope(scope, ip)`
    :   Check if the given ip is in the given scope
        
        Args:
            scope: A network range ip or a domain
            ip: An ipv4 like X.X.X.X
        
        Returns:
                True if the ip is in the network range or if scope == ip. False otherwise.

    `getIpsInScope(scopeId)`
    :   Returns a list of IP objects that have the given scope id in there matching scopes.
        Args:
            scopeId: a mongo ObjectId of a scope object.
        Returns:
            a mongo cursor of IP objects matching the given scopeId

    `isIp(ip)`
    :   Checks if the given string is a valid IP
        Args:
            ip: a string that could be representing an ip
        Returns:
            boolean

    `isSubDomain(parentDomain, subDomainTest)`
    :   Check if the given domain is a subdomain of another given domain
        Args:
            parentDomain: a domain that could be the parent domain of the second arg
            subDomainTest: a domain to be tested as a subdomain of first arg
        Returns:
            bool

    ### Methods

    `addAllTool(self, command_name, wave_name, scope)`
    :   Kind of recursive operation as it will call the same function in its children ports.
        Add the appropriate tools (level check and wave's commands check) for this ip.
        Also add for all registered ports the appropriate tools.
        
        Args:
            command_name: The command that we want to create all the tools for.
            wave_name: the wave name from where we want to load tools
            scope: a scope object allowing to launch this command. Opt

    `addInDb(self)`
    :   Add this IP in database.
        
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise

    `addPort(self, values)`
    :   Add a port object to database associated with this Ip.
        
        Args:
            values: A dictionary crafted by PortView containg all form fields values needed.
        
        Returns:ret
                '_id': The mongo ObjectId _idret of the inserted port document or None if insertion failed (unicity broken).

    `addScopeFitting(self, scopeId)`
    :   Add the given scopeId to the list of scopes this IP fits in.
        Args:
            scopeId: a mongo ObjectId of a Scope object.

    `delete(self)`
    :   Deletes the Ip represented by this model in database.
        Also deletes the tools associated with this ip
        Also deletes the ports associated with this ip
        Also deletes the defects associated with this ip and its ports

    `fitInScope(self, scope)`
    :   Checks if this IP is the given scope.
        Args:
            scope: a string of perimeter (Network Ip, IP or domain)
        Returns:
            boolean: True if this ip/domain is in given scope. False otherwise.

    `getDbKey(self)`
    :   Return a dict from model to use as unique composed key.
        Returns:
            A dict (1 key :"ip")

    `getDefects(self)`
    :   Returns ip assigned tools as a list of mongo fetched defects dict
        Returns:
            list of defect raw mongo data dictionnaries

    `getPorts(self)`
    :   Returns ip assigned ports as a list of mongo fetched defects dict
        Returns:
            list of port raw mongo data dictionnaries

    `getScopesFittingMe(self)`
    :   Returns a list of scope objects ids where this IP object fits.
        Returns:
            a list of scopes objects Mongo Ids where this IP/Domain is in scope.

    `getTools(self)`
    :   Return ip assigned tools as a list of mongo fetched defects dict
        Returns:
            list of tool raw mongo data dictionnaries

    `initialize(self, ip='', notes='', in_scopes=None, tags=None, infos=None)`
    :   Set values of ip
        Args:
            ip: the host (ip or domain) to represent
            notes: notes concerning this IP (opt). Default to ""
            in_scopes: a list of scopes that matches this host. If empty this IP will be OOS (Out of Scope). Default to None
            tags: a list of tags. Default to None
            infos: a dictionnary of additional info
        Returns:
            this object

    `removeScopeFitting(self, scopeId)`
    :   Remove the given scopeId from the list of scopes this IP fits in.
        Args:
            scopeId: a mongo ObjectId of a scope object.

    `update(self, pipeline_set=None)`
    :   Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.