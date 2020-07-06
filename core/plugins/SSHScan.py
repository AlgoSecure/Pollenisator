"""A plugin to parse sshscan"""

import json
from core.plugins.plugin import Plugin
from core.Models.Ip import Ip
from core.Models.Port import Port
from core.Models.Defect import Defect


class SSHScan(Plugin):
    def getFileOutputArg(self):
        """Returns the command line paramater giving the output file
        Returns:
            string
        """
        return " -o "

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
        content = file_opened.read()
        targets = {}
        try:
            notes_json = json.loads(content)
        except json.decoder.JSONDecodeError:
            return None, None, None, None
        oneScanIsValid = False
        for scan in notes_json:
            try:
                if scan.get('ssh_scan_version', None) is None:
                    continue
                ips = [scan["hostname"], scan["ip"]]
                port = str(scan["port"])
                for ip in ips:
                    Ip().initialize(ip).addInDb()
                    port_o = Port().initialize(ip, port, "tcp", "ssh")
                    res, iid = port_o.addInDb()
                    if not res:
                        port_o = Port.fetchObject({"_id": iid})
                    notes = "\n".join(
                        scan["compliance"].get("recommendations", []))
                    targets[str(port_o.getId())] = {
                        "ip": ip, "port": port, "proto": "tcp"}
                    oneScanIsValid = True
                    if "nopassword" in scan["auth_methods"]:
                        tags = ["P0wned!"]
                    # Will not exit if port was not ssh
                    is_ok = scan["compliance"]["compliant"]
                    if str(is_ok) == "False":
                        port_o.updateInfos({"compliant": "False"})
                        port_o.updateInfos({"auth_methods": scan["auth_methods"]})
                        Defect().initialize(ip, port, "tcp", "Défauts d’implémentation de la configuration SSH",
                                            "Très difficile", "Majeur", "Important",  "N/A", ["Socle"], notes=notes, proofs=[]).addInDb()
            except KeyError:
                continue
        if not oneScanIsValid:
            return None, None, None, None
        return notes, tags, "port", targets
