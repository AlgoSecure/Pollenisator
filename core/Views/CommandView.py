"""View for command object. Handle node in treeview and present forms to user when interacted with."""

from core.Views.ViewElement import ViewElement
from core.Components.Settings import Settings
import core.Components.Utils as Utils
import tkinter as tk


class CommandView(ViewElement):
    """
    View for command object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory.
    """
    icon = 'command.png'

    def __init__(self, appTw, appViewFrame, mainApp, controller):
        """Constructor
        Args:
            appTw: a PollenisatorTreeview instance to put this view in
            appViewFrame: an view frame to build the forms in.
            mainApp: the Application instance
            controller: a CommandController for this view.
        """
        self.menuContextuel = None
        self.widgetMenuOpen = None
        super().__init__(appTw, appViewFrame, mainApp, controller)

    def _commonWindowForms(self, default={}):
        """Construct form parts identical between Modify and Insert forms
        Args:
            default: a dict of default values for inputs (sleep_between, priority, max_thread). Default to empty respectively "0", "0", "1"
        """
        panel_bottom = self.form.addFormPanel(grid=True)
        panel_bottom.addFormLabel("Delay")
        panel_bottom.addFormStr("Delay", r"\d+", default.get("sleep_between", "0"), width=5, column=1)
        panel_bottom.addFormHelper(
            "Delay in-between two launch of this command (in seconds)", column=2)
        panel_bottom.addFormLabel("Priority", row=1)
        panel_bottom.addFormStr("Priority", r"\d+", default.get("priority", "0"),
                                width=2, row=1, column=1)
        panel_bottom.addFormHelper(
            "Priority in queue (0 is HIGHEST)", row=1, column=2)
        panel_bottom.addFormLabel("Threads", row=2)
        panel_bottom.addFormStr("Threads", r"\d+", default.get("max_thread", "1"),
                                width=2, row=2, column=1)
        panel_bottom.addFormHelper(
            "Number of authorized parallel running of this command on one worker.", row=2, column=2)

    def openModifyWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to update or delete an existing Command
        """
        modelData = self.controller.getData()
        self._initContextualMenu()
        settings = self.mainApp.settings
        settings.reloadSettings()
        panel_top = self.form.addFormPanel(grid=True)
        panel_top.addFormLabel("Name", modelData["name"], sticky=tk.NW)
        panel_top.addFormLabel("Level", modelData["lvl"], row=1, sticky=tk.NW)
        panel_top_bis = self.form.addFormPanel(grid=True)
        panel_top_bis.addFormChecklist(
            "Types", Settings.getPentestTypes().keys(), modelData["types"], column=1)
        panel_safe = self.form.addFormPanel(grid=True)
        panel_safe.addFormLabel("Safe")
        panel_safe.addFormCheckbox(
            "Safe", "Safe", modelData["safe"] == "True", column=1)
        panel_safe.addFormHelper(
            "If checked, this command can be run by an auto scan.", column=2)
        panel_text = self.form.addFormPanel()
        panel_text.addFormLabel("Command line options", side="top")
        panel_text.addFormHelper(
            """Do not include binary name/path\nDo not include Output file option\nUse variables |wave|, |scope|, |ip|, |port|, |parent_domain|, |outputDir|, |port.service|, |port.product|, |ip.infos.*| |port.infos.*|""", side="right")
        panel_text.addFormText("Command line options", r"",
                               modelData["text"], self.menuContextuel, side="left", height=5)
        panel_bottom = self.form.addFormPanel(grid=True)
        if modelData["lvl"] == "port":
            panel_bottom.addFormLabel("Ports/Services", column=0)
            panel_bottom.addFormStr(
                "Ports/Services", r"^(\d{1,5}|[^\,]+)(?:,(\d{1,5}|[^\,]+))*$", modelData["ports"], self.popup, width=50, column=1)
            panel_bottom.addFormHelper(
                "Services, ports or port ranges.\nthis list must be separated by a comma, if no protocol is specified, tcp/ will be used.\n Example: ssl/http,https,http/ssl,0-65535,443...",column=2)
        self._commonWindowForms(modelData)
        self.completeModifyWindow()

    def openInsertWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to insert a new Command
        """
        self._initContextualMenu()
        panel_top = self.form.addFormPanel(grid=True)
        panel_top.addFormLabel("Name")
        panel_top.addFormStr("Name", r"\S+", "", None, column=1)
        panel_top.addFormLabel("Level", row=1)
        panel_top.addFormCombo(
            "Level", ["network", "domain", "ip", "port", "wave"], "network", row=1, column=1)
        panel_top.addFormHelper(
            "lvl wave: will run on each wave once\nlvl network: will run on each NetworkIP once\nlvl domain: will run on each scope domain once\nlvl ip: will run on each ip/hostname once\nlvl port: will run on each port once", row=1, column=2)
        panel_types = self.form.addFormPanel(grid=True)
        panel_types.addFormChecklist(
            "Types", Settings.getPentestTypes(), [], row=2, column=1)
        panel_types.addFormHelper(
            "This command will be added by default on pentest having a type checked in this list.\nThis list can be modified on settings.", column=2)
        panel_safe = self.form.addFormPanel(grid=True)
        panel_safe.addFormLabel("Safe")
        panel_safe.addFormCheckbox(
            "Safe", "Safe", "False", column=1)
        panel_safe.addFormHelper(
            "If checked, this command can be run by an auto scan.", column=2)
        panel_text = self.form.addFormPanel()
        panel_text.addFormLabel("Command line options", side="top")
        panel_text.addFormHelper(
            """Do not include binary name/path\nDo not include Output file option\nUse variables |wave|, |scope|, |ip|, |port|, |parent_domain|, |outputDir|, |port.service|, |port.product|, |ip.infos.*| |port.infos.*|""", side="right")
        panel_text.addFormText("Command line options",
                               r"", "", self.menuContextuel, side="top", height=5)
        panel_bottom = self.form.addFormPanel(grid=True)
        panel_bottom.addFormLabel("Ports/Services")
        panel_bottom.addFormStr(
            "Ports/Services", r"^((.{0})|(\d{1,5}|[^\, ]+)(?:, (\d{1,5}|[^\, ]+))*)$", "", width=50, column=1)
        panel_bottom.addFormHelper(
            "Services, ports or port ranges.\nthis list must be separated by a comma, if no protocol is specified, tcp/ will be used.\n Example: ssl/http,https,http/ssl,0-65535,443...", column=2)

        self._commonWindowForms()
        self.completeInsertWindow()

    def addInTreeview(self, parentNode=None):
        """Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
        """
        if parentNode is None:
            parentNode = self.getParent()
        self.appliTw.views[str(self.controller.getDbId())] = {"view": self}
        self.appliTw.insert(parentNode, "end", str(
            self.controller.getDbId()), text=str(self.controller.getModelRepr()), tags=self.controller.getTags(), image=self.getClassIcon())
        if "hidden" in self.controller.getTags():
            self.hide()

    def getParent(self):
        """
        Return the id of the parent node in treeview.

        Returns:
            return the saved command_node node inside the Appli class.
        """
        return self.appliTw.commands_node

    def _initContextualMenu(self):
        """Initiate contextual menu with variables"""
        self.menuContextuel = tk.Menu(self.appliViewFrame, tearoff=0, background='#A8CF4D',
                                      foreground='white', activebackground='#A8CF4D', activeforeground='white')
        self.menuContextuel.add_command(
            label="Wave id", command=self.addWaveVariable)
        self.menuContextuel.add_command(
            label="Network address without slash nor dots", command=self.addIpReseauDirVariable)
        self.menuContextuel.add_command(
            label="Network address", command=self.addIpReseauVariable)
        self.menuContextuel.add_command(
            label="Parent domain", command=self.addParentDomainVariable)
        self.menuContextuel.add_command(label="Ip", command=self.addIpVariable)
        self.menuContextuel.add_command(
            label="Ip without dots", command=self.addIpDirVariable)
        self.menuContextuel.add_command(
            label="Port", command=self.addPortVariable)

    def popup(self, event):
        """
        Fill the self.widgetMenuOpen and reraise the event in the editing window contextual menu

        Args:
            event: a ttk Treeview event autofilled. Contains information on what treeview node was clicked.
        """
        self.widgetMenuOpen = event.widget
        self.menuContextuel.post(event.x_root, event.y_root)
        self.menuContextuel.focus_set()
        self.menuContextuel.bind('<FocusOut>', self.popupFocusOut)

    def popupFocusOut(self, _event=None):
        """
        Called when the contextual menu is unfocused
        Args:
            _event: a ttk event autofilled. not used but mandatory.
        """
        self.menuContextuel.unpost()

    def addWaveVariable(self):
        """
        insert the wave variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.
        """
        self.widgetMenuOpen.insert(tk.INSERT, "|wave|")

    def addIpReseauDirVariable(self):
        """
        insert the scope_dir variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.
        """
        self.widgetMenuOpen.insert(tk.INSERT, "|scope_dir|")

    def addIpReseauVariable(self):
        """
        insert the scope variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.
        """
        self.widgetMenuOpen.insert(tk.INSERT, "|scope|")

    def addParentDomainVariable(self):
        """
        insert the scope variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.
        """
        self.widgetMenuOpen.insert(tk.INSERT, "|parent_domain|")

    def addIpVariable(self):
        """
        insert the ip variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.
        """
        self.widgetMenuOpen.insert(tk.INSERT, "|ip|")

    def addIpDirVariable(self):
        """
        insert the ip_dir variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.
        """
        self.widgetMenuOpen.insert(tk.INSERT, "|ip_dir|")

    def addPortVariable(self):
        """
        insert the port variable inside the a tkinter widget stored in appli widgetMenuOpen attribute.
        """
        self.widgetMenuOpen.insert(tk.INSERT, "|port|")

    def key(self):
        """Returns a key for sorting this node
        Returns:
            string, key to sort
        """
        return str(self.controller.getModelRepr()).lower()
