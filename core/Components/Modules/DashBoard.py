"""Dashboard module to display pentest info"""
import os
import tkinter as tk
import tkinter.messagebox
import tkinter.ttk as ttk
from datetime import datetime
from os import listdir
from os.path import isfile, join

from bson.objectid import ObjectId
from PIL import Image, ImageTk

from core.Application.Dialogs.ChildDialogCombo import ChildDialogCombo
from core.Application.Dialogs.ChildDialogDefectView import ChildDialogDefectView
from core.Application.Dialogs.ChildDialogProgress import ChildDialogProgress
from core.Application.Dialogs.ChildDialogQuestion import ChildDialogQuestion
from core.Components.mongo import MongoCalendar
from core.Models.Ip import Ip
from core.Models.Port import Port
from core.Models.Tool import Tool
import core.Components.Utils as Utils


class DashBoard:
    """
    Shows information about ongoing pentest. 
    """
    iconName = "tab_dashboard.png"
    tabName = " Dashboard "
    def __init__(self, parent, settings):
        """
        Constructor
        """
        self.dashboardFrame = None
        self.parent = None
        self.treevw = None
        self.style = None
        self.ips = None
        self.ports = None
        self.tools = None

        iconPath = Utils.getIconDir()
        self.icons = {}
        self.icons["tool"] = ImageTk.PhotoImage(
            Image.open(iconPath+"tool.png"))
        self.icons["cross"] = ImageTk.PhotoImage(
            Image.open(iconPath+"cross.png"))
        self.icons["running"] = ImageTk.PhotoImage(
            Image.open(iconPath+"running.png"))
        self.icons["done"] = ImageTk.PhotoImage(
            Image.open(iconPath+"done_tool.png"))
        self.icons["ready"] = ImageTk.PhotoImage(
            Image.open(iconPath+"waiting.png"))
        self.icons["Not ready"] = ImageTk.PhotoImage(
            Image.open(iconPath+"cross.png"))
    
    def open(self):
        mongoInstance = MongoCalendar.getInstance()
        if mongoInstance.calendarName is not None:
            self.refreshUI()
        return True

    def refreshUI(self):
        """
        Reload data and display them
        """
        self.loadData()
        self.displayData()

    def loadData(self):
        """
        Fetch data from database
        """
        self.ports = Port.fetchObjects({})
        self.ips = Ip.fetchObjects({})
        self.tools = Tool.fetchObjects({})

    def displayData(self):
        """
        Display loaded data in treeviews
        """
        dialog = ChildDialogProgress(self.parent, "Loading dashboard ",
                                     "Refreshing dashboard. Please wait for a few seconds.", 200, "determinate")
        dialog.show(10)

        # Reset Ip treeview
        for children in self.treevw.get_children():
            self.treevw.delete(children)
        dialog.update(1)
        listOfip = []
        for ip in self.ips:
            servicesCount = len([x for x in Port.fetchObjects({"ip": ip.ip})])
            listOfip.append((ip.ip, servicesCount))
        dialog.update(2)
        listOfip.sort(key=lambda tup: tup[1], reverse=True)
        for i in range(len(listOfip)):
            self.treevw.insert(
                '', 'end', i, text=listOfip[i][0], values=(listOfip[i][1]))
        dialog.update(3)
        # Reset Port treeview
        for children in self.treevwport.get_children():
            self.treevwport.delete(children)
        dialog.update(4)
        portCounts = {}
        for port in self.ports:
            if port.port not in portCounts.keys():
                portCounts[port.port] = 1
            else:
                portCounts[port.port] += 1
        dialog.update(5)

        port_id = 0
        # Ordering dictionnary
        portCounts = {k: v for k, v in sorted(
            portCounts.items(), key=lambda item: item[1], reverse=True)}
        for portCount in portCounts:
            self.treevwport.insert('', 'end', port_id, text=str(
                portCount), values=(portCounts[portCount]))
            port_id += 1
        dialog.update(6)
        # Tool part
        # Reset Tools treeview
        for children in self.treevwtools.get_children():
            self.treevwtools.delete(children)
        dialog.update(7)
        listOfTools = [_ for _ in self.tools]
        listOfTools.sort(key=lambda x: x.status, reverse=True)

        result = MongoCalendar.getInstance().aggregate("tools",
                                                       [
                                                           {
                                                               "$group":
                                                               {
                                                                   "_id": {"name": "$name", "status": "$status", "wave": "$wave"}, "count": {"$sum": 1}
                                                               }
                                                           }
                                                       ]
                                                       )

        result = [_ for _ in result]
        result.sort(key=lambda x: x["_id"]["name"])
        dialog.update(8)
        tools_dashboard = {}
        for tool in result:
            toolName = tool["_id"]["name"]
            toolWave = tool["_id"]["wave"]
            tools_dashboard[toolWave] = tools_dashboard.get(toolWave, {})
            tools_dashboard[toolWave][toolName] = tools_dashboard[toolWave].get(toolName, {})
            toolStatus = "Not ready" if len(
                tool["_id"]["status"]) == 0 else tool["_id"]["status"][0]
            tools_dashboard[toolWave][toolName][toolStatus] = tools_dashboard[toolWave][toolName].get(toolStatus, 0) + 1
        for wave in tools_dashboard.keys():
            for toolName in tools_dashboard[wave].keys():
                self.treevwtools.insert('', 'end', None, text=str(
                    toolName), values=(wave, tools_dashboard[wave][toolName].get("ready", 0), tools_dashboard[wave][toolName].get("running", 0), tools_dashboard[wave][toolName].get("done", 0)))
        dialog.update(9)
        # Defect Part
        # reset defect TW
        for children in self.treevwDefaults.get_children():
            self.treevwDefaults.delete(children)

        result = MongoCalendar.getInstance().aggregate("defects",
                                                       [
                                                           {
                                                               "$group":
                                                               {
                                                                   "_id": {"risk": "$risk", "type": "$type"}, "count": {"$sum": 1}
                                                               }
                                                           }
                                                       ]
                                                       )
        dialog.update(10)
        result = [_ for _ in result]
        result.sort(key=lambda x: x["count"], reverse=True)
        for defect in result:
            defectRisk = defect["_id"]["risk"]
            defectType = " ".join(defect["_id"]["type"])
            defectCount = defect["count"]
            self.treevwDefaults.insert('', 'end', None, text=str(
                defectRisk), values=(defectType, defectCount))
        dialog.destroy()

    def initUI(self, parent, nbk, treevw):
        """
        Initialize Dashboard widgets
        Args:
            parent: its parent widget
        """
        if self.parent is not None:  # Already initialized
            return
        self.parent = parent
        self.dashboardFrame = ttk.Frame(parent)

        self.rowHeight = 20
        self.style = ttk.Style()
        self.style.configure('DashBoard.Treeview', rowheight=self.rowHeight)

        frameTwHosts = ttk.Frame(self.dashboardFrame)
        self.treevw = ttk.Treeview(
            frameTwHosts, style='DashBoard.Treeview', height=5)
        self.treevw['columns'] = ('services')
        self.treevw.heading("#0", text='Hostname', anchor=tk.W)
        self.treevw.column("#0", anchor=tk.W, width=150)
        self.treevw.heading('services', text='Services')
        self.treevw.column('services', anchor='center', width=40)
        self.treevw.grid(row=0, column=0, sticky=tk.NSEW)
        scbVSel = ttk.Scrollbar(frameTwHosts,
                                orient=tk.VERTICAL,
                                command=self.treevw.yview)
        self.treevw.configure(yscrollcommand=scbVSel.set)
        scbVSel.grid(row=0, column=1, sticky=tk.NS)
        #frameTwHosts.pack(side=tk.TOP, fill=tk.X, padx=100, pady=10)
        frameTwHosts.columnconfigure(0, weight=1)
        frameTwHosts.rowconfigure(0, weight=1)
        frameTwHosts.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=10)

        frameTwPports = ttk.Frame(self.dashboardFrame)
        self.treevwport = ttk.Treeview(
            frameTwPports, style='DashBoard.Treeview', height=5)
        self.treevwport['columns'] = ('amount')
        self.treevwport.heading("#0", text='Port', anchor=tk.W)
        self.treevwport.column("#0", anchor=tk.W, width=70)
        self.treevwport.heading('amount', text='Amount')
        self.treevwport.column('amount', anchor='center', width=40)
        self.treevwport.grid(row=0, column=0, sticky=tk.NSEW)
        scbVSel = ttk.Scrollbar(frameTwPports,
                                orient=tk.VERTICAL,
                                command=self.treevwport.yview)
        self.treevwport.configure(yscrollcommand=scbVSel.set)
        scbVSel.grid(row=0, column=1, sticky=tk.NS)
        frameTwPports.columnconfigure(0, weight=1)
        frameTwPports.rowconfigure(0, weight=1)
        frameTwPports.grid(row=0, column=1, sticky=tk.NSEW, padx=5, pady=10)

        frameTools = ttk.Frame(self.dashboardFrame)
        self.treevwtools = ttk.Treeview(
            frameTools, style='DashBoard.Treeview', height=10)
        self.treevwtools['columns'] = ('wave', 'ready', 'running', 'done')
        self.treevwtools.heading("#0", text='Tool name', anchor=tk.W)
        self.treevwtools.column("#0", anchor=tk.W, width=150)
        self.treevwtools.heading('#1', text='Wave')
        self.treevwtools.column('#1', anchor='center', width=10)
        self.treevwtools.heading('#2', text='Ready')
        self.treevwtools.column('#2', anchor='center', width=10)
        self.treevwtools.heading('#3', text='Running')
        self.treevwtools.column('#3', anchor='center', width=10)
        self.treevwtools.heading('#4', text='Done')
        self.treevwtools.column('#4', anchor='center', width=10)
        self.treevwtools.grid(row=0, column=0, sticky=tk.NSEW)
        scbVSel = ttk.Scrollbar(frameTools,
                                orient=tk.VERTICAL,
                                command=self.treevwtools.yview)
        self.treevwtools.configure(yscrollcommand=scbVSel.set)
        self.treevwtools.bind("<Motion>", self.mycallback)
        scbVSel.grid(row=0, column=1, sticky=tk.NS)
        frameTools.columnconfigure(0, weight=1)
        frameTools.rowconfigure(0, weight=1)
        frameTools.grid(row=1, sticky=tk.NSEW, padx=5, pady=5, columnspan=2)

        frameDefaults = ttk.Frame(self.dashboardFrame)
        self.treevwDefaults = ttk.Treeview(
            frameDefaults, style='DashBoard.Treeview', height=15)
        self.treevwDefaults["columns"] = ('type', 'amount')
        self.treevwDefaults.heading("#0", text='Risk', anchor=tk.W)
        self.treevwDefaults.column("#0", anchor=tk.W, width=50)
        self.treevwDefaults.heading('type', text='Type')
        self.treevwDefaults.column('type', anchor='center', width=40)
        self.treevwDefaults.heading('amount', text='Amount')
        self.treevwDefaults.column('amount', anchor='center', width=40)
        self.treevwDefaults.grid(row=0, column=0, sticky=tk.NSEW)
        scbVSel = ttk.Scrollbar(frameDefaults,
                                orient=tk.VERTICAL,
                                command=self.treevwDefaults.yview)
        self.treevwDefaults.configure(yscrollcommand=scbVSel.set)
        scbVSel.grid(row=0, column=1, sticky=tk.NS)
        frameDefaults.columnconfigure(0, weight=1)
        frameDefaults.rowconfigure(0, weight=1)
        frameDefaults.grid(row=2, sticky=tk.NSEW, padx=5, columnspan=2, pady=5)

        self.dashboardFrame.columnconfigure(0, weight=1)
        self.dashboardFrame.columnconfigure(1, weight=1)
        self.dashboardFrame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        # self.refreshUI()

    def mycallback(self, event):
        _iid = self.treevwtools.identify_row(event.y)
        self.treevwtools.item(_iid)
