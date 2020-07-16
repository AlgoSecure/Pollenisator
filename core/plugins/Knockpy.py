"""A plugin to parse knockpy scan"""

from core.plugins.plugin import Plugin
from core.Models.Ip import Ip
import re


def parse_knockpy_line(line):
    """
    Parse one line of knockpy result file
        Args:
            line:  one line of knockpy result file

        Returns:
            a tuple with 3 values:
                0. the ip found by knockpy on this line or None if no domain exists on this line.
                1. the domain found by knockpy on this line or None if no domain exists on this line.
                2. a boolean indicating that knockpy marked this domain as alias
    """
    regexIP_domain = r"((?:[0-9]{1,3}\.){3}[0-9]{1,3}).+(host|alias)\s+(\S+)"
    ipSearch = re.search(regexIP_domain, line)
    ip = None
    domain = None
    alias = None
    if(ipSearch is not None):  # regex match
        ip = ipSearch.group(1).strip()
        alias = ipSearch.group(2).strip() == "alias"
        domain = ipSearch.group(3).strip()
    return ip, domain, alias


class Knockpy(Plugin):
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

    def checkReturnCode(self, returncode):
        """Check if the command was executed successfully using the final exit code.
        Args:
            returncode: the exit code of the command executed.
        Returns:
            bool: True if successful returncode, False otherwise.
        """
        return returncode == 0

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
        tags = ["todo"]
        marker = "- scanning for subdomain..."
        markerFound = False
        countFound = 0
        for line in file_opened:
            if marker == line.strip():
                markerFound = True
            if not markerFound:
                continue
            ip, domain, alias = parse_knockpy_line(line)
            if ip is not None and domain is not None:
                # a domain has been found
                res, iid = Ip().initialize(domain).addInDb()
                if res:
                    Ip().initialize(ip).addInDb()
                    notes += line+"\n"
                    countFound += 1
                # failed, domain is out of scope
                else:
                    notes += domain+" exists but already added.\n"
                ip_m = Ip.fetchObject({"_id": iid})
                if alias:
                    ip_m.updateInfos({"alias": ip})
        if notes.strip() == "":
            return None, None, None, None
        return notes, tags, "wave", {"wave": None}
