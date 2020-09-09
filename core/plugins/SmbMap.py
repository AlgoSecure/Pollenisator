"""A plugin to parse smbmap scan"""

from core.plugins.plugin import Plugin
from core.Models.Ip import Ip
from core.Models.Port import Port
import re
import csv

def smbmap_format(row):
    """Parse row of smbmap csv file
    Args:
        row: row of smbmap csv file content parsed as a list
    Returns:
        A tuple with values:
            0. if the filename matched a pattern, the pattern. None otherwise
            1. the targeted host
    """
    interesting_name_list = ["passwd", "password", "pwd", "mot_de_passe", "motdepasse", "auth",
                             "creds", "confidentiel", "confidential", "backup", ".xml", ".conf", ".cfg", "unattended"]
    interesting_type = None
    if row[3] == "f": # isDir
        for interesting_name in interesting_name_list:
            if interesting_name in row[4].lower():
                interesting_type = interesting_name
                break
    return interesting_type, row[0]
   


class SmbMap(Plugin):
    def getFileOutputArg(self):
        """Returns the command line paramater giving the output file
        Returns:
            string
        """
        return " --csv "

    def getFileOutputExt(self):
        """Returns the expected file extension for this command result file
        Returns:
            string
        """
        return ".csv"

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
        content = csv.reader(file_opened, delimiter=',', quotechar='"')
        targets = {}
        interesting_files = {}
        less_interesting_notes = ""
        first_row = True
        for row in content:
            if first_row and not ','.join(row).startswith("Host,Share,Privs,isDir,Path,fileSize,Date"):
                return None, None, None, None
            elif first_row:
                first_row = False
                continue
            interesting_file_type, target = smbmap_format(row)
            targets[target] = {"ip": target, "port": 445, "proto": "tcp"}
            if interesting_file_type is not None:
                interesting_files[interesting_file_type] = interesting_files.get(interesting_file_type, [])
                interesting_files[interesting_file_type].append(', '.join(row))
                tags=["Interesting"]
            else:
                less_interesting_notes += ", ".join(row)+"\n"
        for interesting_file_type in interesting_files.keys():
            notes += "\n=====================Interesting files:=====================\n"
            notes += str(interesting_file_type)+":\n"
            for elem in interesting_files[interesting_file_type]:
                 notes += "\t"+str(elem)+"\n"
        notes += "\n=====================Other files:=====================\n"+less_interesting_notes
        
        return notes, tags, "port", targets
