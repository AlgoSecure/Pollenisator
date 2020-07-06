"""
Module to add defects and export them
"""
import tkinter.ttk as ttk
import tkinter as tk
import tkinter.messagebox
import os
from os import listdir
from os.path import isfile, join
from bson.objectid import ObjectId
from datetime import datetime
from core.Components.mongo import MongoCalendar
import core.Reporting.WordExport as WordExport
import core.Reporting.PowerpointExport as PowerpointExport
import core.Reporting.ExcelExport as ExcelExport
from core.Models.Defect import Defect
from core.Application.Dialogs.ChildDialogCombo import ChildDialogCombo
from core.Application.Dialogs.ChildDialogProgress import ChildDialogProgress
from core.Application.Dialogs.ChildDialogQuestion import ChildDialogQuestion
from core.Application.Dialogs.ChildDialogDefectView import ChildDialogDefectView
from core.Forms.FormHelper import FormHelper

class Report:
    """
    Store elements to report and create docx or xlsx with them
    """
    iconName = "tab_report.png"
    tabName = "   Report   "

    def __init__(self, parent, settings):

        """
        Constructor
        """
        self.dir_path = os.path.dirname(os.path.realpath(__file__))
        self.dir_path = os.path.normpath(os.path.join(self.dir_path, "../../../Templates/"))
        self.default_ppt = os.path.join(self.dir_path, "Modele.pptx")
        self.default_word = os.path.join(self.dir_path, "Modele.docx")
        self.mainRedac = "N/A"
        self.settings = settings
        self.dragging = None
        self.parent = None
        self.reportFrame = None
        self.rowHeight = 0
        self.pane_base_height = 31
        self.style = None
        self.treevw = None
        self.ent_client = None
        self.ent_contract = None
        self.val_word = None
        self.entry_word = None
        self.val_ppt = None
        self.entry_ppt = None
        return

    def open(self):
        self.refreshUI()
        return True

    @classmethod
    def getEases(cls):
        """
        Returns: 
            Returns a list of ease of exploitation levels for a security defect.
        """
        return ["Facile", "Modérée", "Difficile", "Très difficile", "N/A"]

    @classmethod
    def getImpacts(cls):
        """
        Returns: 
            Returns a list of impact levels for a security defect.
        """
        return ["Critique", "Majeur", "Important", "Mineur", "N/A"]

    @classmethod
    def getRisks(cls):
        """
        Returns: 
            Returns a list of risk levels for a security defect.
        """
        return ["Critique", "Majeur", "Important", "Mineur", "N/A"]

    @classmethod
    def getTypes(cls):
        """
        Returns: 
            Returns a list of type for a security defect.
        """
        return ["Socle", "Application", "Politique", "Active Directory", "Infrastructure", "Données"]

    def refreshUI(self):
        """
        Reload informations and reload them into the widgets
        """
        self.default_word = os.path.join(self.dir_path, "Modele.docx")
        self.settings.reloadSettings()
        pentest_type = self.settings.getPentestType().lower()
        models = [f for f in listdir(
            self.dir_path) if isfile(join(self.dir_path, f)) and f.endswith(".docx") and pentest_type in f.lower()]
        if models:
            self.default_word = join(self.dir_path, models[0])
        self.val_word.set(self.default_word)

    def initUI(self, parent, nbk, treevw):
        """
        Initialize window and widgets.
        """
        if self.parent is not None:  # Already initialized
            self.reset()
            self.fillWithDefects()
            return
        self.parent = parent
        ### MAIN PAGE FRAME ###
        self.reportFrame = ttk.Frame(parent)
        self.paned = tk.PanedWindow(self.reportFrame, orient=tk.VERTICAL, height=800)
        ### DEFECT TABLE ###
        self.rowHeight = 20
        self.style = ttk.Style()
        self.style.configure('Report.Treeview', rowheight=self.rowHeight)
        self.frameTw = ttk.Frame(self.paned)
        self.treevw = ttk.Treeview(self.frameTw, style='Report.Treeview', height=0)
        self.treevw['columns'] = ('ease', 'impact', 'risk', 'type', 'redactor')
        self.treevw.heading("#0", text='Title', anchor=tk.W)
        self.treevw.column("#0", anchor=tk.W, width=150)
        self.treevw.heading('ease', text='Ease')
        self.treevw.column('ease', anchor='center', width=40)
        self.treevw.heading('impact', text='Impact')
        self.treevw.column('impact', anchor='center', width=40)
        self.treevw.heading('risk', text='Risk')
        self.treevw.column('risk', anchor='center', width=40)
        self.treevw.heading('type', text='Type')
        self.treevw.column('type', anchor='center', width=10)
        self.treevw.heading('redactor', text='Redactor')
        self.treevw.column('redactor', anchor='center', width=20)
        self.treevw.tag_configure(
            "Critique", background="black", foreground="white")
        self.treevw.tag_configure(
            "Majeur", background="red", foreground="white")
        self.treevw.tag_configure(
            "Important", background="orange", foreground="white")
        self.treevw.tag_configure(
            "Mineur", background="yellow", foreground="black")
        self.treevw.bind("<Double-Button-1>", self.OnDoubleClick)
        self.treevw.bind("<Alt-Up>", self.moveItemUp)
        self.treevw.bind("<Alt-Down>", self.moveItemDown)
        self.treevw.bind("<Delete>", self.deleteSelectedItem)
        self.treevw.grid(row=0, column=0, sticky=tk.NSEW)
        scbVSel = ttk.Scrollbar(self.frameTw,
                                orient=tk.VERTICAL,
                                command=self.treevw.yview)
        self.treevw.configure(yscrollcommand=scbVSel.set)
        scbVSel.grid(row=0, column=1, sticky=tk.NS)
        self.frameTw.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)
        self.frameTw.columnconfigure(0, weight=1)
        self.frameTw.rowconfigure(0, weight=1)
        ### OFFICE EXPORT FRAME ###
        belowFrame = ttk.Frame(self.paned)
        frameBtn = ttk.Frame(belowFrame)
        #lbl_help = FormHelper("DefectHelper", "Use del to delete a defect, use Alt+Arrows to order them")
        #lbl_help.constructView(frameBtn)
        btn_addDefect = ttk.Button(
            frameBtn, text="Add a security defect", command=self.addDefectCallback)
        btn_addDefect.pack(side=tk.RIGHT)
        btn_setMainRedactor = ttk.Button(
            frameBtn, text="Set main redactor", command=self.setMainRedactor)
        btn_setMainRedactor.pack(side=tk.RIGHT)
        frameBtn.pack(side=tk.TOP)
        officeFrame = ttk.LabelFrame(belowFrame, text=" Office reports ")
        ### INFORMATION EXPORT FRAME ###
        informations_frame = ttk.Frame(officeFrame)
        lbl_client = ttk.Label(informations_frame, text="Client's name :")
        lbl_client.grid(row=0, column=0, sticky=tk.E)
        self.ent_client = ttk.Entry(informations_frame, width=50)
        self.ent_client.grid(row=0, column=1, sticky=tk.W)
        lbl_contract = ttk.Label(informations_frame, text="Contract's name :")
        lbl_contract.grid(row=1, column=0, sticky=tk.E)
        self.ent_contract = ttk.Entry(informations_frame, width=50)
        self.ent_contract.grid(row=1, column=1, sticky=tk.W)
        informations_frame.pack(side=tk.TOP, pady=10)
        ### WORD EXPORT FRAME ###
        wordFrame = ttk.Frame(officeFrame)
        lbl = ttk.Label(
            wordFrame, text="Choose a word template : ", background="white")
        lbl.pack(side=tk.LEFT)
        self.val_word = tk.StringVar()
        self.entry_word = tk.Entry(
            wordFrame, textvariable=self.val_word, width=50)
        self.entry_word.bind("<Control-a>", self.selectAll)
        self.entry_word.pack(side=tk.LEFT, padx=10)
        self.val_word.set(self.default_word)
        search_btn = ttk.Button(wordFrame, text="...",
                                command=self.on_click, width=5)
        search_btn.pack(side=tk.LEFT, padx=10)
        btn_word = ttk.Button(
            wordFrame, text="Generate Word report", command=self.generateReportWord, width=30)
        btn_word.pack(side=tk.RIGHT, padx=10)
        wordFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        ### POWERPOINT EXPORT FRAME ###
        powerpointFrame = ttk.Frame(officeFrame)
        lbl = ttk.Label(powerpointFrame,
                        text="Choose a pptx template : ", background="white")
        lbl.pack(side=tk.LEFT)
        self.val_ppt = tk.StringVar()
        self.entry_ppt = tk.Entry(
            powerpointFrame, textvariable=self.val_ppt, width=50)
        self.entry_ppt.bind("<Control-a>", self.selectAll)
        self.entry_ppt.pack(side=tk.LEFT, padx=10)
        self.val_ppt.set(self.default_ppt)
        search_btn = ttk.Button(
            powerpointFrame, text="...", command=self.on_click_pptx, width=5)
        search_btn.pack(side=tk.LEFT, padx=10)
        btn_ppt = ttk.Button(
            powerpointFrame, text="Generate Powerpoint report", command=self.generateReportPowerpoint, width=30)
        btn_ppt.pack(side=tk.RIGHT, padx=10)
        powerpointFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        #### EXCEL EXPORT FRAME ###
        excelFrame = ttk.Frame(officeFrame)
        btn_excel = ttk.Button(
            excelFrame, text="Generate Excel report", command=self.generateReportExcel, width=30)
        btn_excel.pack(side=tk.RIGHT, padx=10)
        excelFrame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        officeFrame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)
        self.paned.add(self.frameTw)
        self.paned.add(belowFrame)
        self.paned.pack(fill=tk.BOTH, expand=1)
        self.reportFrame.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)
        self.fillWithDefects()

    def reset(self):
        """
        reset defect treeview by deleting every item inside.
        """
        for item in self.treevw.get_children():
            self.treevw.delete(item)

    def deleteSelectedItem(self, _event=None):
        """
        Remove selected defect from treeview
        Args:
            _event: not used but mandatory
        """
        selected = self.treevw.selection()[0]
        self.removeItem(selected)

    def removeItem(self, toDeleteIid):
        """
        Remove defect from given iid in defect treeview
        Args:
            toDeleteIid: database ID of defect to delete
        """
        item = self.treevw.item(toDeleteIid)
        dialog = ChildDialogQuestion(self.parent,
                                     "DELETE WARNING", "Are you sure you want to delete defect "+str(item["text"])+" ?", ["Delete", "Cancel"])
        self.parent.wait_window(dialog.app)
        if dialog.rvalue != "Delete":
            return
        self.treevw.delete(toDeleteIid)
        defectToDelete = Defect.fetchObject({"title": item["text"], "ip":"", "port":"", "proto":""})
        if defectToDelete is not None:
            if defectToDelete.index is not None:
                index = int(defectToDelete.index)
                children = self.treevw.get_children()
                for i in range(index+1,len(children),1):
                    d_o = Defect({"_id":children[i]})
                    d_o.update({"index":str(i)})
            defectToDelete.delete()
            self.resizeDefectTreeview()

    def moveItemUp(self, _event=None):
        """
        Swap the selected treeview item with the one up above it.
        Args:
            _event: not used but mandatory
        Returns:
            returns "break" to stop the interrupt the event thus preventing cursor to move up
        """
        selected = self.treevw.selection()[0]
        currentIndice = 0
        children = self.treevw.get_children()
        for i, child in enumerate(children):
            if child == selected:
                currentIndice = i
                break
        if currentIndice != 0:
            self.treevw.move(selected, '', currentIndice-1)
            mongoInstance = MongoCalendar.getInstance()
            selected = children[currentIndice]
            moved_by_side_effect = children[currentIndice-1]
            mongoInstance.update(Defect.coll_name,
                             {"_id": ObjectId(selected)}, {"$set": {"index":str(currentIndice-1)}})
            mongoInstance.update(Defect.coll_name,
                             {"_id": ObjectId(moved_by_side_effect)}, {"$set": {"index":str(currentIndice)}})
        return "break"

    def moveItemDown(self, _event=None):
        """
        Swap the selected treeview item with the one down below it.
        Args:
            _event: not used but mandatory
        Returns:
            returns "break" to stop the interrupt the event thus preventing cursor to move down
        """
        selected = self.treevw.selection()[0]
        len_max = len(self.treevw.get_children())
        currentIndice = len_max-1
        children = self.treevw.get_children()
        for i, child in enumerate(children):
            if child == selected:
                currentIndice = i
                break
        if currentIndice < len_max-1:
            self.treevw.move(selected, '', currentIndice+1)
            mongoInstance = MongoCalendar.getInstance()
            selected = children[currentIndice]
            moved_by_side_effect = children[currentIndice+1]
            mongoInstance.update(Defect.coll_name,
                             {"_id": ObjectId(selected)}, {"$set": {"index":str(currentIndice+1)}})
            mongoInstance.update(Defect.coll_name,
                             {"_id": ObjectId(moved_by_side_effect)}, {"$set": {"index":str(currentIndice)}})
        return "break"

    def on_click(self, _event=None):
        """
        Callback for selecting word template.
        Open a filedialog window and sets the entry value to the selected file
        Args:
            _event: not used but mandatory
        """
        ftypes = [
            ('Word files', '*.docx'),
            ('All files', '*'),
        ]
        f = tkinter.filedialog.askopenfilename(
            initialdir=self.dir_path, title="Select template for report", defaultextension=".docx", filetypes=ftypes)
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        filename = str(f)
        if filename == "()":
            return
        self.val_word.set(filename)

    def on_click_pptx(self, _event=None):
        """
        Callback for selecting powerpoint template.
        Open a filedialog window and sets the entry value to the selected file
        Args:
            _event: not used but mandatory
        """
        ftypes = [
            ('Powerpoint files', '*.pptx'),
            ('All files', '*'),
        ]
        f = tkinter.filedialog.askopenfilename(
            initialdir=self.dir_path, title="Select template for report", defaultextension=".pptx", filetypes=ftypes)
        if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
            return
        filename = str(f)
        if filename == "()":
            return
        self.val_ppt.set(filename)

    def selectAll(self, _event):
        """
        Select all text in an entry
        Args:
            _event: not used but mandatory
        Returns:
            returns "break" to stop the interrupt the event thus preventing the shortcut key to be written
        """
        # select text
        self.entry_word.select_range(0, 'end')
        # move cursor to the end
        self.entry_word.icursor('end')
        return "break"

    def addDefectCallback(self):
        """Open an insert defect view form in a child window"""
        dialog = ChildDialogDefectView(self.parent, self.settings)
        self.parent.wait_window(dialog.app)

    def setMainRedactor(self):
        """Sets a main redactor for a pentest. Each not assigned defect will be assigned to him/her"""
        self.settings.reloadSettings()
        dialog = ChildDialogCombo(self.parent, self.settings.getPentesters()+["N/A"], "Set main redactor", "N/A")
        newVal = self.parent.wait_window(dialog.app)
        if newVal is None:
            return
        if not newVal or newVal.strip() == "":
            return
        columnRedactor = self.treevw['columns'].index("redactor")
        for it in self.treevw.get_children():
            oldValues = self.treevw.item(it)["values"]
            if oldValues[columnRedactor] == "N/A":
                oldValues[columnRedactor] = newVal
                self.treevw.item(it, values=oldValues)
                d_o = Defect({"_id":it})
                d_o.update({"redactor":newVal})
        self.mainRedac = newVal

    def updateDefectInTreevw(self, defect_m, redactor=None):
        """
        Change values of a selected defect in the treeview
        Args:
            defect_m: a defect model with updated values
            redactor: a redactor name for this defect, can be None (default)
        """
        columnEase = self.treevw['columns'].index("ease")
        columnImpact = self.treevw['columns'].index("impact")
        columnRisk = self.treevw['columns'].index("risk")
        columnType = self.treevw['columns'].index("type")
        columnRedactor = self.treevw['columns'].index("redactor")
        oldValues = self.treevw.item(defect_m.getId())["values"]
        oldRisk = oldValues[columnRisk]
        newRisk = defect_m.risk
        newValues = [""]*5
        newValues[columnEase] = defect_m.ease
        newValues[columnImpact] = defect_m.impact
        newValues[columnRisk] = defect_m.risk
        newValues[columnType] = ", ".join(defect_m.mtype)
        newValues[columnRedactor] = defect_m.redactor
        self.treevw.item(defect_m.getId(), text=defect_m.title,
                         tags=(newRisk), values=newValues)
        if oldRisk != newRisk:
            self.treevw.move(defect_m.getId(), '',
                             self.findInsertIndex(defect_m))

    def OnDoubleClick(self, event):
        """
        Callback for double click on treeview.
        Opens a window to update the double clicked defect view.
        Args:
            event: automatically created with the event catch. stores data about line in treeview that was double clicked.
        """
        item = self.treevw.identify("item", event.x, event.y)
        defect_m = Defect.fetchObject({"_id": ObjectId(item)})
        dialog = ChildDialogDefectView(self.parent, self.settings, defect_m)
        self.parent.wait_window(dialog.app)
        self.updateDefectInTreevw(defect_m)

    def fillWithDefects(self):
        """
        Fetch defects that are global (not assigned to an ip) and fill the defect table with them.
        """
        defects = Defect.fetchObjects({"ip":""})
        d_list = {}
        end_defect = []
        for defect in defects:
            if defect.index is None:
                end_defect.append(defect)
            elif str(defect.index) == "end":
                end_defect.append(defect)
            else:
                ind = int(defect.index)
                if ind not in d_list:
                    d_list[ind] = defect
                else:
                    new_ind = ind + 1
                    while new_ind in d_list:
                        new_ind += 1
                    d_list[new_ind] = defect
                    defect.index = new_ind
                    defect.update({"index":str(new_ind)})
        # Fix dict order to index between 0 and *
        keys_ordered = sorted(list(d_list.keys()))
        for i in range(len(keys_ordered)):
            self.addDefect(d_list[keys_ordered[i]])
        for defect in end_defect:
            self.addDefect(defect)

    def findInsertIndex(self, defect_o):
        """
        Find the inserting position for the given defect (treeview is sorted by risk)
        Args:
            defect_o: a Models.Defect object to be inserted in treeview
        Returns:
            the string "end" to insert at the end of the treeview
            an integer between 0 and the nb of lines-1 otherwise
        """
        children = self.treevw.get_children()
        order = Report.getRisks()
        columnRisk = self.treevw['columns'].index("risk")
        for i in range(len(children)):
            if str(defect_o.getId()) != str(children[i]):
                cursorRisk = self.treevw.item(
                    children[i])["values"][columnRisk]
                if order.index(defect_o.risk) <= order.index(cursorRisk):
                    return i
        return "end"

    def addDefect(self, defect_o):
        """
        Add the given defect object in the treeview
        Args:
            defect_o: a Models.Defect object to be inserted in treeview
        """
        if defect_o is None:
            return
        children = self.treevw.get_children()
        if defect_o.index is None or str(defect_o.index) == "":
            indToInsert = self.findInsertIndex(defect_o)
            if str(indToInsert) != "end":
                for i in range(int(indToInsert), len(children), 1):
                    d_o = Defect({"_id":children[i]})
                    d_o.update({"index":str(i+1)})
        else:
            indToInsert = defect_o.index
        types = defect_o.mtype
        types = ", ".join(defect_o.mtype)
        new_values = (defect_o.ease, defect_o.impact,
                      defect_o.risk, types, defect_o.redactor if defect_o.redactor != "N/A" else self.mainRedac)
        already_inserted = False
        already_inserted_iid = None
        for child in children:
            title = self.treevw.item(child)["text"]
            if title == defect_o.title:
                already_inserted = True
                already_inserted_iid = child
                break
        if not already_inserted:
            try:
                self.treevw.insert('', indToInsert, defect_o.getId(), text=defect_o.title,
                                   values=new_values,
                                   tags=(defect_o.risk))
                defect_o.update({"index":str(indToInsert)})
            except tk.TclError:
                # The defect already exists
                already_inserted = True
                already_inserted_iid = defect_o.getId()
        if already_inserted:
            existing = self.treevw.item(already_inserted_iid)
            values = existing["values"]
            if values[4].strip() == "N/A":
                values[4] = defect_o.redactor
            elif defect_o.redactor not in values[4].split(", "):
                values[4] += ", "+defect_o.redactor
            self.treevw.item(already_inserted_iid, values=values)
        # mongoInstance.insert("defects_table",{""})
        self.resizeDefectTreeview()
    
    def resizeDefectTreeview(self):
        currentHeight = len(self.treevw.get_children())
        if currentHeight <= 15:
            self.treevw.config(height=currentHeight)
            sx, sy = self.paned.sash_coord(0)
            if sy <= (currentHeight)*self.rowHeight + self.pane_base_height:
                self.paned.paneconfigure(self.frameTw, height=(currentHeight)*self.rowHeight + self.pane_base_height)

    def getDefectsAsDict(self):
        """
        Returns a dictionnary with treeview defects stored inside
        Returns:
            The returned dict will be formed this way (shown as json):
            {
                "Risk level describer 1":{
                    "defect title 1": {
                        "description":{
                            "title": "defect title 1",
                            "risk": "Risk level 1",
                            "ease": "Ease of exploitation 1",
                            "impact": "Impact 1",
                            "redactor": "Redactor name",
                            "type": ['D', 'T', ...]
                        },
                        "defects_ids":[
                            id 1,
                            id 2...
                        ]
                    },
                    "defect title 2":{
                        ...
                    }
                    ...
                },
                "Risk level describer 2":{
                    ...
                }
                ...
            }
        """
        defects_dict = dict()
        defects_dict["Critique"] = dict()
        defects_dict["Majeur"] = dict()
        defects_dict["Important"] = dict()
        defects_dict["Mineur"] = dict()
        columnEase = self.treevw['columns'].index("ease")
        columnImpact = self.treevw['columns'].index("impact")
        columnType = self.treevw['columns'].index("type")
        columnRisk = self.treevw['columns'].index("risk")
        columnRedactor = self.treevw['columns'].index("redactor")
        for children_id in self.treevw.get_children():
            children = self.treevw.item(children_id)
            title = children["text"]
            defect_recap = dict()
            defect_recap["title"] = title
            defect_recap["risk"] = children["values"][columnRisk]
            defect_recap["ease"] = children["values"][columnEase]
            defect_recap["impact"] = children["values"][columnImpact]
            defect_recap["redactor"] = children["values"][columnRedactor]
            types = children["values"][columnType].split(",")
            d_types = []
            for d_type in types:
                d_types.append(d_type.strip())
            defect_recap["type"] = d_types
            defects_dict[defect_recap["risk"]][title] = dict()
            defects_dict[defect_recap["risk"]
                         ][title]["description"] = defect_recap
            defects_dict[defect_recap["risk"]][title]["defects_ids"] = []
            defects = Defect.fetchObjects({"title": title})
            for defect in defects:
                defects_dict[defect_recap["risk"]
                             ][title]["defects_ids"].append(defect.getId())
        return defects_dict

    def generateReportWord(self):
        """
        Export a calendar defects to a word formatted file.
        """
        if self.ent_client.get().strip() == "":
            tk.messagebox.showerror(
                "Missing required field", "The client's name input must be filled.")
            return
        if self.ent_contract.get().strip() == "":
            tk.messagebox.showerror(
                "Missing required field", "The contract's name input must be filled.")
            return
        mongoInstance = MongoCalendar.getInstance()
        toExport = mongoInstance.calendarName
        if toExport != "":
            modele_docx = str(self.val_word.get())
            timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
            basename = self.ent_client.get().strip() + " - "+self.ent_contract.get().strip()
            out_name = str(timestr)+" - "+basename
            dialog = ChildDialogProgress(
                self.parent, "Word Report", "Creating report "+str(out_name) + ". Please wait.", 200, "determinate")
            WordExport.createReport(self.getDefectsAsDict(), modele_docx, out_name, main_redactor=self.mainRedac,
                                    client=self.ent_client.get().strip(), contract=self.ent_contract.get().strip(), root=self.parent, progressbar=dialog)
            dialog.destroy()
            tkinter.messagebox.showinfo(
                "Success", "The document was generated in ./exports/"+str(out_name))

    def generateReportPowerpoint(self):
        """
        Export a calendar defects to a pptx formatted file.
        """
        if self.ent_client.get().strip() == "":
            tk.messagebox.showerror(
                "Missing required field", "The client's name input must be filled.")
            return
        if self.ent_contract.get().strip() == "":
            tk.messagebox.showerror(
                "Missing required field", "The contract's name input must be filled.")
            return
        mongoInstance = MongoCalendar.getInstance()
        toExport = mongoInstance.calendarName
        if toExport != "":
            modele_pptx = str(self.val_ppt.get())
            timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
            basename = self.ent_client.get().strip() + " - "+self.ent_contract.get().strip()
            out_name = str(timestr)+" - "+basename
            dialog = ChildDialogProgress(
                self.parent, "Powerpoint Report", "Creating report "+str(out_name) + ". Please wait.", 200, progress_mode="determinate")
            PowerpointExport.createReport(self.getDefectsAsDict(), modele_pptx, out_name, client=self.ent_client.get(
            ).strip(), contract=self.ent_contract.get().strip(), root=self.parent, progressbar=dialog)
            dialog.destroy()
            tkinter.messagebox.showinfo(
                "Success", "The document was generated in ./exports/"+str(out_name))

    def generateReportExcel(self):
        """
        Export a calendar status to an excel file.
        """
        mongoInstance = MongoCalendar.getInstance()
        toExport = mongoInstance.calendarName
        if toExport != "":
            timestr = datetime.now().strftime("%Y%m%d-%H%M%S")
            out_name = toExport+"_"+str(timestr)+".xlsx"
            ExcelExport.exportExcel(self.getDefectsAsDict(), out_name)
            tkinter.messagebox.showinfo(
                "Success", "The document was generated in ./exports/"+str(out_name))
