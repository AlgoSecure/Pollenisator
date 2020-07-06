Module Pollenisator.core.Models.Scope
=====================================
Scope Model

Classes
-------

`Scope(valuesFromDb=None)`
:   Represents a Scope object that defines a scope that will be targeted by network or domain tools.
    
    Attributes:
        coll_name: collection name in pollenisator database
    
    Constructor
    Args:
        valueFromDb: a dict holding values to load into the object. A mongo fetched interval is optimal.
                    possible keys with default values are : _id (None), parent (None), tags([]), infos({}),
                    wave(""), scope(""), notes("")

    ### Ancestors (in MRO)

    * core.Models.Element.Element

    ### Class variables

    `coll_name`
    :

    ### Static methods

    `checkDomainFit(waveName, domain)`
    :   Check if a found domain belongs to one of the scope of the given wave.
        
        Args:
            waveName: The wave id (name) you want to search for a validating scope
            domain: The found domain.
        
        Returns:
            boolean

    `isSubDomain(parentDomain, subDomainTest)`
    :   Returns True if this scope is a valid subdomain of the given domain
        Args:
            parentDomain: a domain that could be the parent domain of the second arg
            subDomainTest: a domain to be tested as a subdomain of first arg
        Returns:
            bool

    ### Methods

    `addAllTool(self, command_name)`
    :   Add the appropriate tools (level check and wave's commands check) for this scope.
        Args:
            command_name: The command that we want to create all the tools for.

    `addDomainInDb(self, checkDomain=True)`
    :   Add this scope domain in database.
        
        Args:
            checkDomain: boolean. If true (Default), checks that the domain IP is in scope
        
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise

    `addInDb(self)`
    :   Add this scope in database.
        
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise

    `delete(self)`
    :   Delete the Scope represented by this model in database.
        Also delete the tools associated with this scope
        Also remove this scope from ips in_scopes attributes

    `getDbKey(self)`
    :   Return a dict from model to use as unique composed key.
        Returns:
            A dict (2 keys :"wave", "scope")

    `getIpsFitting(self)`
    :   Returns a list of ip mongo dict fitting this scope
        Returns:
            A list ip IP dictionnary from mongo db

    `getTools(self)`
    :   Return port assigned tools as a list of mongo fetched defects dict
        Returns:
            list of tool raw mongo data dictionnaries

    `initialize(self, wave, scope='', notes='', infos=None)`
    :   Set values of scope
        Args:
            wave: the wave parent of this scope
            scope: a string describing the perimeter of this scope (domain, IP, NetworkIP as IP/Mask)
            notes: notes concerning this IP (opt). Default to ""
            infos: a dictionnary of additional info
        Returns:
            this object

    `isDomain(self)`
    :   Returns True if this scope is not a valid NetworkIP
        Returns:
            bool

    `update(self, pipeline_set=None)`
    :   Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.