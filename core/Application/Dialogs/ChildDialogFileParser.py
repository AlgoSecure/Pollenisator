"""Ask the user to select a file or directory and then parse it with the selected parser"""
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
import io
import os
import hashlib
from core.Components.Utils import listPlugin, loadPlugin
from core.Components.mongo import MongoCalendar
from core.Forms.FormPanel import FormPanel
from core.Views.ViewElement import ViewElement
from core.Models.Wave import Wave
from core.Models.Tool import Tool
from core.Application.Dialogs.ChildDialogProgress import ChildDialogProgress


def md5(fname):
    """Compute md5 hash of the given file name.
    Args:
        fname: path to the file you want to compute the md5 of.
    Return:
        The digested hash of the file in an hexadecimal string format.
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


class ChildDialogFileParser:
    """
    Open a child dialog of a tkinter application to ask details about
    existing files parsing.
    """

    def __init__(self, parent):
        """
        Open a child dialog of a tkinter application to ask details about
        existing files parsing.

        Args:
            parent: the tkinter parent view to use for this window construction.
        """
        self.app = tk.Toplevel(parent)
        self.app.title("Upload result file")
        self.rvalue = None
        self.parent = parent
        appFrame = ttk.Frame(self.app)
        self.form = FormPanel()
        self.form.addFormLabel(
            "Import one file or choose a directory", "", side=tk.TOP)
        self.form.addFormFile("File", ".+", width=50,
                              side=tk.TOP, mode="file|directory")
        self.form.addFormLabel("Plugins", side=tk.TOP)
        self.form.addFormCombo(
            "Plugin", ["auto-detect"]+listPlugin(), "auto-detect", side=tk.TOP)
        self.form.addFormLabel("Wave name", side=tk.TOP)
        wave_list = Wave.listWaves()
        if "Imported files" not in wave_list:
            wave_list.append("Imported files")
        self.form.addFormCombo(
            "Wave", wave_list, "Imported files", side=tk.TOP)
        self.form.addFormButton("Parse", self.onOk, side=tk.TOP)

        self.form.constructView(appFrame)
        appFrame.pack(ipadx=10, ipady=10)

        self.app.transient(parent)
        self.app.grab_set()

    def onOk(self, _event=None):
        """
        Called when the user clicked the validation button.
        launch parsing with selected parser on selected file/directory.
        Close the window.

        Args:
            _event: not used but mandatory
        """
        res, msg = self.form.checkForm()
        if not res:
            tk.messagebox.showwarning(
                "Form not validated", msg, parent=self.app)
            return
        notes = None
        tags = None
        form_values = self.form.getValue()
        form_values_as_dicts = ViewElement.list_tuple_to_dict(form_values)
        file_path = form_values_as_dicts["File"]
        plugin = form_values_as_dicts["Plugin"]
        wave = form_values_as_dicts["Wave"]
        files = []
        if os.path.isdir(file_path):
            # r=root, d=directories, f = files
            for r, _d, f in os.walk(file_path):
                for fil in f:
                    files.append(os.path.join(r, fil))
        else:
            files.append(file_path)
        results = {}
        dialog = ChildDialogProgress(self.parent, "Importing files", "Importing "+str(
            len(files)) + " files. Please wait for a few seconds.", 200, "determinate")
        dialog.show(len(files))
        # LOOP ON FOLDER FILES
        for f_i, file_path in enumerate(files):
            md5File = md5(file_path)
            toolName = os.path.splitext(os.path.basename(file_path))[
                0] + md5File[:6]
            dialog.update(f_i)
            if plugin == "auto-detect":
                # AUTO DETECT
                foundPlugin = "Ignored"
                for pluginName in listPlugin():
                    if foundPlugin != "Ignored":
                        break
                    mod = loadPlugin(pluginName)
                    if mod.autoDetectEnabled():
                        with io.open(file_path, 'r', encoding="utf-8") as f:
                            notes, tags, lvl, targets = mod.Parse(f)
                            if notes is not None and tags is not None:
                                foundPlugin = pluginName
                results[foundPlugin] = results.get(
                    foundPlugin, []) + [file_path]
            else:
                # SET PLUGIN 
                mod = loadPlugin(plugin)
                with io.open(file_path, 'r', encoding="utf-8") as f:
                    notes, tags, lvl, targets = mod.Parse(f)
                    results[plugin] = results.get(
                        plugin, []) + [file_path]
            # IF PLUGIN FOUND SOMETHING
            if notes is not None and tags is not None:
                # ADD THE RESULTING TOOL TO AFFECTED
                for target in targets.values():
                    date = datetime.fromtimestamp(os.path.getmtime(
                        file_path)).strftime("%d/%m/%Y %H:%M:%S")
                    if target is None:
                        scope = None
                        ip = None
                        port = None
                        proto = None
                    else:
                        scope = target.get("scope", None)
                        ip = target.get("ip", None)
                        port = target.get("port", None)
                        proto = target.get("proto", None)
                    Wave().initialize(wave, []).addInDb()
                    tool_m = Tool().initialize(toolName, wave, scope=scope, ip=ip, port=port, proto=proto, lvl=lvl, text="",
                                                dated=date, datef=date, scanner_ip="Imported file", status="done", notes=notes, tags=tags)
                    tool_m.addInDb()
                    mongoInstance = MongoCalendar.getInstance()
                    outputRelDir = tool_m.getOutputDir(
                        mongoInstance.calendarName)
                    abs_path = os.path.dirname(os.path.abspath(__file__))
                    outputDir = os.path.join(
                        abs_path, "../../../results", outputRelDir)
                    mod.centralizeFile(file_path, outputDir)
                    tool_m.update({"resultfile": os.path.join(
                        outputRelDir, os.path.basename(file_path))})
        
        dialog.destroy()
        # DISPLAY RESULTS
        presResults = ""
        filesIgnored = 0
        for key, value in results.items():
            presResults += str(len(value)) + " " + str(key)+".\n"
            if key == "Ignored":
                filesIgnored += 1
        if plugin == "auto-detect":
            if filesIgnored > 0:
                tk.messagebox.showwarning(
                    "Auto-detect ended", presResults, parent=self.app)
            else:
                tk.messagebox.showinfo("Auto-detect ended", presResults, parent=self.app)
        else:
            if filesIgnored > 0:
                tk.messagebox.showwarning(
                    "Parsing ended", presResults, parent=self.app)
            else:
                tk.messagebox.showinfo("Parsing ended", presResults, parent=self.app)

        self.rvalue = None
        self.app.destroy()
