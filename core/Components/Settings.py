"""Hold functions to interact with the settings"""
import os
import tkinter.ttk as ttk
import tkinter as tk
import tkinter.messagebox
import json
from core.Components.mongo import MongoCalendar
from shutil import which


class Settings:
    """
    Represents the settings of pollenisator.
    There are three level of settings:
        * local settings: stored in a file under ../../config/settings.cfg
        * pentest db settings: stored in the pentest database under settings collection
        * global settings: stored in the pollenisator database under settings collection
    """
    def __init__(self):
        """
        Load the tree types of settings and stores them in dictionnaries
        """
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.confdir = os.path.join(dir_path, "../../config/settings.cfg")

        self.local_settings = {}
        try:
            with open(self.confdir, "r") as f:
                self.local_settings = json.loads(f.read())
        except json.JSONDecodeError:
            self.local_settings = {}
        except IOError:
            self.local_settings = {}
        self.db_settings = {}
        self.global_settings = {}
        self.text_pentest_types = None
        self.text_tags = None
        self.box_pentest_type = None
        self.visual_include_domains_with_ip_in_scope = None
        self.visual_include_domains_with_topdomain_in_scope = None
        self.visual_search_show_hidden = None
        self.visual_search_exact_match = None
        self.visual_include_all_domains = None
        self.text_pentesters = None
        self.box_favorite_term = None
        self.text_terms = None

    @classmethod
    def getTags(cls):
        """
        Returns tags defined in settings.
        Returns:
            If none are defined returns {"todo":"orange", "unscanned":"yellow", "P0wned!":"red", "Interesting":"dark green", "Uninteresting":"sky blue", "Neutral":"white"}
            otherwise returns a dict with defined key values
        """
        mongoInstance = MongoCalendar.getInstance()
        tags = mongoInstance.findInDb(
            "pollenisator", "settings", {"key": "tags"}, False)
        if tags is not None:
            if isinstance(tags["value"], dict):
                return tags["value"]
        return  {"todo":"orange", "unscanned":"yellow", "P0wned!":"red", "Interesting":"dark green", "Uninteresting":"sky blue", "Neutral":"white"}

    @classmethod
    def getPentestTypes(cls):
        """
        Returns pentest types and associeted defect type defined in settings.
        Returns:
            If none are defined returns {"Web":["Socle", "Application", "Données", "Politique"], "LAN":["Infrastructure", "Active Directory", "Données", "Politique"]}
            otherwise returns a dict with defined key values
        """
        mongoInstance = MongoCalendar.getInstance()
        pentest_types = mongoInstance.findInDb(
            "pollenisator", "settings", {"key": "pentest_types"}, False)
        if pentest_types is not None:
            if isinstance(pentest_types["value"], dict):
                return pentest_types["value"]
        return  {"Web":["Socle", "Application", "Données", "Politique"], "LAN":["Infrastructure", "Active Directory", "Données", "Politique"]}


    def getTerms(self):
        """
        Returns terminals configured 
        Returns:
            If none are defined returns ['''gnome-terminal --window --title="Pollenisator terminal" -- bash --rcfile setupTerminalForPentest.sh''',
             '''xfce4-terminal -x bash --rcfile setupTerminalForPentest.sh''',
             '''xterm -e bash --rcfile setupTerminalForPentest.sh''']
            otherwise returns a list with defined  values
        """
        self._reloadLocalSettings()
        return self.local_settings.get("terms",
            ["""gnome-terminal --window --title="Pollenisator terminal" -- bash --rcfile setupTerminalForPentest.sh""",
             """xfce4-terminal -x bash --rcfile setupTerminalForPentest.sh""",
             "xterm -e bash --rcfile setupTerminalForPentest.sh"])
    
    def getFavoriteTerm(self):
        """
        Returns favorite terminal configured 
        Returns:
            If none are defined returns first in the list of terms
            Otherwise returns the favorite terminal configured 
        """
        self._reloadLocalSettings()
        fav = self.local_settings.get("fav_term", None)
        if fav is None:
            terms = self.getTerms()
            for term in terms:
                term_name = term.split(" ")[0].strip()
                if which(term_name):
                    fav = term_name
        return fav

    def setFavoriteTerm(self):
        """
        Change favorite term 
        """
        self._reloadLocalSettings()
        self.local_settings["fav_term"] = self.box_favorite_term.get()
        self.saveLocalSettings()
    
    def _reloadLocalSettings(self):
        """
        Reload local settings from local conf file
        """
        try:
            with open(self.confdir, "r") as f:
                self.local_settings = json.loads(f.read())
        except json.JSONDecodeError:
            self.local_settings = {}
        except IOError:
            self.local_settings = {}

    def _reloadDbSettings(self):
        """
        Reload pentest database settings from pentest database
        """
        mongoInstance = MongoCalendar.getInstance()
        dbSettings = mongoInstance.find("settings", {})
        if dbSettings is None:
            dbSettings = {}
        for settings_dict in dbSettings:
            try:
                self.db_settings[settings_dict["key"]] = settings_dict["value"]
            except KeyError:
                pass

    def _reloadGlobalSettings(self):
        """
        Reload pentest database settings from pollenisator database
        """
        mongoInstance = MongoCalendar.getInstance()
        globalSettings = mongoInstance.findInDb("pollenisator", "settings", {})
        for settings_dict in globalSettings:
            self.global_settings[settings_dict["key"]] = settings_dict["value"]

    def reloadSettings(self):
        """
        Reload local, database and global settings.
        """
        self._reloadLocalSettings()
        self._reloadDbSettings()
        self._reloadGlobalSettings()

    def reloadUI(self):
        """
        Reload all settings and refresh view with values
        """
        self.reloadSettings()
        self.visual_include_all_domains.set(
            self.db_settings.get("include_all_domains", False))
        self.visual_include_domains_with_ip_in_scope.set(
            self.db_settings.get("include_domains_with_ip_in_scope", False))
        self.visual_include_domains_with_topdomain_in_scope.set(
            self.db_settings.get("include_domains_with_topdomain_in_scope", False))
        self.visual_search_show_hidden.set(
            self.local_settings.get("search_show_hidden", True))
        self.visual_search_exact_match.set(
            self.local_settings.get("search_exact_match", False))
        self.text_terms.delete('1.0', tk.END)
        terms_cmd = self.getTerms()
        self.text_terms.insert(tk.INSERT, "\n".join(terms_cmd))
        self.text_pentesters.delete('1.0', tk.END)
        self.text_pentesters.insert(
            tk.INSERT, "\n".join(
                self.db_settings.get("pentesters", [])))
        terms_name = [term_cmd.split(" ")[0] for term_cmd in terms_cmd]
        self.box_favorite_term.config(values=terms_name)
        fav_term = self.getFavoriteTerm()
        if fav_term in terms_name:
            self.box_favorite_term.set(fav_term)
        self.box_pentest_type.set(self.db_settings.get("pentest_type", "None"))
        self.text_pentest_types.delete('1.0', tk.END)
        pentestTypes = Settings.getPentestTypes()
        buffer = ""
        for pentestType, pentestTypeDefectTypes in pentestTypes.items():
            buffer += pentestType +" : "+ (", ".join(pentestTypeDefectTypes))+"\n"
        self.text_pentest_types.insert(
            tk.INSERT, buffer)
        self.text_tags.delete('1.0', tk.END)
        tagsRegistered = Settings.getTags()
        buffer = ""
        for tagName, tagColor in tagsRegistered.items():
            buffer += tagName +" : "+ tagColor+"\n"
        self.text_tags.insert(
            tk.INSERT, buffer)
        self.canvas.bind('<Enter>', self.boundToMousewheel)
        self.canvas.bind('<Leave>', self.unboundToMousewheel)
        self.canvas.update()
        self.canvas.create_window((0, 0), window=self.settingsFrame, anchor='nw')
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.configure(yscrollcommand=self.myscrollbar.set)

    def saveLocalSettings(self):
        """
        Save local settings to conf file
        """
        with open(self.confdir, "w") as f:
            f.write(json.dumps(self.local_settings))

    def save(self):
        """
        Save all the settings (local, database and global)
        """
        mongoInstance = MongoCalendar.getInstance()
        for k, v in self.global_settings.items():
            if mongoInstance.findInDb("pollenisator", "settings", {"key": k}, False) is None:
                mongoInstance.insertInDb("pollenisator", "settings", {
                                         "key": k, "value": v})
            else:
                mongoInstance.updateInDb("pollenisator", "settings", {
                    "key": k}, {"$set": {"value": v}})
        for k, v in self.db_settings.items():
            if mongoInstance.find("settings", {"key": k}, False) is None:
                mongoInstance.insert("settings", {
                    "key": k, "value": v})
            else:
                mongoInstance.update("settings", {
                    "key": k}, {"$set": {"value": v}})
        
        self.saveLocalSettings()
        self.reloadUI()

    def _onMousewheel(self, event):
        """Scroll the settings canvas
        Args:
            event: scroll info filled when scroll event is triggered"""
        if event.num == 5 or event.delta == -120:
            count = 1
        if event.num == 4 or event.delta == 120:
            count = -1
        self.canvas.yview_scroll(count, "units")

    def boundToMousewheel(self, _event):
        """Called when the main view canvas is focused.
        Bind the command scrollbar button on linux to the main view canvas
        Args:
            _event: not used but mandatory"""
        self.canvas.bind_all("<Button-4>", self._onMousewheel)
        self.canvas.bind_all("<Button-5>", self._onMousewheel)

    def unboundToMousewheel(self, _event):
        """Called when the main view canvas is unfocused.
        Unbind the command scrollbar button on linux to the main view canvas
        Args:
            _event: not used but mandatory"""
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def initUI(self, parent):
        """Create settings widgets and initialize them
        Args:
            parent: parent tkinter container widget"""
        if self.visual_include_all_domains is not None:  # Already built
            self.reloadUI()
            return
        self.canvas = tk.Canvas(parent, bg="white")
        self.settingsFrame = ttk.Frame(self.canvas)
        self.myscrollbar = tk.Scrollbar(parent, orient="vertical", command=self.canvas.yview)
        self.myscrollbar.grid(column=1, row=0, sticky="ns")
        
        self.canvas.grid(column=0, row=0, sticky="nsew")
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(0, weight=1)

        self.visual_include_all_domains = tk.BooleanVar()
        self.visual_include_domains_with_ip_in_scope = tk.BooleanVar()
        self.visual_include_domains_with_topdomain_in_scope = tk.BooleanVar()
        self.visual_search_show_hidden = tk.BooleanVar()
        self.visual_search_exact_match = tk.BooleanVar()

        lbl_domains = ttk.LabelFrame(
            self.settingsFrame, text="Discovered domains options:")
        lbl_domains.pack(padx=10, pady=10, side=tk.TOP,
                         anchor=tk.W, fill=tk.X, expand=tk.YES)
        chkbox_include_domains_with_ip_in_scope = ttk.Checkbutton(lbl_domains, text="Check if discovered subdomains ips are in scope",
                                                                  variable=self.visual_include_domains_with_ip_in_scope)
        chkbox_include_domains_with_ip_in_scope.pack(
            padx=10, pady=10, side=tk.TOP, anchor=tk.W)

        chkbox_include_domains_with_topdomain_in_scope = ttk.Checkbutton(lbl_domains, text="Check if discovered subdomains have a top domain already in scope",
                                                                         variable=self.visual_include_domains_with_topdomain_in_scope)
        chkbox_include_domains_with_topdomain_in_scope.pack(
            padx=10, pady=10, side=tk.TOP, anchor=tk.W)
        chkbox_include_all_domains = ttk.Checkbutton(lbl_domains, text="/!\\ Include every domain found in scope",
                                                     variable=self.visual_include_all_domains)
        chkbox_include_all_domains.pack(
            padx=10, pady=10, side=tk.TOP, anchor=tk.W)
        
        frame_term = ttk.LabelFrame(self.settingsFrame, text="Terminals:")
        self.text_terms = tk.scrolledtext.ScrolledText(
            frame_term, relief=tk.SUNKEN, height=4, width=130)
        self.text_terms.pack(side=tk.TOP, fill=tk.X,pady=5)
        frame_fav_term = ttk.Frame(frame_term)
        lbl_fav_term = ttk.Label(frame_term, text="Favorite term:")
        lbl_fav_term.pack(side=tk.LEFT, anchor=tk.W)
        self.box_favorite_term = ttk.Combobox(frame_term, values=(self.getTerms()), state="readonly")
        self.box_favorite_term.pack(side=tk.LEFT, anchor=tk.W)
        frame_fav_term.pack(padx=10, pady=10, side=tk.TOP,
                           anchor=tk.W, fill=tk.X, expand=tk.YES)
        frame_term.pack(padx=10, pady=10, side=tk.TOP,
                           anchor=tk.W, fill=tk.X, expand=tk.YES)
        lbl_SearchBar = ttk.LabelFrame(self.settingsFrame, text="Search settings:")
        lbl_SearchBar.pack(padx=10, pady=10, side=tk.TOP,
                           anchor=tk.W, fill=tk.X, expand=tk.YES)
        chkbox_search_show_hidden = ttk.Checkbutton(lbl_SearchBar, text="Show hidden objects",
                                                    variable=self.visual_search_show_hidden)
        chkbox_search_show_hidden.pack(
            padx=10, pady=10, side=tk.TOP, anchor=tk.W)
        chkbox_search_exact_match = ttk.Checkbutton(lbl_SearchBar, text="Exact match",
                                                    variable=self.visual_search_exact_match)
        chkbox_search_exact_match.pack(
            padx=10, pady=10, side=tk.TOP, anchor=tk.W)

        lblframe_pentest_params = ttk.LabelFrame(
            self.settingsFrame, text="Pentest parameters:")
        lblframe_pentest_params.pack(
            padx=10, pady=10, side=tk.TOP, anchor=tk.W, fill=tk.X, expand=tk.YES)
        lbl_pentest_type = ttk.Label(
            lblframe_pentest_params, text="Pentest type:")
        lbl_pentest_type.grid(row=0, column=0, sticky=tk.E)
        self.box_pentest_type = ttk.Combobox(
            lblframe_pentest_params, values=tuple(Settings.getPentestTypes().keys()), state="readonly")
        self.box_pentest_type.grid(row=1, column=1, sticky=tk.W)
        self.text_pentesters = tk.scrolledtext.ScrolledText(
            lblframe_pentest_params, relief=tk.SUNKEN, height=3)
        lbl_pentesters = ttk.Label(
            lblframe_pentest_params, text="Pentester names:")
        lbl_pentesters.grid(row=2, column=0, sticky=tk.E)
        self.text_pentesters.grid(row=2, column=1, sticky=tk.W, pady=5)
        lblframe_global_params = ttk.LabelFrame(
            self.settingsFrame, text="Global parameters:")
        lblframe_global_params.pack(
            padx=10, pady=10, side=tk.TOP, anchor=tk.W, fill=tk.X, expand=tk.YES)
        lbl_pentest_types = ttk.Label(
            lblframe_global_params, text="Pentests possible types:")
        lbl_pentest_types.grid(row=0, column=0, sticky=tk.E)
        self.text_pentest_types = tk.scrolledtext.ScrolledText(
            lblframe_global_params, relief=tk.SUNKEN, height=6)
        self.text_pentest_types.grid(row=0, column=1, sticky=tk.W)
        lbl_tags = ttk.Label(
            lblframe_global_params, text="Registered tags:")
        lbl_tags.grid(row=1, column=0, sticky=tk.E)
        self.text_tags = tk.scrolledtext.ScrolledText(
            lblframe_global_params, relief=tk.SUNKEN, height=6)
        self.text_tags.grid(row=1, column=1, sticky=tk.W)
        btn_save = ttk.Button(parent, text="Save", command=self.on_ok)
        btn_save.grid(row=1, column=0, padx=10, pady=10, sticky="s")
        self.settingsFrame.pack(fill=tk.BOTH, expand=1)

        #self.reloadUI()

    def on_ok(self):
        """Callback on click save button. loads some data and calls save.
        Args:
            parent: parent tkinter container widget"""
        self.db_settings["include_all_domains"] = self.visual_include_all_domains.get(
        ) == 1
        self.db_settings["include_domains_with_ip_in_scope"] = self.visual_include_domains_with_ip_in_scope.get(
        ) == 1
        self.db_settings["pentest_type"] = self.box_pentest_type.get()
        self.db_settings["include_domains_with_topdomain_in_scope"] = self.visual_include_domains_with_topdomain_in_scope.get(
        ) == 1
        self.db_settings["pentesters"] = []
        for pentester in self.text_pentesters.get('1.0', tk.END).split(
                "\n"):
            if pentester.strip() != "":
                self.db_settings["pentesters"].append(
                    pentester.strip())
        self.local_settings["search_show_hidden"] = self.visual_search_show_hidden.get(
        ) == 1
        self.local_settings["search_exact_match"] = self.visual_search_exact_match.get(
        ) == 1
        self.local_settings["terms"] = [x.strip() for x in self.text_terms.get('1.0', tk.END).split("\n") if x.strip() != ""]
        self.local_settings["fav_term"] = self.box_favorite_term.get().strip()
        self.global_settings["pentest_types"] = []
        for type_of_pentest in self.text_pentest_types.get('1.0', tk.END).split(
                "\n"):
            if type_of_pentest.strip() != "":
                line_splitted = type_of_pentest.strip().split(":")
                if len(line_splitted) == 2:
                    typesOfDefects = list(map(lambda x: x.strip(), line_splitted[1].split(",")))
                    self.global_settings["pentest_types"].append(
                        {line_splitted[0].strip():typesOfDefects})
        self.global_settings["tags"] = {}
        for tagRegistered in self.text_tags.get('1.0', tk.END).split(
                "\n"):
            if tagRegistered.strip() != "":
                line_splitted = tagRegistered.strip().split(":")
                if len(line_splitted) == 2:
                    self.global_settings["tags"][line_splitted[0].strip()] = line_splitted[1].strip()
        self.save()
        tkinter.messagebox.showinfo(
            "Settings", "Settings saved.")

    def getPentestType(self):
        """Return selected database pentest type.
        Returns:
            Open database pentest type. string "None" if not defined"""
        return self.db_settings.get("pentest_type", "None")

    def getPentesters(self):
        """Return a list of pentesters registered for open pentest database
        Returns:
            List of pentesters names"""
        return self.db_settings.get("pentesters", [])