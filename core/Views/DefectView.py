"""View for defect object. Handle node in treeview and present forms to user when interacted with."""

from tkinter import TclError
import tkinter as tk
from core.Views.ViewElement import ViewElement
from core.Models.Defect import Defect
import core.Components.Utils as Utils
from shutil import which
import os
import sys
import subprocess



class DefectView(ViewElement):
    """View for defect object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory.
    """

    icon = 'defect.png'

    def __init__(self, appTw, appViewFrame, mainApp, controller):
        """Constructor
        Args:
            appTw: a PollenisatorTreeview instance to put this view in
            appViewFrame: an view frame to build the forms in.
            mainApp: the Application instance
            controller: a CommandController for this view.
        """
        super().__init__(appTw, appViewFrame, mainApp, controller)
        self.easeForm = None
        self.impactForm = None
        self.riskForm = None

    def openInsertWindow(self, notes="", addButtons=True):
        """
        Creates a tkinter form using Forms classes. This form aims to insert a new Defect
        Args:
            notes: default notes to be written in notes text input. Default is ""
            addButtons: boolean value indicating that insertion buttons should be visible. Default to True
        """
        settings = self.mainApp.settings
        settings.reloadSettings()
        modelData = self.controller.getData()
        topPanel = self.form.addFormPanel(grid=True)
        topPanel.addFormLabel("Title")
        topPanel.addFormStr("Title", r".+", "", column=1, width=50)
        topPanel = self.form.addFormPanel(grid=True)
        topPanel.addFormLabel("Ease")
        self.easeForm = topPanel.addFormCombo(
            "Ease", ['Facile', "Modérée", "Difficile", "Très difficile", "N/A"], column=1, binds={"<<ComboboxSelected>>": self.updateRiskBox})
        topPanel.addFormHelper("0: Trivial to exploit, no tool required\n1: Simple technics and public tools needed to exploit\n2: public vulnerability exploit requiring security skills and/or the development of simple tools.\n3: Use of non-public exploits requiring strong skills in security and/or the development of targeted tools", column=2)
        topPanel.addFormLabel("Impact", row=1)
        self.impactForm = topPanel.addFormCombo(
            "Impact", ["Mineur", "Important", "Majeur", "Critique", "N/A"], row=1, column=1, binds={"<<ComboboxSelected>>": self.updateRiskBox})
        topPanel.addFormHelper("0: No direct impact on system security\n1: Impact isolated on precise locations of pentested system security\n2: Impact restricted to a part of the system security.\n3: Global impact on the pentested system security.", row=1, column=2)
        topPanel.addFormLabel("Risk", row=2)
        self.riskForm = topPanel.addFormCombo(
            "Risk", ["Mineur", "Important", "Majeur", "Critique", "N/A"], modelData["risk"], row=2, column=1)
        topPanel.addFormHelper(
            "0: small risk that might be fixed\n1: moderate risk that need a planed fix\n2: major risk that need to be fixed quickly.\n3: critical risk that need an immediate fix or an immediate interruption.", row=2, column=2)
        topPanel.addFormLabel("Redactor", row=3)
        topPanel.addFormCombo("Redactor", self.mainApp.settings.getPentesters()+["N/A"], "N/A", row=3, column=1)
        chklistPanel = self.form.addFormPanel(grid=True)
        defectTypes = settings.getPentestTypes()
        if defectTypes is not None:
            defectTypes = defectTypes.get(settings.getPentestType(), [])
            if len(defectTypes) == 0:
                defectTypes = ["N/A"]
        else:
            defectTypes = ["N/A"]
        chklistPanel.addFormChecklist("Type", defectTypes, ["N/A"])
        proofsPanel = self.form.addFormPanel(grid=True)
        proofsPanel.addFormFile("Proof", r"")
        notesPanel = self.form.addFormPanel()
        notesPanel.addFormLabel("Notes", side="top")
        notesPanel.addFormText("Notes", r"", notes, None, side="top")
        self.form.addFormHidden("ip", modelData["ip"])
        self.form.addFormHidden("proto", modelData["proto"])
        self.form.addFormHidden("port", modelData["port"])
        if addButtons:
            self.completeInsertWindow()
        else:
            self.showForm()

    def openModifyWindow(self, addButtons=True):
        """
        Creates a tkinter form using Forms classes.
        This form aims to update or delete an existing Defect
        Args:
            addButtons: boolean value indicating that insertion buttons should be visible. Default to True
        """
        modelData = self.controller.getData()
        settings = self.mainApp.settings
        settings.reloadSettings()
        topPanel = self.form.addFormPanel(grid=True)
        row = 0
        if modelData.get("ip", "") != "":
            topPanel.addFormLabel("IP", row=row, column=0)
            topPanel.addFormStr(
                "IP", '', modelData["ip"], None, column=1, row=row, state="readonly")
            row += 1
            if modelData.get("port", "") != "" and modelData["proto"] is not None:
                topPanel.addFormLabel("Port", row=row, column=0)
                port_str = modelData["proto"] + \
                    "/" if modelData["proto"] != "tcp" else ""
                port_str += modelData["port"]
                topPanel.addFormStr(
                    "Port", '', port_str, None, column=1, row=row, state="readonly")
                row += 1
        topPanel.addFormLabel("Title", row=row, column=0)
        topPanel.addFormStr(
            "Title", ".+", modelData["title"], width=50, row=row, column=1)
        row += 1
        topPanel = self.form.addFormPanel(grid=True)
        row = 0
        topPanel.addFormLabel("Ease", row=row)
        self.easeForm = topPanel.addFormCombo(
            "Ease", ['Facile', "Modérée", "Difficile", "Très difficile", "N/A"], modelData["ease"], row=row, column=1, binds={"<<ComboboxSelected>>": self.updateRiskBox})
        topPanel.addFormHelper("0: Trivial to exploit, no tool required\n1: Simple technics and public tools needed to exploit\n2: public vulnerability exploit requiring security skills and/or the development of simple tools.\n3: Use of non-public exploits requiring strong skills in security and/or the development of targeted tools", row=row, column=2)
        row += 1
        topPanel.addFormLabel("Impact", row=row)
        self.impactForm = topPanel.addFormCombo(
            "Impact", ["Mineur", "Important", "Majeur", "Critique", "N/A"], modelData["impact"], row=row, column=1, binds={"<<ComboboxSelected>>": self.updateRiskBox})
        topPanel.addFormHelper("0: No direct impact on system security\n1: Impact isolated on precise locations of pentested system security\n2: Impact restricted to a part of the system security.\n3: Global impact on the pentested system security.", row=row, column=2)
        row += 1
        topPanel.addFormLabel("Risk", row=row)
        self.riskForm = topPanel.addFormCombo(
            "Risk", ["Mineur", "Important", "Majeur", "Critique", "N/A"], modelData["risk"], row=row, column=1)
        topPanel.addFormHelper(
            "0: small risk that might be fixed\n1: moderate risk that need a planed fix\n2: major risk that need to be fixed quickly.\n3: critical risk that need an immediate fix or an immediate interruption.", row=row, column=2)
        row += 1
        chklistPanel = self.form.addFormPanel(grid=True)
        defect_types = settings.getPentestTypes()[settings.getPentestType()]
        for savedType in modelData["type"]:
            if savedType.strip() not in defect_types:
                defect_types.insert(0, savedType)
        chklistPanel.addFormChecklist("Type", defect_types, modelData["type"])
        topPanel.addFormLabel("Redactor", row=row)
        topPanel.addFormCombo("Redactor", list(set(self.mainApp.settings.getPentesters()+["N/A"]+[modelData["redactor"]])), modelData["redactor"], row=row, column=1)
        row += 1
        proofPanel = self.form.addFormPanel(grid=True)
        i = 0
        for proof in modelData["proofs"]:
            proofPanel.addFormLabel("Proof "+str(i), proof, row=i, column=0)
            proofPanel.addFormButton("View", lambda event, obj=i: self.viewProof(
                event, obj), row=i, column=1)
            proofPanel.addFormButton("Delete", lambda event, obj=i: self.deleteProof(
                event, obj), row=i, column=2)
            i += 1
        proofPanel.addFormFile("Proof "+str(i), r"", "", row=i, column=0)
        proofPanel.addFormButton("Upload", lambda event, obj=i: self.addAProof(
            event, obj), row=i, column=1)
        notesPanel = self.form.addFormPanel()
        notesPanel.addFormLabel("Notes", side="top")
        notesPanel.addFormText(
            "Notes", r"", modelData["notes"], None, side="top", height=10)
        if addButtons:
            self.completeModifyWindow()
        else:
            self.showForm()

    def updateRiskBox(self, _event=None):
        """Callback when ease or impact is modified.
        Calculate new resulting risk value
        Args
            _event: mandatory but not used
        """
        ease = self.easeForm.getValue()
        impact = self.impactForm.getValue()
        risk = Defect.getRisk(ease, impact)
        self.riskForm.setValue(risk)

    def viewProof(self, _event, obj):
        """Callback when view proof is clicked.
        Download and display the file using xdg-open on linux or os.startfile (windows)
        Args
            _event: mandatory but not used
            obj: the clicked index proof
        """
        proof_local_path = self.controller.getProof(obj)
        if proof_local_path is not None:
            if os.path.isfile(proof_local_path):
                if which("xdg-open") is not None:
                    subprocess.call(["xdg-open", proof_local_path])
                else:
                    try:
                        os.startfile(proof_local_path)
                    except Exception:
                        tk.messagebox.showerror("Could not open", "Failed to open this file.")
                        proof_local_path = None
                        return
        if proof_local_path is None:
            tk.messagebox.showerror(
                "Download failed", "the file does not exist on sftp server")

    def deleteProof(self, _event, obj):
        """Callback when delete proof is clicked.
        remove remote proof and update window
        Args
            _event: mandatory but not used
            obj: the clicked index proof
        """
        self.controller.deleteProof(obj)
        self.form.clear()
        for widget in self.appliViewFrame.winfo_children():
            widget.destroy()
        self.openModifyWindow()

    def addAProof(self, _event, obj):
        """Callback when add proof is clicked.
        Add proof and update window
        Args
            _event: mandatory but not used
            obj: the clicked index proof
        """
        values = self.form.getValue()
        formValues = ViewElement.list_tuple_to_dict(values)
        self.controller.addAProof(formValues, obj)
        self.form.clear()
        for widget in self.appliViewFrame.winfo_children():
            widget.destroy()
        self.openModifyWindow()

    def beforeDelete(self, iid=None):
        """Called before defect deletion.
        Will attempt to remove this defect from global defect table.
        Args:
            iid: the mongo ID of the deleted defect
        """
        if iid is None:
            if self.controller is not None:
                iid = self.controller.getDbId()
        if iid is not None:
            for module in self.mainApp.modules:
                if callable(getattr(module["object"], "removeItem", None)):
                    module["object"].removeItem(iid)

    def addInTreeview(self, parentNode=None, _addChildren=True):
        """Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            _addChildren: not used here
        """
        if not self.controller.isAssigned():
            # Unassigned defect are loaded on the report tab
            return
        if self.controller.model is None:
            return
        if parentNode is None:
            parentNode = DefectView.DbToTreeviewListId(
                self.controller.getParent())
            nodeText = str(self.controller.getModelRepr())
        elif parentNode == '':
            nodeText = self.controller.getDetailedString()
        else:
            parentNode = DefectView.DbToTreeviewListId(parentNode)
            nodeText = str(self.controller.getModelRepr())
        try:
            parentNode = self.appliTw.insert(
                self.controller.getParent(), 0, parentNode, text="Defects", image=self.getIcon())
        except TclError:
            pass
        self.appliTw.views[str(self.controller.getDbId())] = {"view": self}
        try:
            self.appliTw.insert(parentNode, "end", str(self.controller.getDbId()),
                                text=nodeText, tags=self.controller.getTags(), image=self.getIcon())
        except TclError:
            pass
        if "hidden" in self.controller.getTags():
            self.hide()

    @classmethod
    def DbToTreeviewListId(cls, parent_db_id):
        """Converts a mongo Id to a unique string identifying a list of defects given its parent
        Args:
            parent_db_id: the parent node mongo ID
        Returns:
            A string that should be unique to describe the parent list of defect node
        """
        return str(parent_db_id)+"|Defects"

    @classmethod
    def treeviewListIdToDb(cls, treeviewId):
        """Extract from the unique string identifying a list of defects the parent db ID
        Args:
            treeviewId: the treeview node id of a list of defects node
        Returns:
            the parent object mongo id as string
        """
        return str(treeviewId).split("|")[0]

    def insertReceived(self):
        """Called when a defect insertion is received by notification.
        Insert the node in treeview.
        Also insert it in global report of defect
        """
        if self.controller.model is None:
            return
        if self.controller.isAssigned():
            super().insertReceived()
        else:
            for module in self.mainApp.modules:
                if callable(getattr(module["object"], "addDefect", None)):
                    module["object"].addDefect(self.controller.model)
    
    def updateReceived(self):
        """Called when a defect update is received by notification.
        Update the defect node and the report defect table.
        """
        if self.controller.model is None:
            return
        if not self.controller.isAssigned():
            for module in self.mainApp.modules:
                if callable(getattr(module["object"], "updateDefectInTreeview", None)):
                    module["object"].updateDefectInTreeview(self.controller.model)
        super().updateReceived()