"""Scope Model"""

from core.Models.Element import Element
from core.Models.Ip import Ip
from bson.objectid import ObjectId
from core.Components.mongo import MongoCalendar
from core.Models.Tool import Tool
import core.Components.Utils as Utils
from core.Components.Settings import Settings


class Scope(Element):
    """
    Represents a Scope object that defines a scope that will be targeted by network or domain tools.

    Attributes:
        coll_name: collection name in pollenisator database
    """

    coll_name = "scopes"

    def __init__(self, valuesFromDb=None):
        """Constructor
        Args:
            valueFromDb: a dict holding values to load into the object. A mongo fetched interval is optimal.
                        possible keys with default values are : _id (None), parent (None), tags([]), infos({}),
                        wave(""), scope(""), notes("")
        """
        if valuesFromDb is None:
            valuesFromDb = {}
        super().__init__(valuesFromDb.get("_id", None), valuesFromDb.get("parent", None), valuesFromDb.get(
            "tags", []), valuesFromDb.get("infos", {}))
        self.initialize(valuesFromDb.get("wave", ""), valuesFromDb.get("scope", ""),
                        valuesFromDb.get("notes", ""), valuesFromDb.get("infos", {}))

    def initialize(self, wave, scope="", notes="", infos=None):
        """Set values of scope
        Args:
            wave: the wave parent of this scope
            scope: a string describing the perimeter of this scope (domain, IP, NetworkIP as IP/Mask)
            notes: notes concerning this IP (opt). Default to ""
            infos: a dictionnary of additional info
        Returns:
            this object
        """
        self.wave = wave
        self.scope = scope
        self.notes = notes
        self.infos = infos if infos is not None else {}
        return self

    def update(self, pipeline_set=None):
        """Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.
        """
        mongoInstance = MongoCalendar.getInstance()
        if pipeline_set is None:
            mongoInstance.update("scopes", {"_id": ObjectId(self._id)}, {
                "$set": {"notes": self.notes, "tags": self.tags}})
        else:
            mongoInstance.update("scopes", {"_id": ObjectId(self._id)}, {
                "$set": pipeline_set})

    def delete(self):
        """
        Delete the Scope represented by this model in database.
        Also delete the tools associated with this scope
        Also remove this scope from ips in_scopes attributes
        """
        # deleting tool with scope lvl
        tools = Tool.fetchObjects({"scope": self.scope, "wave": self.wave, "$or": [
                                  {"lvl": "network"}, {"lvl": "domain"}]})
        for tool in tools:
            tool.delete()
        # Deleting this scope against every ips
        ips = Ip.getIpsInScope(self._id)
        for ip in ips:
            ip.removeScopeFitting(self._id)
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.delete("scopes", {"_id": self._id})
        parent_wave = mongoInstance.find("waves", {"wave": self.wave}, False)
        if parent_wave is None:
            return
        mongoInstance.notify(mongoInstance.calendarName,
                             "waves", parent_wave["_id"], "update", "")
        # Finally delete the selected element

    def addInDb(self):
        """
        Add this scope in database.

        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise 
        """
        base = self.getDbKey()
        # Checking unicity
        mongoInstance = MongoCalendar.getInstance()
        existing = mongoInstance.find("scopes", base, False)
        if existing is not None:
            return False, existing["_id"]
        # Inserting scope
        parent = self.getParent()
        res_insert = mongoInstance.insert("scopes", base, parent)
        ret = res_insert.inserted_id
        self._id = ret
        # adding the appropriate tools for this scope.
        wave = mongoInstance.find("waves", {"wave": self.wave}, False)
        commands = wave["wave_commands"]
        for commName in commands:
            if commName.strip() != "":
                self.addAllTool(commName)
        # Testing this scope against every ips
        ips = Ip.fetchObjects({})
        for ip in ips:
            if self._id not in ip.in_scopes:
                if ip.fitInScope(self.scope):
                    ip.addScopeFitting(self.getId())
        return True, ret

    def addDomainInDb(self, checkDomain=True):
        """
        Add this scope domain in database.

        Args:
            checkDomain: boolean. If true (Default), checks that the domain IP is in scope

        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise 
        """
        # Checking unicity
        base = self.getDbKey()
        mongoInstance = MongoCalendar.getInstance()
        existing = mongoInstance.find("scopes", base, False)
        if existing is not None:
            return 0, None
        # Check if domain's ip fit in one of the Scope of the wave
        if checkDomain:
            if not Scope.checkDomainFit(self.wave, self.scope):
                return -1, None
        # insert the domains in the scopes
        parent = self.getParent()
        res_insert = mongoInstance.insert("scopes", base, parent)
        ret = res_insert.inserted_id
        self._id = ret
        # Adding appropriate tools for this scopes
        wave = mongoInstance.find("waves", {"wave": self.wave}, False)
        commands = wave["wave_commands"]
        for commName in commands:
            comm = mongoInstance.findInDb("pollenisator",
                                          "commands", {"name": commName, "lvl": "network"}, False)
            if comm is not None:
                newTool = Tool()
                newTool.initialize(
                    comm["name"], self.wave, self.scope, "", "", "", "network")
                newTool.addInDb()
            else:
                comm = mongoInstance.findInDb("pollenisator",
                                              "commands", {"name": commName, "lvl": "domain"}, False)
                if comm is not None:
                    newTool = Tool()
                    newTool.initialize(
                        comm["name"], self.wave, self.scope, "", "", "", "domain")
                    newTool.addInDb()
        # Testing this scope against every ips
        ips = Ip.fetchObjects({})
        for ip in ips:
            if self._id not in ip.in_scopes:
                if ip.fitInScope(self.scope):
                    ip.addScopeFitting(self.getId())
        ipToInsert = Ip()
        ipToInsert.initialize(self.scope)
        ipToInsert.addInDb()
        return 1, ret

    @classmethod
    def checkDomainFit(cls, waveName, domain):
        """
        Check if a found domain belongs to one of the scope of the given wave.

        Args:
            waveName: The wave id (name) you want to search for a validating scope
            domain: The found domain.

        Returns:
            boolean
        """
        # Checking settings for domain check.
        settings = Settings()
        # get the domain ip so we can search for it in ipv4 range scopes.
        domainIp = Utils.performLookUp(domain)
        mongoInstance = MongoCalendar.getInstance()
        scopesOfWave = mongoInstance.find("scopes", {"wave": waveName})
        for scopeOfWave in scopesOfWave:
            scopeIsANetworkIp = Utils.isNetworkIp(scopeOfWave["scope"])
            if scopeIsANetworkIp:
                if settings.db_settings.get("include_domains_with_ip_in_scope", False):
                    if Ip.checkIpScope(scopeOfWave["scope"], domainIp):
                        return True
            else:  # If scope is domain
                # check if we include subdomains
                if settings.db_settings.get("include_all_domains", False):
                    return True
                else:
                    splitted_domain = domain.split(".")
                    # Assuring to check only if there is a domain before the tld (.com, .fr ... )
                    topDomainExists = len(splitted_domain) > 2
                    if topDomainExists:
                        if settings.db_settings.get("include_domains_with_topdomain_in_scope", False):
                            if splitted_domain[1:] == scopeOfWave["scope"].split("."):
                                return True
                    if settings.db_settings.get("include_domains_with_ip_in_scope", False):
                        inRangeDomainIp = Utils.performLookUp(
                            scopeOfWave["scope"])
                        if str(inRangeDomainIp) == str(domainIp):
                            return True
        return False

    def addAllTool(self, command_name):
        """
        Add the appropriate tools (level check and wave's commands check) for this scope.
        Args:
            command_name: The command that we want to create all the tools for.
        """
        mongoInstance = MongoCalendar.getInstance()
        command = mongoInstance.findInDb("pollenisator", "commands", {
                                         "name": command_name}, False)
        if command["lvl"] == "network":
            newTool = Tool()
            newTool.initialize(
                command["name"], self.wave, self.scope, "", "", "", "network")
            newTool.addInDb()
            return
        if command["lvl"] == "domain":
            if not Utils.isNetworkIp(self.scope):
                newTool = Tool()
                newTool.initialize(
                    command["name"], self.wave, self.scope, "", "", "", "domain")
                newTool.addInDb()
            return
        ips = self.getIpsFitting()
        for ip in ips:
            i = Ip(ip)
            i.addAllTool(command_name, self.wave, self.scope)

    def _getParent(self):
        """
        Return the mongo ObjectId _id of the first parent of this object. For a scope it is the wave.

        Returns:
            Returns the parent wave's ObjectId _id".
        """
        mongoInstance = MongoCalendar.getInstance()
        return mongoInstance.find("waves", {"wave": self.wave}, False)["_id"]

    def __str__(self):
        """
        Get a string representation of a scope.

        Returns:
            Returns the scope string (network ipv4 range or domain).
        """
        return self.scope

    def getTools(self):
        """Return port assigned tools as a list of mongo fetched defects dict
        Returns:
            list of tool raw mongo data dictionnaries
        """
        mongoInstance = MongoCalendar.getInstance()
        return mongoInstance.find("tools", {"wave": self.wave, "$or": [{"lvl": "network"}, {"lvl": "domain"}], "scope": self.scope})

    def getDbKey(self):
        """Return a dict from model to use as unique composed key.
        Returns:
            A dict (2 keys :"wave", "scope")
        """
        return {"wave": self.wave, "scope": self.scope}

    def getIpsFitting(self):
        """Returns a list of ip mongo dict fitting this scope
        Returns:
            A list ip IP dictionnary from mongo db
        """
        mongoInstance = MongoCalendar.getInstance()
        ips = mongoInstance.find("ips", )
        ips_fitting = []
        isdomain = self.isDomain()
        for ip in ips:
            if isdomain:
                my_ip = Utils.performLookUp(self.scope)
                my_domain = self.scope
                ip_isdomain = not Utils.isIp(ip["ip"])
                if ip_isdomain:
                    if my_domain == ip["ip"]:
                        ips_fitting.append(ip)
                    if Scope.isSubDomain(my_domain, ip["ip"]):
                        ips_fitting.append(ip)
                else:
                    if my_ip == ip["ip"]:
                        ips_fitting.append(ip)
            else:
                if Ip.checkIpScope(self.scope, ip["ip"]):
                    ips_fitting.append(ip)
        return ips_fitting

    def isDomain(self):
        """Returns True if this scope is not a valid NetworkIP
        Returns:
            bool
        """
        return not Utils.isNetworkIp(self.scope)

    @classmethod
    def isSubDomain(cls, parentDomain, subDomainTest):
        """Returns True if this scope is a valid subdomain of the given domain
        Args:
            parentDomain: a domain that could be the parent domain of the second arg
            subDomainTest: a domain to be tested as a subdomain of first arg
        Returns:
            bool
        """
        splitted_domain = subDomainTest.split(".")
        # Assuring to check only if there is a domain before the tld (.com, .fr ... )
        topDomainExists = len(splitted_domain) > 2
        if topDomainExists:
            if ".".join(splitted_domain[1:]) == parentDomain:
                return True
        return False
