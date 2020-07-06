"""A plugin to parse a dirsearch scan"""

from core.plugins.plugin import Plugin
from core.Models.Ip import Ip
from core.Models.Port import Port
from core.Application.Dialogs.ChildDialogQuestion import ChildDialogQuestion
import re
import webbrowser
import tkinter as tk

def parse_dirsearch_file(notes):
    """Parse a dirsearch resulting raw text file
    Args:
        notes: the dirsearch raw text
    Returns:
        a dict with scanned hosts has keys and another dict as value:
            this dict has scanned ports as keys and another dict as value:
                this dict has 3 keys:
                    * service: "http" or "https"
                    * paths: a list of path found on port
                    * statuscode: a list of status code matching the list of paths
    """
    hosts = {}
    parsed = []
    lines = notes.split("\n")
    for line in lines:
        words = line.strip().split()
        res = []
        for word in words:
            if word.strip() != "":
                res.append(word.strip())
        if len(res) == 3:
            parsed.append(res)
    for pathFound in parsed:
        # Auto detect and infos extract
        try:
            # integer conversion fails if not valid
            statuscode = int(pathFound[0])
        except ValueError:
            continue
        if re.search(r"\d+K?M?B", pathFound[1]) is None:
            continue
        url = pathFound[2]
        re_host_port = r"http.?:\/\/([^\/]+)(\/.*)?"
        service = "https" if "https://" in url else "http"
        host_port = re.search(re_host_port, url)
        if host_port is not None:
            infos = host_port.group(1).split(":")
            if len(infos) == 2:
                host = infos[0]
                port = infos[1]
            elif len(infos) == 1:
                host = infos[0]
                port = "443" if service == "https" else "80"
            elif len(infos) > 2:
                host = "/".join(infos[:-1])
                port = infos[-1]
            if host not in hosts:
                hosts[host] = {}
            if port not in hosts[host]:
                hosts[host][port] = {}
            hosts[host][port]["service"] = service
            hosts[host][port]["paths"] = hosts[host][port].get(
                "paths", [])+["   ".join(pathFound)]
            hosts[host][port][statuscode] = hosts[host][port].get(
                statuscode, [])+[host_port.group(2)]
        else:
            print("Not a url: "+str(pathFound[2]))

    return hosts


class Dirsearch(Plugin):

    def __init__(self):
        """Constructor"""
        self.port_m = None

    def getActions(self, toolmodel):
        """
        Summary: Add buttons to the tool view.
        Args:
            toolmodel : the tool model opened in the pollenisator client.
        Return:
            A dictionary with buttons text as key and function callback as value.
        """
        self.port_m = Port.fetchObject(
            {"ip": toolmodel.ip, "port": toolmodel.port, "proto": toolmodel.proto})
        if self.port_m is None:
            return {}
        return {"Open 200 in browser": self.openInBrowser}

    def openInBrowser(self, _event=None):
        """Callback of action  Open 200 in browser
        Open all 200 status code in browser as tabs. If more that 10 status code 200 are to be opened, shows a warning.
        Args:
            _event: not used but mandatory
        """
        ssl = self.port_m.infos.get("SSL", "False")
        paths = self.port_m.infos.get("Dirsearch_200", [])
        url_base = "https://" if ssl == "True" else "http://"
        toplevel = tk.Toplevel()
        if len(paths) > 10:
            dialog = ChildDialogQuestion(toplevel,
                                     "OPEN WARNING", "Becareful for you are about to open "+str(len(paths)) + "in your browser. This may a bit too much.", ["Continue", "Cancel"])
            toplevel.wait_window(dialog.app)
            if dialog.rvalue != "Continue":
                return
        toplevel.destroy()
        for path in paths:
            url = url_base + self.port_m.ip+":"+str(self.port_m.port)+path
            webbrowser.open_new_tab(url)

    def getFileOutputArg(self):
        """Returns the command line paramater giving the output file
        Returns:
            string
        """
        return " --plain-text-report "

    def getFileOutputExt(self):
        """Returns the expected file extension for this command result file
        Returns:
            string
        """
        return ".txt"

    def getFileOutputPath(self, commandExecuted):
        """Returns the output file path given in the executed command using getFileOutputArg
        Args:
            commandExecuted: the command that was executed with an output file inside.
        Returns:
            string: the path to file created
        """
        return commandExecuted.split(self.getFileOutputArg())[-1].strip().split(" ")[0]


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
        tags = ["todo"]
        data = file_opened.read()
        notes = ""
        if data.strip() == "":
            return None, None, None, None
        else:
            hosts = parse_dirsearch_file(data)
            if not hosts.keys():
                return None, None, None, None
            targets = {}
            for host in hosts:
                Ip().initialize(host).addInDb()
                for port in hosts[host]:
                    port_o = Port()
                    port_o.initialize(host, port, "tcp",
                                      hosts[host][port]["service"])
                    res, iid = port_o.addInDb()
                    if not res:
                        port_o = Port.fetchObject({"_id": iid})
                    targets[str(port_o.getId())] = {
                        "ip": host, "port": port, "proto": "tcp"}
                    hosts[host][port]["paths"].sort(key=lambda x: int(x[0]))
                    results = "\n".join(hosts[host][port]["paths"])
                    notes += results
                    newInfos = {}
                    for statuscode in hosts[host][port]:
                        if isinstance(statuscode, int):
                            if hosts[host][port].get(statuscode, []):
                                newInfos["Dirsearch_"+str(statuscode)
                                         ] = hosts[host][port][statuscode]
                    newInfos["SSL"] = "True" if hosts[host][port]["service"] == "https" else "False"
                    port_o.updateInfos(newInfos)
        return notes, tags, "port", targets
