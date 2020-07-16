"""A plugin to parse sublist3r"""

from core.plugins.plugin import Plugin
from core.Models.Ip import Ip
import re


class Sublist3r(Plugin):
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
        countInserted = 0
        markerSublister = "# Coded By Ahmed Aboul-Ela - @aboul3la"
        markerFound = False
        for line in file_opened:
            if markerSublister in line:
                markerFound = True
            if not markerFound:
                continue
            if line.startswith("\x1b[92m"):
                line = line[len("\x1b[92m"):]
            if line.endswith("\x1b[0m"):
                line = line[:-1*len("\x1b[0m")]
            domainGroup = re.search(
                r"((?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9])", line.strip())
            if domainGroup is not None:
                # a domain has been found
                domain = domainGroup.group(1)
                inserted, _ = Ip().initialize(domain).addInDb()
                # failed, domain is out of wave, still noting thi
                if not inserted:
                    notes += domain+" exists but already added.\n"
                else:
                    countInserted += 1
                    notes += domain+" inserted.\n"
        if notes.strip() == "":
            return None, None, None, None
        if not markerFound:
            return None, None, None, None
        return notes, tags, "wave", {"wave": None}
