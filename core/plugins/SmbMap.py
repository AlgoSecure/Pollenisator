"""A plugin to parse smbmap scan"""

from core.plugins.plugin import Plugin
from core.Models.Ip import Ip
from core.Models.Port import Port
import re


def smbmap_format(smbmap_output):
    """Parse raw smbmap file
    Args:
        smbmap_output: raw smbmap file content
    Returns:
        A tuple with values:
            0. a string formated where each line are : fullpath  permissions  date
            1. a list of interesting name file found
            2. targets as described in Parse
    """
    targets = {}
    regex_only_match_serv = re.compile(
        r"^\[\+\] IP: ([^:\s]+)(?::\d+)?\sName: \S+\s+$")
    # group 1 = SHARE NAME group 2 = PERMISSIONS
    regex_only_match_share_header = re.compile(r"^\t(\S+)\s+([A-Z , ]+)$")
    # group 1 = directory full path
    regex_only_match_dir = re.compile(r"^\t(\S+)$")
    # group 1 = d ou -, group 2 = permissions, group 3 = date, group 4 = filename
    regex_only_match_files = re.compile(
        r"^\s+([d-])([xrw-]{9})\s+([^\t]+)\t(.+)$")
    ret = ""
    interesting_files = {}
    interesting_name_list = ["passwd", "password", "pwd", "mot_de_passe", "motdepasse", "auth",
                             "creds", "confidentiel", "confidential", "backup", ".xml", ".conf", ".cfg", "unattended"]
    current_serv = ""
    current_share = ""
    current_dir = ""
    ip_states = []
    lines = smbmap_output.split("\n")
    for line in lines:
        result = regex_only_match_serv.match(line)
        if result is not None:
            ip = str(result.group(1))
            current_serv = ip
            if ip not in ip_states:
                ip_o = Ip().initialize(ip)
                ip_o.addInDb()
                Port().initialize(ip, "445", "tcp", "samba").addInDb()
                targets[str(ip_o.getId())] = {
                    "ip": ip, "port": "445", "proto": "tcp"}

                ip_states.append(ip)
            continue
        result = regex_only_match_share_header.match(line)
        if result is not None:
            share_name = str(result.group(1))
            permissions = str(result.group(2))
            current_share = share_name
            continue
        result = regex_only_match_dir.match(line)
        if result is not None:
            dir_path = str(result.group(1))
            current_dir = dir_path
            continue
        result = regex_only_match_files.match(line)
        if result is not None:
            # isDirectory = (str(result.group(1)) == "d")
            permissions = str(result.group(2))
            date = str(result.group(3))
            file_name = str(result.group(4))
            fullpath = "\\\\"+current_serv+"\\" + \
                current_share+current_dir[1:]+file_name
            for interesting_names in interesting_name_list:
                if interesting_names.lower() in file_name.lower():
                    interesting_files["Shared "+interesting_names] = interesting_files.get(
                        "Shared " + interesting_names, [])
                    interesting_files["Shared "+interesting_names].append(
                        fullpath+"\t"+permissions+"\t"+date)
            ret += fullpath+"\t"+permissions+"\t"+date+"\n"
            continue
    return ret, interesting_files, targets


class SmbMap(Plugin):
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
        notes = file_opened.read()
        if not notes.startswith("[+] Finding open SMB ports...."):
            return None, None, None, None
        if "[!] Authentication error occured" in notes:
            targets = {}
        else:
            full_notes, interesting_files, targets = smbmap_format(notes)
            for target in targets:
                port_m = Port.fetchObject(
                    {"ip": targets[target]["ip"], "port": targets[target]["port"], "proto": "tcp"})
                port_m.updateInfos(interesting_files)
            if interesting_files:
                tags=["Interesting"]
            notes = "=====================Interesting files:=====================\n"
            for type_shared in interesting_files:
                notes = "\n"+type_shared+":\n"
                notes += ("\n".join(interesting_files[type_shared]))+"\n"
            notes += "=====================Other files:=====================\n"+full_notes
        return notes, tags, "port", targets
