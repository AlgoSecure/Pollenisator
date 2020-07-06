"""CalendarTreeview class
Ttk treeview class with added functions.
"""
import tkinter as tk
from bson.objectid import ObjectId
from core.Components.mongo import MongoCalendar
from core.Components.Settings import Settings
from core.Models.Interval import Interval
from core.Models.Ip import Ip
from core.Models.Port import Port
from core.Models.Scope import Scope
from core.Models.Tool import Tool
from core.Models.Wave import Wave
from core.Models.Defect import Defect
from core.Views.IntervalView import IntervalView
from core.Views.IpView import IpView
from core.Views.MultipleIpView import MultipleIpView
from core.Views.MultipleScopeView import MultipleScopeView
from core.Views.MultiSelectionView import MultiSelectionView
from core.Views.PortView import PortView
from core.Views.ScopeView import ScopeView
from core.Views.ToolView import ToolView
from core.Views.WaveView import WaveView
from core.Views.DefectView import DefectView
from core.Controllers.WaveController import WaveController
from core.Controllers.PortController import PortController
from core.Controllers.ScopeController import ScopeController
from core.Controllers.ToolController import ToolController
from core.Controllers.DefectController import DefectController
from core.Controllers.IpController import IpController
from core.Controllers.IntervalController import IntervalController
from core.Application.Dialogs.ChildDialogProgress import ChildDialogProgress
from core.Application.Dialogs.ChildDialogInfo import ChildDialogInfo
from core.Application.Dialogs.ChildDialogCustomCommand import ChildDialogCustomCommand
from core.Application.Dialogs.ChildDialogExportSelection import ChildDialogExportSelection
from core.Application.Treeviews.PollenisatorTreeview import PollenisatorTreeview


