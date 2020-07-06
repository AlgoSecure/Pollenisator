"""A plugin to parse python reverse lookup scan"""

from core.plugins.plugin import Plugin
from core.Models.Ip import Ip
import re


def parse_reverse_python(result_socket):
    """
    Parse the result of a reverse lookup from python socket module
        Args:
            result_socket:  the response of the socket module for a dns reverse lookup
        Returns:
            Returns a tuple with (all value are None if not a valid python reverse lookup):
                0. the domain found by the socket module or None if no domain was found.
                1. its ip
    EXAMPLE FILE:
    pythonReverseLookup//10.0.0.1//('foe.lan', [], ['10.0.0.1'])
    """
    regex = r"pythonReverseLookup//(?:[0-9]{1,3}\.){3}[0-9]{1,3}//\('(\S+)', [^\, ]+, \['((?:[0-9]{1,3}\.){3}[0-9]{1,3})'\]\)"
    domainSearch = re.search(regex, result_socket)
    if(domainSearch != None):  # regex match
        domain = domainSearch.group(1)
        ip = domainSearch.group(2)
        return domain, ip
    return None, None


class PythonReverseLookup(Plugin):
    def getFileOutputArg(self):
        """Returns the command line paramater giving the output file
        Returns:
            string
        """
        return " > "

    def getFileOutputExt(self):
        """Returns the expected file extension for this command result file
        Returns:
            string
        """
        return ".log.txt"

    def getFileOutputPath(self, commandExecuted):
        """Returns the output file path given in the executed command using getFileOutputArg
        Args:
            commandExecuted: the command that was executed with an output file inside.
        Returns:
            string: the path to file created
        """
        return commandExecuted.split(self.getFileOutputArg())[-1].strip().split(" ")[0]

    def checkReturnCode(self, _returncode):
        return True

    def Parse(self, file_opened, **_kwargs):
        """
        Parse a opened file to extract information
        Args:
            file_opened: the open file
            _kwargs: not used
        Returns:
            a tuple with 4 values (All set to None if Parsing wrong file): 
                0. notes: notes to be inserted in tool giving direct info to pentester
                1. tags: a list of tags to be added to tool 
                2. lvl: the level of the command executed to assign to given targets
                3. targets: a list of composed keys allowing retrieve/insert from/into database targerted objects.
        """
        notes = ""
        tags = []
        targets = {}
        result_socket = file_opened.read()
        domain, ip = parse_reverse_python(result_socket)
        if domain is None:
            return None, None, None, None
        Ip().initialize(domain).addInDb()
        ip_m = Ip().initialize(ip)
        res, iid = ip_m.addInDb()
        if not res:
            ip_m = Ip.fetchObject({"_id": iid})
        hostnames = list(set(ip_m.infos.get("hostname", []) + [domain]))
        ip_m.updateInfos({"hostname": hostnames})
        targets["ip"] = {"ip": ip}
        notes += "Domain found :"+domain+"\n"
        if notes == "":
            notes = "No domain found\n"
        tags.append("hidden")
        return notes, tags, "ip", targets
