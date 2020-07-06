"""A plugin to parse dnsrecon scan"""

# 1. Imports
import re
import json
from core.Models.Ip import Ip
from core.plugins.plugin import Plugin


class dnsrecon(Plugin):
    def getFileOutputArg(self):
        """Returns the command line paramater giving the output file
        Returns:
            string
        """
        return " -j "

    def getFileOutputExt(self):
        """Returns the expected file extension for this command result file
        Returns:
            string
        """
        return ".json"

    def getFileOutputPath(self, commandExecuted):
        """Returns the output file path given in the executed command using getFileOutputArg
        Args:
            commandExecuted: the command that was executed with an output file inside.
        Returns:
            string: the path to file created
        """
        return commandExecuted.split(self.getFileOutputArg())[-1].strip()

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
        Example:
[       
    {
        "arguments": "./dnsrecon.py -r 10.0.0.0/24 -j /home/barre/test.json",
        "date": "2020-01-06 11:43:37.701513",
        "type": "ScanInfo"
    },
    {
        "address": "10.0.0.1",
        "name": "_gateway",
        "type": "PTR"
    },
    {
        "address": "10.0.0.77",
        "name": "barre-ThinkPad-E480",
        "type": "PTR"
    },
    {
        "address": "10.0.0.77",
        "name": "barre-ThinkPad-E480.local",
        "type": "PTR"
    }
]
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
        countInserted = 0
        try:
            dnsrecon_content = json.loads(file_opened.read())
        except json.decoder.JSONDecodeError:
            return None, None, None, None
        if len(dnsrecon_content) == 0:
            return None, None, None, None
        if not isinstance(dnsrecon_content[0], dict):
            return None, None, None, None
        if dnsrecon_content[0].get("type", "") != "ScanInfo":
            return None, None, None, None
        if dnsrecon_content[0].get("date", "") == "":
            return None, None, None, None
        for record in dnsrecon_content[1:]:
            ip = record["address"]
            name = record["name"]
            infosToAdd = {"hostname": name}
            ip_m = Ip().initialize(ip, infos=infosToAdd)
            res, iid = ip_m.addInDb()
            infosToAdd = {"ip": ip}
            ip_m = Ip().initialize(name, infos=infosToAdd)
            res, iid = ip_m.addInDb()
            # failed, domain is out of scope
            if not res:
                notes += name+" exists but already added.\n"
                ip_m = Ip.fetchObject({"_id": iid})
                infosToAdd = {"ip": list(set([ip] +
                                                    ip_m.infos.get("ip", [])))}
                ip_m.updateInfos(infosToAdd)
            else:
                countInserted += 1
                notes += name+" inserted.\n"
        return notes, tags, "wave", {"wave": None}
