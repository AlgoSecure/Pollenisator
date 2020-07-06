"""A plugin to parse python reverse searchsploit scan"""

import re
from core.Models.Ip import Ip
from core.Models.Port import Port
from core.plugins.plugin import Plugin
from pprint import pprint
import json

class SearchSploit(Plugin):
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
        return ".json"

    def getFileOutputPath(self, commandExecuted):
        """Returns the output file path given in the executed command using getFileOutputArg
        Args:
            commandExecuted: the command that was executed with an output file inside.
        Returns:
            string: the path to file created
        """
        ouputPath = str(commandExecuted.split(self.getFileOutputArg())[-1].strip().split(" ")[0])
        return ouputPath

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
        tags = []
        notes = file_opened.read()
        try:
            jsonFile = json.loads(notes)
            if jsonFile.get("RESULTS_EXPLOIT", None) is None or jsonFile.get("RESULTS_SHELLCODE", None) is None:
                return None,None,None,None
            if jsonFile.get("SEARCH", "None") == "None":
                return "No product known detected", tags, "wave", {"wave": None}
            if len(jsonFile["RESULTS_EXPLOIT"]) == 0 :
                return notes, tags,"wave", {"wave": None}
            else:     
                tags.append("Interesting")
                for exploit in jsonFile["RESULTS_EXPLOIT"]:
                    notes += exploit["Date"] + " - " + exploit["Title"] + "\n"
                    notes += "Exploitdb path : " + exploit["Path"] + "\n"
                    notes += "\n"
                return notes, tags, "wave", {"wave": None}
        except ValueError: # Couldn't parse json file
            return notes,None,None,None