class CalendarTreeview(PollenisatorTreeview):
    """Inherit PollenisatorTreeview.
    Ttk treeview class with added functions to handle the main view objects.
    """

    def __init__(self, appli, parentFrame):
        """
        Args:
            appli: a reference to the main Application object.
            parentFrame: the parent tkinter window object.
        """
        super().__init__(appli, parentFrame)
        self._hidden = []  # Hidden objects references
        self.tagsMenu = None  # Menu bar for tag changing
        self.tagsVars = None  # list of tag values
        self.contextualMenu = None  #  contextual menu to open on right click
        self.waves_node = None  # the wave parent node on the treeview
        self.ips_node = None  # the IPs parent node on the treeview
        self.openedViewFrameId = None  # id of opened object in the view frame.

    def initUI(self):
        """Initialize the user interface widgets and binds them."""
        self._initContextualsMenus()
        self.heading('#0', text='Object', anchor=tk.W)
        self.column('#0', stretch=tk.YES, minwidth=300, width=300)
        self.bind("<Button-3>", self.doPopup)
        self.bind("<Button-2>", self.doPopupTag)
        #self.bind("<Return>", self.onTreeviewSelect)
        #self.bind("<Button-1>", self.onTreeviewSelect)
        self.bind("<<TreeviewSelect>>", self.onTreeviewSelect)
        self.bind('<Delete>', self.deleteSelected)
        self.bind('h', self.hideSelection)
        self.bind("<Shift-Down>", self.openNextSameTypeNode)
        self.bind("<Shift-Up>", self.openPrevSameTypeNode)

    def getRows(self, startNode=''):
        """Returns all child nodes of the given startNode iid as a list.
        Args:
            - startNode: node to recursively get children. Default to '' which is rhe treeview root.
        Returns:
            - List of all children iid of given node.
        """
        myRows = []
        children = self.get_children(startNode)
        for child in children:
            myRows.append(child)
            myRows += self.getRows(child)
        return myRows

    def openPrevSameTypeNode(self, _event):
        """Open the first node of the same type above the currently selected object on the tree view.
        Args:
            - _event: not used but mandatory
        Return:
            return the string "break" to stop processing the event
        """
        fromNode = self.selection()
        if fromNode:
            fromNode = fromNode[0]
            rows = self.getRows()
            pos = rows.index(fromNode)
            if pos-1 > 0:
                view_o = self.getViewFromId(fromNode)
                classToFind = view_o.__class__
                for row_nth in range(pos-1, -1, -1):
                    row = rows[row_nth]
                    cmp_view_o = self.getViewFromId(row)
                    if classToFind == cmp_view_o.__class__:
                        self.see(row)
                        self.focus(row)
                        self.selection_set(row)
                        return "break"
        return "break"

    def openNextSameTypeNode(self, _event):
        """Open the first node of the same type below the currently selected object on the tree view.
        Args:
            - _event: not used but mandatory
        Return:
            return the string "break" to stop processing the event
        """
        fromNode = self.selection()
        if fromNode:
            fromNode = fromNode[0]
            rows = self.getRows()
            pos = rows.index(fromNode)
            if pos+1 < len(rows):
                view_o = self.getViewFromId(fromNode)
                classToFind = view_o.__class__
                for row in rows[pos+1:]:
                    cmp_view_o = self.getViewFromId(row)
                    if classToFind == cmp_view_o.__class__:
                        self.see(row)
                        self.focus(row)
                        self.selection_set(row)
                        return "break"
        return "break"

    def doPopup(self, event):
        """Called when a right click is received by the tree view.
        Open the contextual menu at the clicked position.
        Args:
            - event: sent automatically though an event on treeview
        """
        if self.contextualMenu is not None:
            self.popupFocusOut()
        self._initContextualsMenus()
        self.contextualMenu.selection = self.identify(
            "item", event.x, event.y)
        view = self.getViewFromId(str(self.contextualMenu.selection))
        if view is None:
            self.contextualMenu.entryconfig(4, state=tk.DISABLED)
        else:
            self.contextualMenu.entryconfig(4, state=tk.ACTIVE)
        if self.appli.searchMode:
            self.contextualMenu.add_command(
                label="Show in full tree", command=self.showInTreeview)
        super().doPopup(event)

    def doPopupTag(self, event):
        """Called when a middle click is received by the tree view.
        Open the tag menu at the clicked position.
        Args:
            - event: sent automatically though an event on treeview
        """
        self.tagsMenu.selection = self.identify(
            "item", event.x, event.y)
        # display the popup menu
        try:
            self.tagsMenu.post(event.x_root, event.y_root)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            self.tagsMenu.grab_release()
        self.tagsMenu.focus_set()
        self.tagsMenu.bind('<FocusOut>', self.popupFocusOutTag)

    def popupFocusOutTag(self, _=None):
        """Called when the tag contextual menu is unfocused.
        Close the tag contextual menu.
        """
        self.tagsMenu.unpost()

    def showInTreeview(self, _=None):
        """Unfilter the treeview and focus the node stored in the contextualMenu.selection variable0
        Also select it.
        """
        node = str(self.contextualMenu.selection)
        self.unfilter()
        self.see(node)
        self.focus(node)
        self.selection_set(node)

    def tagClicked(self, name):
        """Callback for an event. If the function was called directly it would not work.
        Args:
            - name: the tag name clicked
        """
        return lambda : self.setTagFromMenubar(name)

    def _initContextualsMenus(self):
        """
        Create the contextual menu
        """
        self.contextualMenu = tk.Menu(self.parentFrame, tearoff=0, background='#A8CF4D',
                                      foreground='white', activebackground='#A8CF4D', activeforeground='white')
        self.contextualMenu.add_command(
            label="Custom command", command=self.customCommand)
        self.contextualMenu.add_command(
            label="Export selection", command=self.exportSelection)
        self.tagsMenu = tk.Menu(self.parentFrame, tearoff=0, background='#A8CF4D',
                                foreground='white', activebackground='#A8CF4D', activeforeground='white')
        tags = Settings.getTags()
        listOfLambdas = [self.tagClicked(tag) for tag in list(tags.keys())]
        for i,val in enumerate(tags):
            self.tagsMenu.add_command(
                label=val, command=listOfLambdas[i])
        self.contextualMenu.add_command(
            label="Sort children", command=self.sort)
        self.contextualMenu.add_command(
            label="Expand", command=self.expand)
        self.contextualMenu.add_command(
            label="Collapse", command=self.collapse)
        self.contextualMenu.add_command(
            label="Hide", command=self.hideAndUpdate)
        self.contextualMenu.add_command(
            label="Unhide children", command=self.unhide)
        self.contextualMenu.add_command(
            label="Close", command=self.closeMenu)

    def setTagFromMenubar(self, name):
        """
        Change the tags of every selected object in the treeview to the one selected in the tag contextual menu.
        Args:
            - name: the tag name clicked
        """
        for selected in self.selection():
            view_o = self.getViewFromId(selected)
            view_o.controller.setTags([name])

    def closeMenu(self, _event=None):
        """
        Close the contextual menu. Does nothing, just an empty callback
        Args:
            - _event: not used but mandatory
        """
        # Do nothing and close
        return

    def notify(self, db, collection, iid, action, _parent):
        """
        Callback for the observer implemented in mongo.py.
        Each time an object is inserted, updated or deleted the standard way, this function will be called.

        Args:
            collection: the collection that has been modified
            iid: the mongo ObjectId _id that was modified/inserted/deleted
            action: string "update" or "insert" or "delete". It was the action performed on the iid
            _parent: Not used. the mongo ObjectId of the parent. Only if action in an insert. Not used anymore
        """
        mongoInstance = MongoCalendar.getInstance()
        if not mongoInstance.hasACalendarOpen():
            return
        if mongoInstance.calendarName != db:
            return
        # Delete
        if action == "delete":
            if collection == "defects":
                view = self.getViewFromId(str(iid))
                if view is not None:
                    view.beforeDelete()
                    self.appli.statusbar.notify([],view.controller.getTags())
            try:
                self.delete(ObjectId(iid))
            except tk.TclError:
                pass  # item was not inserted in the treeview

        # Insert
        if action == "insert":
            view = None
            res = mongoInstance.find(collection, {"_id": ObjectId(iid)}, False)
            if collection == "tools":
                view = ToolView(self, self.appli.viewframe,
                                self.appli, ToolController(Tool(res)))
            elif collection == "waves":
                view = WaveView(self, self.appli.viewframe,
                                self.appli, WaveController(Wave(res)))
            elif collection == "scopes":
                view = ScopeView(self, self.appli.viewframe,
                                 self.appli, ScopeController(Scope(res)))
            elif collection == "ports":
                view = PortView(self, self.appli.viewframe,
                                self.appli, PortController(Port(res)))
            elif collection == "ips":
                view = IpView(self, self.appli.viewframe,
                              self.appli, IpController(Ip(res)))
            elif collection == "intervals":
                view = IntervalView(self, self.appli.viewframe,
                                    self.appli, IntervalController(Interval(res)))
            elif collection == "defects":
                view = DefectView(self, self.appli.viewframe,
                                self.appli, DefectController(Defect(res)))
            try:
                if view is not None:
                    view.addInTreeview()
                    view.insertReceived()
                    self.appli.statusbar.notify(view.controller.getTags())
            except tk.TclError:
                pass

        if action == "update":
            try:
                view = self.getViewFromId(str(iid))
                if view is not None:
                    oldTags = self.item(str(iid))["tags"]
                    view.controller.actualize()
                    self.appli.statusbar.notify(view.controller.getTags(), oldTags)
                    self.item(str(iid), text=str(
                        view.controller.getModelRepr()), image=view.getIcon())
            except tk.TclError:
                if view is not None:
                    view.addInTreeview()
            if str(self.appli.openedViewFrameId) == str(iid):
                for widget in self.appli.viewframe.winfo_children():
                    widget.destroy()
                view.openModifyWindow()
            if view is not None:
                view.updateReceived()
        self.appli.statusbar.update()

    def exportSelection(self, _event=None):
        """
        Popup a window to help a user to export some data from treeview.
        Args:
            _event: not used but mandatory
        """
        values = set()
        for selected in self.selection():
            view_o = self.getViewFromId(selected)
            if view_o is not None:
                data = view_o.controller.getData()
                for key in data.keys():
                    if key == "infos":
                        for info_keys in data["infos"]:
                            values.add("infos."+info_keys)
                    else:
                        values.add(key)
        dialog = ChildDialogExportSelection(self, values)
        self.wait_window(dialog.app)
        if isinstance(dialog.rvalue, list):
            fields_to_export = dialog.rvalue
            f = tk.filedialog.asksaveasfilename(defaultextension=".csv")
            if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return
            csv_filename = str(f)
            with open(csv_filename, 'w') as f:
                f.write(", ".join(fields_to_export)+"\n")
                for selected in self.selection():
                    view_o = self.getViewFromId(selected)
                    if view_o is not None:
                        line = []
                        modelData = view_o.controller.getData()
                        for field in fields_to_export:
                            if field.startswith("infos."):
                                line.append(
                                    str(modelData.get("infos", {}).get(field[6:], "")))
                            else:
                                line.append(str(modelData.get(field, "")))
                        f.write(", ".join(line)+"\n")
            dialog = ChildDialogInfo(
                self, "Export completed", "Your export just finished. You can find it here : "+csv_filename)
        self.wait_window(dialog.app)

    def customCommand(self, _event=None):
        """
        Ask the user for a custom tool to launch and which parser it will use.
        Args:
            _event: not used but mandatory
        """
        mongoInstance = MongoCalendar.getInstance()
        workers = self.appli.scanManager.monitor.getWorkerList()
        workers.append("localhost")
        dialog = ChildDialogCustomCommand(
                    self, workers, "localhost")
        self.wait_window(dialog.app)
        if isinstance(dialog.rvalue, tuple):
            commName = dialog.rvalue[0]
            commArgs = dialog.rvalue[1]
            parser = dialog.rvalue[2]
            worker = dialog.rvalue[3]
        for selected in self.selection():
            view_o = self.getViewFromId(selected)
            if view_o is not None:
                lvl = "network" if isinstance(view_o, ScopeView) else None
                lvl = "wave" if isinstance(view_o, WaveView) else lvl
                lvl = "ip" if isinstance(view_o, IpView) else lvl
                lvl = "port" if isinstance(view_o, PortView) else lvl
                if lvl is not None:
                    inst = view_o.controller.getData()
                    wave = inst.get("wave", "Custom commands")
                    if wave == "Custom commands":
                        Wave().initialize("Custom commands").addInDb()
                    tool = Tool()
                    tool.initialize(commName, wave, inst.get("scope", ""), inst.get("ip", None), inst.get("port", None), inst.get(
                        "proto", None), lvl, commArgs, dated="None", datef="None", scanner_ip="None", notes="Arguments: "+commArgs)
                    tool.addInDb()
                    if tool is None:
                        print("Tool already existing.")
                        return
                    self.appli.scanManager.monitor.launchTask(
                        mongoInstance.calendarName, tool, parser, False, worker)

    def onTreeviewSelect(self, event=None):
        """Called when a line is selected on the treeview
        Open the selected object view on the view frame.
        Args:
            _event: not used but mandatory
        """
        selection = self.selection()
        if len(selection) == 1:
            item = super().onTreeviewSelect(event)
            if isinstance(item, str):
                mongoInstance = MongoCalendar.getInstance()
                self.saveState(mongoInstance.calendarName)
                if str(item) == "waves":
                    objView = WaveView(self, self.appli.viewframe,
                                    self.appli, WaveController(Wave()))
                    objView.openInsertWindow()
                elif str(item) == "ips":
                    objView = MultipleIpView(
                        self, self.appli.viewframe, self.appli, IpController(Ip()))
                    objView.openInsertWindow()
                elif "intervals" in str(item):
                    wave = Wave.fetchObject(
                        {"_id": ObjectId(IntervalView.treeviewListIdToDb(item))})
                    objView = IntervalView(self, self.appli.viewframe, self.appli, IntervalController(
                        Interval().initialize(wave.wave)))
                    objView.openInsertWindow()
                elif "scopes" in str(item):
                    wave = Wave.fetchObject(
                        {"_id": ObjectId(ScopeView.treeviewListIdToDb(item))})
                    objView = MultipleScopeView(
                        self, self.appli.viewframe, self.appli, ScopeController(Scope().initialize(wave.wave)))
                    objView.openInsertWindow()
            else:
                self.openModifyWindowOf(item)
        elif len(selection) > 1:
            # Multi select:
            multiView = MultiSelectionView(self, self.appli.viewframe, self.appli)
            for widget in self.appli.viewframe.winfo_children():
                widget.destroy()
            multiView.form.clear()
            multiView.openModifyWindow()

    def load(self, searchModel=None):
        """
        Load the treeview with database information
        Args:
            searchModel: (DEPRECATED) a search object default to None
        """
        for widget in self.appli.viewframe.winfo_children():
            widget.destroy()
        # Reattach hidden as get_children won't get them otherwise
        hidden = sorted(self._hidden, key=lambda x: len(x[0]))
        for hide in hidden:
            try:
                self.reattach(hide[0], hide[1], 0)
            except tk.TclError:
                pass
        # Clear the tree
        mongoInstance = MongoCalendar.getInstance()
        self.heading("#0", text=mongoInstance.calendarName)
        self.delete(*self.get_children())
        self._hidden = []
        if searchModel is None:
            self._load()
        elif searchModel.query == "":
            self._load()
        else:
            viewsFound = searchModel.getViews(
                self, self.appli.viewframe, self.appli)
            for viewFound in viewsFound:
                viewFound.addInTreeview('', False)
        self.loadState(mongoInstance.calendarName)

    def refresh(self):
        """Alias to load function"""
        self.load()

    def _load(self):
        """
        Load the treeview with database information
        """
        mongoInstance = MongoCalendar.getInstance()
        dialog = ChildDialogProgress(self.appli, "Loading "+str(
            mongoInstance.calendarName), "Opening "+str(mongoInstance.calendarName) + ". Please wait for a few seconds.", 200, "determinate")
        step = 0
        dialog.show(100)
        nbObjects = mongoInstance.find("waves").count()
        nbObjects += mongoInstance.find("scopes").count()
        nbObjects += mongoInstance.find("intervals").count()
        nbObjects += mongoInstance.find("scopes").count()
        nbObjects += mongoInstance.find("ips").count()
        nbObjects += mongoInstance.find("ports").count()
        nbObjects += mongoInstance.find("tools").count()
        onePercentNbObject = nbObjects//100 if nbObjects > 100 else 1
        nbObjectTreated = 0
        for child in self.get_children():
            self.delete(child)
        self._hidden = []
        self._detached = []
        self.waves_node = self.insert("", "end", str(
            "waves"), text="Waves", image=WaveView.getClassIcon())
        # Loading every category separatly is faster than recursivly.
        # This is due to cursor.next function calls in pymongo
        # Adding wave objects
        waves = Wave.fetchObjects({})
        for wave in waves:
            wave_o = WaveController(wave)
            wave_vw = WaveView(self, self.appli.viewframe, self.appli, wave_o)
            wave_vw.addInTreeview(self.waves_node, False)
            nbObjectTreated += 1
            if nbObjectTreated % onePercentNbObject == 0:
                step += 1
                dialog.update(step)
        scopes = Scope.fetchObjects({})
        for scope in scopes:
            scope_o = ScopeController(scope)
            scope_vw = ScopeView(self, self.appli.viewframe, self.appli, scope_o)
            scope_vw.addInTreeview(None, False)
            nbObjectTreated += 1
            if nbObjectTreated % onePercentNbObject == 0:
                step += 1
                dialog.update(step)
        intervals = Interval.fetchObjects({})
        for interval in intervals:
            interval_o = IntervalController(interval)
            interval_vw = IntervalView(self, self.appli.viewframe, self.appli, interval_o)
            interval_vw.addInTreeview(None, False)
            nbObjectTreated += 1
            if nbObjectTreated % onePercentNbObject == 0:
                step += 1
                dialog.update(step)
        # Adding ip objects
        self.ips_node = self.insert("", "end", str(
            "ips"), text="IPs", image=IpView.getClassIcon())
        ips = Ip.fetchObjects({})
        for ip in ips:
            ip_o = IpController(ip)
            ip_vw = IpView(self, self.appli.viewframe, self.appli, ip_o)
            ip_vw.addInTreeview(None, False)
            self.appli.statusbar.notify(ip_vw.controller.getTags())
            nbObjectTreated += 1
            if nbObjectTreated % onePercentNbObject == 0:
                step += 1
                dialog.update(step)
        # Adding port objects
        ports = Port.fetchObjects({})
        for port in ports:
            port_o = PortController(port)
            port_vw = PortView(self, self.appli.viewframe, self.appli, port_o)
            port_vw.addInTreeview(None, False)
            self.appli.statusbar.notify(port_vw.controller.getTags())
            nbObjectTreated += 1
            if nbObjectTreated % onePercentNbObject == 0:
                step += 1
                dialog.update(step)
        # Adding defect objects
        defects = Defect.fetchObjects({"ip":{"$ne":""}})
        for defect in defects:
            defect_o = DefectController(defect)
            defect_vw = DefectView(
                self, self.appli.viewframe, self.appli, defect_o)
            defect_vw.addInTreeview(None)
            nbObjectTreated += 1
            if nbObjectTreated % onePercentNbObject == 0:
                step += 1
                dialog.update(step)
        # Adding tool objects
        tools = Tool.fetchObjects({})
        for tool in tools:
            tool_o = ToolController(tool)
            tool_vw = ToolView(self, self.appli.viewframe, self.appli, tool_o)
            tool_vw.addInTreeview(None, False)
            self.appli.statusbar.notify(tool_vw.controller.getTags())
            nbObjectTreated += 1
            if nbObjectTreated % onePercentNbObject == 0:
                step += 1
                dialog.update(step)
        self.sort(self.ips_node)
        self.appli.statusbar.update()
        dialog.destroy()

    def openModifyWindowOf(self, dbId):
        """
        Retrieve the View of the database id given and open the modifying form for its model.
        Args:
            dbId: the Mongo Id to open the modification form on.
        """
        # self.resetTags()
        objView = self.getViewFromId(str(dbId))
        if objView is not None:
            for widget in self.appli.viewframe.winfo_children():
                widget.destroy()
            objView.form.clear()
            self.openedViewFrameId = str(dbId)
            objView.openModifyWindow()

    def unhide(self, node=None):
        """Unhide children of given node.
        Args:
            - node: the node which we want to unhide the children.
                    If this value is None, use the contextualMenu.selection value
                    Default to None.
        """
        nodeToUnhideChildren = str(
            self.contextualMenu.selection) if node is None else node
        hidden = sorted(self._hidden, key=lambda x: len(x[0]))
        for hidden in self._hidden:
            itemId = hidden[0]
            parentId = '' if hidden[1] is None else hidden[1]
            if str(parentId) == str(nodeToUnhideChildren):
                view_o = self.getViewFromId(str(itemId))
                if view_o is not None:
                    view_o.controller.delTag("hidden")
                try:
                    self.reattach(itemId, parentId, 0)
                except tk.TclError:
                    pass # Le noeud a ete supprime entre temps

    def hideAndUpdate(self):
        """Hide object with contextualMenu attached in the treeview and store this effect in its tags."""
        self.hide(None, True)

    def hideSelection(self, _event=None):
        """ Hide selected objects in the treeview and store this effect in their tags."""
        selectedNodes = self.selection()
        for node in selectedNodes:
            self.hide(node, True)

    def hide(self, node=None, updateTags=False):
        """Hide given node object in the treeview and can store this effect in its tag.
        Args:
            - node: node to hide. If none is given, the contextualMenu.selection value will be used.
                    Default to None.
            - updateTags: mark the object as hidden in its tags. Default to False
        """
        nodeToHide = str(
            self.contextualMenu.selection) if node is None else node
        view_o = self.getViewFromId(nodeToHide)
        if view_o is not None:
            if updateTags:
                view_o.controller.addTag("hidden")
            self._hidden.append([nodeToHide, view_o.getParent()])
            self.detach(nodeToHide)
