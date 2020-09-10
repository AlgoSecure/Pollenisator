"""Hold functions to interact form the scan tab in the notebook"""
from core.Components.Monitor import Monitor
from core.Components.mongo import MongoCalendar
import tkinter as tk
import tkinter.ttk as ttk
import multiprocessing
from core.Models.Command import Command
from core.Models.Tool import Tool
from core.Application.Dialogs.ChildDialogFileParser import ChildDialogFileParser
from core.Application.Dialogs.ChildDialogEditCommandSettings import ChildDialogEditCommandSettings
from core.Components.AutoScanMaster import autoScan
from PIL import Image, ImageTk
import os


def autoscan_execute(calendarName):
    """
    Call the autoScan function with given pentest name as endless and no reprint.

    Args:
        calendarName: the pentest database name to auto scan.
    """
    autoScan(calendarName, True, True)


class ScanManager:
    """Scan model class"""

    def __init__(self, nbk, linkedTreeview, calendarToScan, settings):
        """Constructor, initialize a Monitor object"""
        self.monitor = Monitor(calendarToScan)
        self.calendarToScan = calendarToScan
        self.nbk = nbk
        self.running_auto_scans = []
        self.settings = settings
        self.btn_autoscan = None
        
        self.parent = None
        self.workerTv = None
        self.linkTw = linkedTreeview
        abs_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(abs_path, "../../icon/")
        self.ok_icon = ImageTk.PhotoImage(Image.open(path+"tool.png"))
        self.nok_icon = ImageTk.PhotoImage(Image.open(path+"cross.png"))
        self.running_icon = ImageTk.PhotoImage(Image.open(path+"running.png"))

    def startAutoscan(self):
        """Start an automatic scan. Will try to launch all undone tools."""

        if self.settings.db_settings.get("include_all_domains", False):
            answer = tk.messagebox.askyesno(
                "Autoscan warning", "The current settings will add every domain found in attack's scope. Are you sure ?")
            if not answer:
                return
        from core.Components.AutoScanMaster import sendStartAutoScan
        self.btn_autoscan.configure(
            text="Stop Scanning", command=self.stopAutoscan)
        tasks = sendStartAutoScan(MongoCalendar.getInstance().calendarName)
        self.running_auto_scans = tasks
    
    

    def stop(self):
        """Stop an automatic scan. Will try to stop running tools."""
        
        self.stopAutoscan()
        if self.monitor is not None:
            self.monitor.stop()

    def refreshUI(self):
        """Reload informations and renew widgets"""
        mongoInstance = MongoCalendar.getInstance()
        workernames = self.monitor.getWorkerList()
        running_scans = Tool.fetchObjects({"status":"running"})
        for children in self.scanTv.get_children():
            self.scanTv.delete(children)
        for running_scan in running_scans:
            self.scanTv.insert('','end', running_scan.getId(), text=running_scan.name, values=(running_scan.dated), image=self.running_icon)
        for children in self.workerTv.get_children():
            self.workerTv.delete(children)
        for workername in workernames:
            registeredCommands = set()
            try:
                worker_node = self.workerTv.insert(
                    '', 'end', workername, text=workername, image=self.ok_icon)
            except tk.TclError:
                worker_node = self.workerTv.item(workername)
            worker_registered = mongoInstance.findInDb("pollenisator", "workers", {"name":workername}, False)
            commands_registered = worker_registered["registeredCommands"]
            for command in commands_registered:
                try:
                    self.workerTv.insert(
                        worker_node, 'end', command, text=command, image=self.ok_icon)
                except tk.TclError:
                    pass
                registeredCommands.add(str(command))
            allCommands = Command.getList(None, mongoInstance.calendarName)
            for command in allCommands:
                if command not in registeredCommands:
                    try:
                        self.workerTv.insert(
                            worker_node, '0', 'notRegistered|'+command, text=command, image=self.nok_icon)
                    except tk.TclError:
                        pass
                else:
                    try:
                        self.workerTv.delete('notRegistered|'+command)
                    except tk.TclError:
                        pass
        if len(registeredCommands) > 0 and self.btn_autoscan is None:
            if self.running_auto_scans:
                self.btn_autoscan = ttk.Button(
                    self.parent, text="Stop Scanning", command=self.stopAutoscan)
                self.btn_autoscan.pack()
            else:
                self.btn_autoscan = ttk.Button(
                    self.parent, text="Start Scanning", command=self.startAutoscan)
                self.btn_autoscan.pack()

    def initUI(self, parent):
        """Create widgets and initialize them
        Args:
            parent: the parent tkinter widget container."""
        if self.workerTv is not None:
            self.refreshUI()
            return
        mongoInstance = MongoCalendar.getInstance()
        self.parent = parent
        ### WORKER TREEVIEW : Which worker knows which commands
        lblworker = ttk.Label(self.parent, text="Workers:")
        lblworker.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
        self.workerTv = ttk.Treeview(self.parent)
        self.workerTv['columns'] = ('workers')
        self.workerTv.heading("#0", text='Workers', anchor=tk.W)
        self.workerTv.column("#0", anchor=tk.W)
        self.workerTv.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        self.workerTv.bind("<Double-Button-1>", self.OnDoubleClick)
        workernames = self.monitor.getWorkerList()
        total_registered_commands = 0
        for workername in workernames:
            registeredCommands = set()

            worker_node = self.workerTv.insert(
                '', 'end', workername, text=workername, image=self.ok_icon)
            commands_registered = mongoInstance.getRegisteredCommands(
                workername)
            for command in commands_registered:
                self.workerTv.insert(worker_node, 'end', None,
                                   text=command, image=self.ok_icon)
                registeredCommands.add(str(command))
            allCommands = Command.getList(None, mongoInstance.calendarName)
            for command in allCommands:
                if command not in registeredCommands:
                    try:
                        self.workerTv.insert(worker_node, '0', 'notRegistered|' +
                                        str(command), text=str(command), image=self.nok_icon)
                    except tk.TclError:
                        pass
            total_registered_commands += len(registeredCommands)
        #### TREEVIEW SCANS : overview of ongoing auto scan####
        lblscan = ttk.Label(self.parent, text="Scan overview:")
        lblscan.pack(side=tk.TOP, padx=10, pady=5, fill=tk.X)
        self.scanTv = ttk.Treeview(self.parent)
        self.scanTv['columns'] = ('Started at')
        self.scanTv.heading("#0", text='Scans', anchor=tk.W)
        self.scanTv.column("#0", anchor=tk.W)
        self.scanTv.pack(side=tk.TOP, padx=10, pady=10, fill=tk.X)
        self.scanTv.bind("<Double-Button-1>", self.OnDoubleClick)
        running_scans = Tool.fetchObjects({"status":"running"})
        for running_scan in running_scans:
            self.scanTv.insert('','end', running_scan.getId(), text=running_scan.name, values=(running_scan.dated), image=self.running_icon)
        #### BUTTONS FOR AUTO SCANNING ####
        if total_registered_commands > 0:
            if self.running_auto_scans:
                self.btn_autoscan = ttk.Button(
                    self.parent, text="Stop Scanning", command=self.stopAutoscan)
                self.btn_autoscan.pack()
            else:
                self.btn_autoscan = ttk.Button(
                    self.parent, text="Start Scanning", command=self.startAutoscan)
                self.btn_autoscan.pack()
        btn_parse_scans = ttk.Button(
            self.parent, text="Parse existing files", command=self.parseFiles)
        btn_parse_scans.pack()

    def OnDoubleClick(self, event):
        """Callback for a double click on ongoing scan tool treeview. Open the clicked tool in main view and focus on it.
        Args:
            event: Automatically filled when event is triggered. Holds info about which line was double clicked
        """
        if self.scanTv is not None:
            self.nbk.select(0)
            tv = event.widget
            item = tv.identify("item", event.x, event.y)
            self.linkTw.see(item)
            self.linkTw.selection_set(item)
            self.linkTw.focus(item)


    def stopAutoscan(self):
        """
        Stop an automatic scan. Will terminate celery running tasks.
        """
        try:
            if self.btn_autoscan is not None:
                self.btn_autoscan.configure(
                    text="Start Scanning", command=self.startAutoscan)
        except tk.TclError:
            pass
        print("Stopping auto... ")
        for task in self.running_auto_scans:
            task.revoke(terminate=True)

    def parseFiles(self):
        """
        Ask user to import existing files to import.
        """
        dialog = ChildDialogFileParser(self.parent)
        self.parent.wait_window(dialog.app)

    def notify(self, _iid, _action):
        """
        Reload UI when notified
        """
        if self.workerTv is not None:
            self.refreshUI()

    def sendEditToolConfig(self, worker, command_name, remote_bin, plugin):
        mongoInstance = MongoCalendar.getInstance()
        queueName = str(mongoInstance.calendarName)+"&" + \
            worker
        self.monitor.app.control.add_consumer(
            queue=queueName,
            reply=True,
            exchange="celery",
            exchange_type="direct",
            routing_key="transient",
            destination=[worker])
        from AutoScanWorker import editToolConfig
        result_async = editToolConfig.apply_async(args=[command_name, remote_bin, plugin], queue=queueName, retry=False, serializer="json")
        if self.monitor is not None:
            self.monitor.workerRegisterCommands(worker)
    def OnDoubleClick(self, event):
        """Callback for treeview double click.
        If a link treeview is defined, open mainview and focus on the item with same iid clicked.
        Args:
            event: used to identified which link was clicked. Auto filled
        """
        if self.workerTv is not None:
            tv = event.widget
            item = tv.identify("item", event.x, event.y)
            if item.startswith("notRegistered|"):
                worker = self.workerTv.parent(item)
                command_name = item.split("|")[1]
                dialog = ChildDialogEditCommandSettings(self.parent, "Edit worker tools config")
                self.parent.wait_window(dialog.app)
                if isinstance(dialog.rvalue, tuple):
                    tasks = self.sendEditToolConfig(worker, command_name, dialog.rvalue[0], dialog.rvalue[1])
