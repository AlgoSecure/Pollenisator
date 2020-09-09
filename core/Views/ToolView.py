"""View for tool object. Handle node in treeview and present forms to user when interacted with."""

from core.Views.ViewElement import ViewElement
from core.Components.mongo import MongoCalendar
import tkinter.messagebox
import tkinter as tk
from tkinter import TclError
from core.Views.DefectView import DefectView
from core.Components.FileStorage import FileStorage
from core.Models.Defect import Defect
from core.Controllers.DefectController import DefectController
from core.Application.Dialogs.ChildDialogQuestion import ChildDialogQuestion
from core.Application.Dialogs.ChildDialogInfo import ChildDialogInfo
import core.Components.Utils as Utils
import os


class ToolView(ViewElement):
    """View for tool object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory
        done_icon: icon filename for done tools
        ready_icon: icon filename for ready tools
        running_icon: icon filename for running tools
        not_ready_icon: icon filename for not ready tools
        cached_icon: a cached loaded PIL image icon of ToolView.icon. Starts as None.
        cached_done_icon: a cached loaded PIL image icon of ToolView.done_icon. Starts as None.
        cached_ready_icon: a cached loaded PIL image icon of ToolView.ready_icon. Starts as None.
        cached_running_icon: a cached loaded PIL image icon of ToolView.running_icon. Starts as None.
        cached_not_ready_icon: a cached loaded PIL image icon of ToolView.not_ready_icon. Starts as None.
        """

    done_icon = 'done_tool.png'
    ready_icon = 'waiting.png'
    running_icon = 'running.png'
    not_ready_icon = 'cross.png'
    icon = 'tool.png'

    cached_icon = None
    cached_done_icon = None
    cached_ready_icon = None
    cached_running_icon = None
    cached_not_ready_icon = None

    def getIcon(self):
        """
        Load the object icon in cache if it is not yet done, and returns it

        Return:
            Returns the icon representing this object.
        """
        status = self.controller.getStatus()
        iconStatus = "not_ready"
        if "done" in status:
            cache = self.__class__.cached_done_icon
            ui = self.__class__.done_icon
            iconStatus = "done"
        elif "running" in status:
            ui = self.__class__.running_icon
            cache = self.__class__.cached_running_icon
            iconStatus = "running"
        elif "OOS" not in status and "OOT" not in status:
            ui = self.__class__.ready_icon
            cache = self.__class__.cached_ready_icon
            iconStatus = "ready"
        else:
            ui = self.__class__.not_ready_icon
            cache = self.__class__.cached_not_ready_icon
        if status == [] or iconStatus not in status :
            self.controller.setStatus([iconStatus])

        if cache is None:
            from PIL import Image, ImageTk
            abs_path = os.path.dirname(os.path.abspath(__file__))

            path = os.path.join(abs_path, "../../icon/"+ui)
            if iconStatus == "done":
                self.__class__.cached_done_icon = ImageTk.PhotoImage(
                    Image.open(path))
                return self.__class__.cached_done_icon
            elif iconStatus == "running":
                self.__class__.cached_running_icon = ImageTk.PhotoImage(
                    Image.open(path))
                return self.__class__.cached_running_icon
            elif iconStatus == "ready":
                self.__class__.cached_ready_icon = ImageTk.PhotoImage(
                    Image.open(path))
                return self.__class__.cached_ready_icon
            else:
                self.__class__.cached_not_ready_icon = ImageTk.PhotoImage(
                    Image.open(path))
                return self.__class__.cached_not_ready_icon
        return cache

    def openModifyWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to update or delete an existing Tool
        """
        modelData = self.controller.getData()
        top_panel = self.form.addFormPanel(grid=True)
        top_panel.addFormLabel("Name", modelData["name"])
        dates_panel = self.form.addFormPanel(grid=True)
        dates_panel.addFormLabel("Start date")
        dates_panel.addFormDate(
            "Start date", self.mainApp, modelData["dated"], column=1)
        dates_panel.addFormLabel("End date", row=1)
        dates_panel.addFormDate(
            "End date", self.mainApp, modelData["datef"], row=1, column=1)
        dates_panel.addFormLabel("Scanner", row=2)
        dates_panel.addFormStr(
            "Scanner", r"", modelData["scanner_ip"], row=2, column=1)
        dates_panel.addFormLabel("Command executed", row=3)
        dates_panel.addFormStr("Command executed", "", modelData["text"], row=3, column=1, state="disabled")
        notes = modelData.get("notes", "")
        top_panel = self.form.addFormPanel()
        top_panel.addFormLabel("Notes", side="top")
        top_panel.addFormText("Notes", r"", notes, None, side="top", height=15)

        actions_panel = self.form.addFormPanel()
        #Ready is legacy, OOS and/or OOT should be used
        if "ready" in self.controller.getStatus():
            actions_panel.addFormButton(
                "Local launch", self.localLaunchCallback, side="right")
            if self.mainApp.scanManager.monitor.hasWorkers():
                actions_panel.addFormButton(
                    "Run on worker", self.launchCallback, side="right")
            else:
                actions_panel.addFormLabel(
                    "Info", "Tool is ready but no celery worker found", side="right")
        elif "OOS" in self.controller.getStatus() or "OOT" in self.controller.getStatus():
            actions_panel.addFormButton(
                "Local launch", self.localLaunchCallback, side="right")
            if self.mainApp.scanManager.monitor.hasWorkers():
                actions_panel.addFormButton(
                    "Run on worker", self.launchCallback, side="right")
            else:
                actions_panel.addFormLabel(
                    "Info", "Tool is ready but no celery worker found", side="right")
        elif "running" in self.controller.getStatus():
            actions_panel.addFormButton(
                "Stop", self.stopCallback, side="right")
        elif "done" in self.controller.getStatus():
            actions_panel.addFormButton(
                "Download result file", self.downloadResultFile, side="right")
            tools_infos = Utils.loadToolsConfig()
            try:
                mod = Utils.loadPlugin(
                    tools_infos[self.controller.getName()]["plugin"])
                pluginActions = mod.getActions(self.controller.model)
            except KeyError:  # Happens when parsed an existing file.:
                pluginActions = None
            if pluginActions is not None:
                for pluginAction in pluginActions:
                    actions_panel.addFormButton(
                        pluginAction, pluginActions[pluginAction], side="right")
                actions_panel.addFormButton(
                    "Reset", self.resetCallback, side="right")
        defect_panel = self.form.addFormPanel(grid=True)
        defect_panel.addFormButton("Create defect", self.createDefectCallback)
        self.completeModifyWindow()

    def addInTreeview(self, parentNode=None, _addChildren=True):
        """Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            _addChildren: not used for tools
        """
        if parentNode is None:
            parentNode = ToolView.DbToTreeviewListId(
                self.controller.getParent())
            nodeText = str(self.controller.getModelRepr())
        elif parentNode == '':
            # For a filter all node are added to the root which is '' in tkinter
            nodeText = self.controller.getDetailedString()
        else:
            # if a parent node is given it is the model parent, the treeview parent can be retrivied with ToolView.DbToTreeviewListId
            parentNode = ToolView.DbToTreeviewListId(parentNode)
            nodeText = str(self.controller.getModelRepr())
        try:
            parentNode = self.appliTw.insert(
                self.controller.getParent(), 0, parentNode, text="Tools", image=self.getClassIcon())
        except TclError:  #  trigger if tools list node already exist
            pass
        self.appliTw.views[str(self.controller.getDbId())] = {"view": self}
        try:
            self.appliTw.insert(parentNode, "end", str(
                self.controller.getDbId()), text=nodeText, tags=self.controller.getTags(), image=self.getIcon())
        except tk.TclError:
            pass
        self.appliTw.sort(parentNode)
        if "hidden" in self.controller.getTags():
            self.hide()

    def downloadResultFile(self, _event=None):
        """Callback for tool click #TODO move to ToolController
        Download the tool result file and asks the user if he or she wants to open it. 
        If OK, tries to open it using xdg-open or os.startsfile
        Args:
            _event: not used 
        """
        fs = FileStorage()
        fs.open()
        path = None
        if fs.sftp_connection is not None:
            dialog = ChildDialogInfo(
                self.appliViewFrame, "Download Started", "Downloading...")
            resultFile = self.controller.getResultFile()
            dialog.show()
            if resultFile != "" and resultFile is not None:
                path = fs.getToolResult(resultFile)
            else:
                tkinter.messagebox.showerror(
                    "Download failed", "The result file does not exist.")
            dialog.destroy()
        else:
            tkinter.messagebox.showerror(
                "Download failed", "The sftp connection failed.")
            return
        fs.close()
        if path is not None:
            if os.path.isfile(path):
                dialog = ChildDialogQuestion(self.appliViewFrame, "Download completed",
                                             "The file has been downloaded.\n Would you like to open it?", answers=["Open", "Cancel"])
                self.appliViewFrame.wait_window(dialog.app)
                if dialog.rvalue == "Open":
                    Utils.execute("xdg-open "+path)
                    return
                else:
                    return
            path = None
        if path is None:
            tkinter.messagebox.showerror(
                "Download failed", "the file does not exist on sftp server")

    def createDefectCallback(self, _event=None):
        """Callback for tool click #TODO move to ToolController
        Creates an empty defect view and open it's insert window with notes = tools notes.
        """
        modelData = self.controller.getData()
        toExport = modelData["notes"]
        for widget in self.appliViewFrame.winfo_children():
            widget.destroy()
        dv = DefectView(self.appliTw, self.appliViewFrame,
                        self.mainApp, DefectController(Defect(modelData)))
        dv.openInsertWindow(toExport)

    def localLaunchCallback(self, _event=None):
        """
        Callback for the launch tool button. Will launch it on localhost pseudo 'worker'.  #TODO move to ToolController

        Args:
            event: Automatically generated with a button Callback, not used.
        """
        mongoInstance = MongoCalendar.getInstance()
        self.mainApp.scanManager.monitor.launchTask(
            mongoInstance.calendarName, self.controller.model, "", False, "localhost")
        self.controller.update()
        self.form.clear()
        for widget in self.appliViewFrame.winfo_children():
            widget.destroy()
        self.openModifyWindow()

    def safeLaunchCallback(self, _event=None):
        """
        Callback for the launch tool button. Will queue this tool to a celery worker. #TODO move to ToolController
        Args:
            event: Automatically generated with a button Callback, not used.
        Returns:
            None if failed. 
        """
        mongoInstance = MongoCalendar.getInstance()
        result = self.mainApp.scanManager.monitor.launchTask(
            mongoInstance.calendarName, self.controller.model)
        return result

    def launchCallback(self, _event=None):
        """
        Callback for the launch tool button. Will queue this tool to a celery worker. #TODO move to ToolController
        Will try to launch respecting limits first. If it does not work, it will asks the user to force launch.

        Args:
            _event: Automatically generated with a button Callback, not used.
        """
        res = self.safeLaunchCallback()
        if not res:
            dialog = ChildDialogQuestion(self.appliViewFrame,
                                         "Safe queue failed", "This tool cannot be launched because no worker add space for its thread.\nDo you want to launch it anyway?")
            self.appliViewFrame.wait_window(dialog.app)
            answer = dialog.rvalue
            if answer == "Yes":
                mongoInstance = MongoCalendar.getInstance()
                res = self.mainApp.scanManager.monitor.launchTask(
                    mongoInstance.calendarName, self.controller.model, "", False)
        if res:
            self.controller.update()
            self.form.clear()
            for widget in self.appliViewFrame.winfo_children():
                widget.destroy()
            self.openModifyWindow()

    def stopCallback(self, _event=None):
        """
        Callback for the launch tool stop button. Will stop this celery task. #TODO move to ToolController

        Args:
            _event: Automatically generated with a button Callback, not used.
        """
        success = self.mainApp.scanManager.monitor.stopTask(
            self.controller.getData())
        delete_anyway = False
        if success == False:
            delete_anyway = tkinter.messagebox.askyesno(
                "Stop failed", """This tool cannot be stopped because its trace has been lost (The application has been restarted and the tool is still not finished).\n
                    Reset tool anyway?""")
        if delete_anyway or success:
            self.controller.markAsNotDone()
            self.controller.update()
            self.form.clear()
            for widget in self.appliViewFrame.winfo_children():
                widget.destroy()
            self.openModifyWindow()

    def resetCallback(self, _event=None):
        """
        Callback for the reset tool stop button. Will reset the tool to a ready state. #TODO move to ToolController

        Args:
            event: Automatically generated with a button Callback, not used.
        """
        self.controller.markAsNotDone()
        self.controller.update()
        self.form.clear()
        for widget in self.appliViewFrame.winfo_children():
            widget.destroy()
        self.openModifyWindow()

    @classmethod
    def DbToTreeviewListId(cls, parent_db_id):
        """Converts a mongo Id to a unique string identifying a list of tools given its parent
        Args:
            parent_db_id: the parent node mongo ID
        Returns:
            A string that should be unique to describe the parent list of tool node
        """
        return str(parent_db_id)+"|Tools"

    @classmethod
    def treeviewListIdToDb(cls, treeview_id):
        """Extract from the unique string identifying a list of tools the parent db ID
        Args:
            treeview_id: the treeview node id of a list of tools node
        Returns:
            the parent object mongo id as string
        """
        return str(treeview_id).split("|")[0]

    def updateReceived(self):
        """Called when a tool update is received by notification.
        Update the tool treeview item (resulting in icon reloading)
        """
        self.appliTw.item(str(self.controller.getDbId()), text=str(
            self.controller.getModelRepr()), image=self.getIcon())
        super().updateReceived()
