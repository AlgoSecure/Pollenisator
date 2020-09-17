"""
Pollenisator client GUI window.
"""
import traceback
import threading
import tkinter.filedialog
import tkinter as tk
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.ttk as ttk
import sys
from tkinter import TclError
import os
import re
from PIL import ImageTk, Image
import importlib
import pkgutil
import core.Components.Utils as Utils
from core.Application.Treeviews.CalendarTreeview import CalendarTreeview
from core.Application.Treeviews.CommandsTreeview import CommandsTreeview
from core.Application.Dialogs.ChildDialogCombo import ChildDialogCombo
from core.Application.Dialogs.ChildDialogQuestion import ChildDialogQuestion
from core.Application.Dialogs.ChildDialogConnect import ChildDialogConnect
from core.Application.Dialogs.ChildDialogNewCalendar import ChildDialogNewCalendar
from core.Application.Dialogs.ChildDialogException import ChildDialogException
from core.Application.Dialogs.ChildDialogInfo import ChildDialogInfo
from core.Application.StatusBar import StatusBar
from core.Components.mongo import MongoCalendar
from core.Components.ScanManager import ScanManager
from core.Components.Settings import Settings
from core.Components.Filter import Filter
from core.Controllers.ScopeController import ScopeController
from core.Models.Command import Command
from core.Models.Scope import Scope
from core.Models.Wave import Wave
from core.Models.Interval import Interval
from core.Components.FileStorage import FileStorage
import core.Components.Modules


class FloatingHelpWindow(tk.Toplevel):
    """floating basic window with helping text inside
    Inherit tkinter TopLevel
    Found on the internet (stackoverflow) but did not keep link sorry...
    """

    def __init__(self, w, h, posx, posy, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.title('Help: search')
        self.x = posx
        self.y = posy
        self.geometry(str(w)+"x"+str(h)+"+"+str(posx)+"+"+str(posy))
        self.resizable(0, 0)
        self.config(bg='light yellow')
        self.grip = tk.Label(self, bitmap="gray25")
        self.grip.pack(side="left", fill="y")
        label = tk.Label(self, bg='light yellow', fg='black',
                         justify=tk.LEFT, text=Filter.help())
        label.pack()
        self.overrideredirect(True)
        self.grip.bind("<ButtonPress-1>", self.startMove)
        self.grip.bind("<ButtonRelease-1>", self.stopMove)
        self.grip.bind("<B1-Motion>", self.onMotion)

    def startMove(self, event):
        """ Floating window dragging started
            Args:
                event: event.x and event.y hold the new position of the window
        """
        self.x = event.x
        self.y = event.y

    def stopMove(self, _event):
        """ Floating window dragging stopped
            Args:
                _event: Not used but mandatory
        """
        self.x = None
        self.y = None

    def onMotion(self, event):
        """ Floating window dragging ongoing
            Args:
                event: event.x and event.y hold the new position of the window
        """
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))


class AutocompleteEntry(ttk.Entry):
    """Inherit ttk.Entry.
    An entry with an autocompletion ability.
    Found on the internet : http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
    But a bit modified.
    """

    def __init__(self, settings, *args, **kwargs):
        """Constructor
        Args:
            settings: a dict of Settings:
                * histo_filters: number of history search to display
            args: not used
            kwargs: 
                * width: default to 100
        """
        ttk.Entry.__init__(self, *args, **kwargs)
        self.width = kwargs.get("width",100)
        self.lista = set()
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()
        self.var.trace('w', self.changed)
        
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.upArrow)
        self.bind("<Down>", self.downArrow)
        self.settings = settings
        self.lb = None
        self.lb_up = False

    def changed(self, _name=None, _index=None, _mode=None):
        """
        Called when the entry is modified. Perform autocompletion.
        Args:
            _name: not used but mandatory for tk.StringVar.trace
            _index: not used but mandatory for tk.StringVar.trace
            _mode: not used but mandatory for tk.StringVar.trace
        """
        words = self.comparison()
        if words:
            if not self.lb_up:
                self.lb = tk.Listbox(width=self.width)
                self.lb.bind("<Double-Button-1>", self.selection)
                self.lb.bind("<Right>", self.selection)
                self.lb.bind("<Leave>", self.quit)
                self.bind("<Escape>", self.quit)
                self.lb.place(x=self.winfo_x()+133,
                                y=self.winfo_y()+self.winfo_height()+20)
                self.lb_up = True
            self.lb.delete(0, tk.END)
            for w in words:
                self.lb.insert(tk.END, w)
        else:
            self.quit()

    def quit(self, _event=None):
        """
        Callback function to destroy the label shown
        Args:
            _event: not used but mandatory
        """
        if self.lb_up:
            self.lb.destroy()
            self.lb_up = False
    
    def reset(self):
        """
        quit and reset filter bar
        """
        self.quit()
        self.var.set("")

    def selection(self, _event):
        """
        Called when an autocompletion option is chosen. 
        Change entry content and close autocomplete.
        Args:
            _event: not used but mandatory
        """
        if self.lb_up:
            self.var.set(self.lb.get(tk.ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)
            #self.changed()

    def upArrow(self, _event):
        """
        Called when the up arrow is pressed. Navigate in autocompletion options
        Args:
            _event: not used but mandatory
        """
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def downArrow(self, _event):
        """
        Called when the down arrow is pressed. Navigate in autocompletion options
        Args:
            _event: not used but mandatory
        """
        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != tk.END:
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        """
        Search suggestions in regard of what is in the entry
        """
        values = set(self.settings.local_settings.get("histo_filters", []))
        self.lista = values
        content = self.var.get().strip()
        if content == "":
            return []
        pattern = re.compile('.*' + re.escape(content) + '.*')
        return [w for w in self.lista if re.match(pattern, w)]

def iter_namespace(ns_pkg):
    # Specifying the second argument (prefix) to iter_modules makes the
    # returned name an absolute name instead of a relative one. This allows
    # import_module to work without having to do additional modification to
    # the name.
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

class Appli(ttk.Frame):
    """
    Main tkinter graphical application object.
    """

    def __init__(self, parent):
        """
        Initialise the application

        Args:
            parent: The main tk window.
        """
        # Lexic:
        # view frame : the frame in the tab that will hold forms.
        # Tree view : the tree on the left of the window.
        # frame tree view : a frame around the tree view (useful to attach a scrollbar to a treeview)
        # canvas : a canvas object (useful to attach a scrollbar to a frame)
        # paned : a Paned widget is used to separate two other widgets and display a one over the other if desired
        #           Used to separate the treeview frame and view frame.
        
        self.parent = parent  #  parent tkinter window
        #  already read notifications from previous notification reading iteration
        self.old_notifs = []
        self.notifications_timers = None
        tk.Tk.report_callback_exception = self.show_error
        self.setStyle()
        # HISTORY : Main view and command where historically in the same view;
        # This results in lots of widget here with a confusing naming style
        ttk.Frame.__init__(self, parent)
        #### core components (Tab menu on the left objects)####
        self.settings = Settings()
        self.settingViewFrame = None
        self.scanManager = None  #  Loaded when clicking on it if linux only
        self.scanViewFrame = None
        self.main_tab_img = ImageTk.PhotoImage(
            Image.open(Utils.getIconDir()+"tab_main.png"))
        self.commands_tab_img = ImageTk.PhotoImage(
            Image.open(Utils.getIconDir()+"tab_commands.png"))
        self.scan_tab_img = ImageTk.PhotoImage(
            Image.open(Utils.getIconDir()+"tab_scan.png"))
        self.settings_tab_img = ImageTk.PhotoImage(
            Image.open(Utils.getIconDir()+"tab_settings.png"))
        self.initModules()

        #### MAIN VIEW ####
        self.openedViewFrameId = None
        self.mainPageFrame = None
        self.paned = None
        self.canvasMain = None
        self.viewframe = None
        self.frameTw = None
        self.treevw = None
        self.myscrollbarMain = None
        #### COMMAND VIEW ####
        self.commandsPageFrame = None
        self.commandPaned = None
        self.commandsFrameTw = None
        self.canvas = None
        self.commandsViewFrame = None
        self.myscrollbarCommand = None
        self.commandsTreevw = None
        #### SEARCH BAR ####
        # boolean set to true when the main tree view is displaying search results
        self.searchMode = False
        self.searchBar = None  # the search bar component
        self.btnHelp = None  # help button on the right of the search bar
        self.photo = None  # the ? image
        self.helpFrame = None  # the floating help frame poping when the button is pressed

        # Connect to database and choose database to open
        abandon = False
        mongoInstance = MongoCalendar.getInstance()
        while not mongoInstance.isUserConnected() and not abandon:
            abandon = self.promptForConnection() is None
        if not abandon:
            mongoInstance.attach(self)
            self.initUI()
            # Will trigger promptForCalendarOpen when tab will be opened
        else:
            self.onClosing()
            try:
                parent.destroy()
            except tk.TclError:
                pass
    
    def initModules(self):
        discovered_plugins = {
            name: importlib.import_module(name)
            for finder, name, ispkg
            in iter_namespace(core.Components.Modules)
        }
        self.modules = []
        for name, module in discovered_plugins.items():
            module_class = getattr(module, name.split(".")[-1])
            module_obj = module_class(self.parent, self.settings)
            self.modules.append({"name": module_obj.tabName, "object":module_obj, "view":None, "img":ImageTk.PhotoImage(Image.open(Utils.getIconDir()+module_obj.iconName))})

    def show_error(self, *args):
        """Callback for tk.Tk.report_callback_exception.
        Open a window to display exception with some actions possible

        Args:
            args: 3 args are required for tk.Tk.report_callback_exception event to be given to traceback.format_exception(args[0], args[1], args[2])
        
        Raises:
            If an exception occurs in this handler thread, will print it and exit with exit code 1
        """
        try:
            err = traceback.format_exception(args[0], args[1], args[2])
            dialog = ChildDialogException(self, 'Exception occured', err)
            try:
                self.wait_window(dialog.app)
            except tk.TclError:
                sys.exit(1)
        except Exception as e:
            print(e)
            sys.exit(1)

    def promptForConnection(self):
        """Close current database connection and open connection form for the user
        
        Returns: 
            The number of pollenisator database found, 0 if the connection failed."""
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.reinitConnection()
        connectDialog = ChildDialogConnect(self.parent)
        self.wait_window(connectDialog.app)
        return connectDialog.rvalue

    def getCentralizedFiles(self):
        """Download from SFTP server all files of current database in local directory
        """
        fs = FileStorage()
        fs.open()
        fs.getResults()
        fs.close()
        tkinter.messagebox.showinfo(
            "Centralization completed", "Files were download in results/")

    def submitIssue(self):
        """Open git issues in browser"""
        import webbrowser
        webbrowser.open_new_tab("https://github.com/AlgoSecure/Pollenisator/issues")

    def removeFiles(self, calendarName):
        """Open git issues in browser
        Args:
            calendarName: database name to be removed.
        """
        fs = FileStorage()
        fs.open()
        fs.rmDbResults(calendarName.strip())
        fs.rmDbProofs(calendarName.strip())
        fs.close()
        tkinter.messagebox.showinfo(
            "Deleting tool", "Files were removed on sftp for "+str(calendarName))

    def readNotifications(self):
        """
        Read notifications from database every 0.5 or so second. Notifications are used to exchange informations between applications.
        """
        mongoInstance = MongoCalendar.getInstance()
        for old_notif in self.old_notifs:
            mongoInstance.deleteFromDb("pollenisator", "notifications", {"_id": old_notif})
        self.old_notifs = []
        try:
            notifications = mongoInstance.findInDb("pollenisator", "notifications", {"$or":[{"db":str(mongoInstance.calendarName)}, {"db":"pollenisator"}]})
            for notification in notifications:
                # print("Notification received "+str(notification["db"])+"/"+str(notification["collection"])+" iid="+str(notification["iid"])+" action="+str(notification["action"]))
                self.old_notifs.append(notification["_id"])
                if notification["db"] == "pollenisator":
                    if notification["collection"] == "workers":
                        self.scanManager.notify(notification["iid"], notification["action"])
                    elif "commands" in notification["collection"]:
                        self.commandsTreevw.notify(notification["db"], notification["collection"], notification["iid"], notification["action"], notification.get("parent", ""))
                else:
                    self.treevw.notify(notification["db"], notification["collection"],
                                    notification["iid"], notification["action"], notification.get("parent", ""))
                    for module in self.modules:
                        if callable(getattr(module["object"], "notify", None)):
                            module["object"].notify(notification["db"], notification["collection"],
                                    notification["iid"], notification["action"], notification.get("parent", ""))
        except Exception as e:
            print(str(e))
        self.notifications_timers = threading.Timer(
            0.5, self.readNotifications)
        self.notifications_timers.start()

    def onClosing(self):
        """
        Close the application properly.
        """
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.dettach(self)
        if self.scanManager is not None:
            self.scanManager.stop()
        print("Stopping notifications...")
        if self.notifications_timers is not None:
            self.notifications_timers.cancel()
        if self.scanManager is not None:
            self.scanManager.monitor.stopWorkersTimer()
        print("Stopping application...")
        self.quit()

    def _initMenuBar(self):
        """
        Create the bar menu on top of the screen.
        """
        menubar = tk.Menu(self.parent, tearoff=0, bd=0, background='#73B723', foreground='white', activebackground='#73B723', activeforeground='white')
        self.parent.config(menu=menubar)

        self.parent.bind('<F5>', self.refreshView)
        self.parent.bind('<Control-o>', self.promptCalendarName)
        fileMenu = tk.Menu(menubar, tearoff=0, background='#73B723', foreground='white', activebackground='#73B723', activeforeground='white')
        fileMenu.add_command(label="New", command=self.selectNewCalendar)
        fileMenu.add_command(label="Open (Ctrl+o)",
                             command=self.promptCalendarName)
        fileMenu.add_command(label="Connect to server", command=self.promptForConnection)
        fileMenu.add_command(label="Copy", command=self.wrapCopyDb)
        fileMenu.add_command(label="Delete a database",
                             command=self.deleteACalendar)
        fileMenu.add_command(label="Export database",
                             command=self.exportCalendar)
        fileMenu.add_command(label="Import database",
                             command=self.importCalendar)
        fileMenu.add_command(label="Export commands",
                             command=self.exportCommands)
        fileMenu.add_command(label="Import commands",
                             command=self.importCommands)

        fileMenu.add_command(label="Exit", command=self.onExit)
        fileMenu2 = tk.Menu(menubar, tearoff=0, background='#73B723', foreground='white', activebackground='#73B723', activeforeground='white')
        fileMenu2.add_command(label="Reset unfinished tools",
                              command=self.resetUnfinishedTools)
        fileMenu2.add_command(label="Refresh (F5)",
                              command=self.refreshView)
        fileMenu2.add_command(label="Get centralized files",
                              command=self.getCentralizedFiles)
        fileMenu3 = tk.Menu(menubar, tearoff=0, background='#73B723', foreground='white', activebackground='#73B723', activeforeground='white')
        fileMenu3.add_command(label="Submit a bug or feature",
                              command=self.submitIssue)
        menubar.add_cascade(label="File", menu=fileMenu)
        menubar.add_cascade(label="Scans", menu=fileMenu2)
        menubar.add_cascade(label="Help", menu=fileMenu3)

    def setStyle(self, _event=None):
        """
        Set the pollenisator window widget style using ttk.Style
        Args:
            _event: not used but mandatory
        """
        style = ttk.Style(self.parent)
        style.theme_use("clam")
        try:
            style.element_create('Plain.Notebook.tab', "from", 'default')
        except TclError:
            pass # ALready exists
        style.configure("Treeview.Heading", background="#73B723",
                        foreground="white", relief="flat")
        style.map('Treeview.Heading', background=[('active', '#73B723')])
        style.configure("TLabelframe", background="white",
                        labeloutside=False, bordercolor="#73B723")
        style.configure('TLabelframe.Label', background="#73B723",
                        foreground="white", font=('Sans', '10', 'bold'))
        style.configure("TProgressbar",
                        background="#73D723", foreground="#73D723", troughcolor="white", darkcolor="#73D723", lightcolor="#73D723")
        style.configure("Important.TFrame", background="#73B723")
        style.configure("TFrame", background="white")
        style.configure("Important.TLabel", background="#73B723", foreground="white")
        style.configure("TLabel", background="white")
        style.configure("TCombobox", background="white")
        style.configure("TCheckbutton", background="white",
                        font=('Sans', '10', 'bold'))
        style.configure("TButton", background="#73B723",
                        foreground="white", font=('Sans', '10', 'bold'), borderwidth=1)
        style.configure("TNotebook", background="#73B723", foreground="white", font=(
            'Sans', '10', 'bold'), tabposition='wn', borderwidth=0, width=100)

        style.configure("TNotebook.Tab", background="#73B723", borderwidth=0,
                        foreground="white", font=('Sans', '10', 'bold'), padding=20, bordercolor="#73B723")
        style.map('TNotebook.Tab', background=[('active', '#73C723'), ("selected", '#73D723')], foreground=[("active", "white")], font=[("active", (
            'Sans', '10', 'bold'))], padding=[('active', 20)])
        style.map('TButton', background=[('active', '#73D723')])
        #  FIX tkinter tag_configure not showing colors   https://bugs.python.org/issue36468
        style.map('Treeview', foreground=Appli.fixedMap('foreground', style),
                  background=Appli.fixedMap('background', style))
        # Removed dashed line https://stackoverflow.com/questions/23354303/removing-ttk-notebook-tab-dashed-line/23399786
        style.layout("TNotebook.Tab",
                     [('Plain.Notebook.tab',
                       {'children':[('Notebook.padding', {'side': 'top', 'children': [('Notebook.label', {
                           'side': 'top', 'sticky': ''})], 'sticky': 'nswe'})],
                        'sticky': 'nswe'})])

    @staticmethod
    def fixedMap(option, style):
        """
        Fix color tag in treeview not appearing under some linux distros
        Args:
            option: the string option you want to affect on treeview ("background" for example)
            strle: the style object of ttk
        """
        # Fix for setting text colour for Tkinter 8.6.9
        # From: https://core.tcl.tk/tk/info/509cafafae
        #  FIX tkinter tag_configure not showing colors   https://bugs.python.org/issue36468
        # Returns the style map for 'option' with any styles starting with
        # ('!disabled', '!selected', ...) filtered out.

        # style.map() returns an empty list for missing options, so this
        # should be future-safe.
        return [elm for elm in style.map('Treeview', query_opt=option) if
                elm[:2] != ('!disabled', '!selected')]


    def initMainView(self):
        """
        Fill the main view tab menu
        """
        self.mainPageFrame = ttk.Frame(self.nbk)
        searchFrame = ttk.Frame(self.mainPageFrame)
        lblSearch = ttk.Label(searchFrame, text="Filter bar:")
        lblSearch.pack(side="left", fill=tk.NONE)
        self.searchBar = AutocompleteEntry(self.settings, searchFrame)
        #self.searchBar = ttk.Entry(searchFrame, width=108)
        self.searchBar.bind('<Return>', self.newSearch)
        self.searchBar.bind('<KP_Enter>', self.newSearch)
        self.searchBar.bind('<Control-a>', self.searchbarSelectAll)
        # searchBar.bind("<Button-3>", self.do_popup)
        self.searchBar.pack(side="left", fill="x", expand=True)
        btnSearchBar = ttk.Button(searchFrame, text="Search", command=self.newSearch)
        btnSearchBar.pack(side="left", fill="x")
        btnReset = ttk.Button(searchFrame, text="Reset",command=self.resetButtonClicked)
        btnReset.pack(side="left", fill="x")
        self.btnHelp = ttk.Button(searchFrame)
        self.photo = tk.PhotoImage(file=Utils.getHelpIconPath())
        self.helpFrame = None
        self.btnHelp.config(image=self.photo, command=self.showSearchHelp)
        self.btnHelp.pack(side="left")
        searchFrame.pack(side="top", fill="x")
        #PANED PART
        self.paned = tk.PanedWindow(self.mainPageFrame, height=800)
        #RIGHT PANE : Canvas + frame
        self.canvasMain = tk.Canvas(self.paned, bg="white")
        self.viewframe = ttk.Frame(self.canvasMain)
        #LEFT PANE : Treeview
        self.frameTw = ttk.Frame(self.paned)
        self.treevw = CalendarTreeview(self, self.frameTw)
        self.treevw.initUI()
        scbVSel = ttk.Scrollbar(self.frameTw,
                                orient=tk.VERTICAL,
                                command=self.treevw.yview)
        self.treevw.configure(yscrollcommand=scbVSel.set)
        self.treevw.grid(row=0, column=0, sticky=tk.NSEW)
        scbVSel.grid(row=0, column=1, sticky=tk.NS)
        self.paned.add(self.frameTw)
        self.myscrollbarMain = tk.Scrollbar(self.paned, orient="vertical", command=self.canvasMain.yview)
        self.myscrollbarMain.pack(side="right", fill=tk.BOTH)
        self.canvasMain.bind('<Enter>', self.boundToMousewheelMain)
        self.canvasMain.bind('<Leave>', self.unboundToMousewheelMain)
        self.canvasMain.pack(side="left")
        self.canvasMain.bind('<Configure>', self.resizeCanvasMainFrame)
        self.canvas_main_frame = self.canvasMain.create_window((0, 0), window=self.viewframe, anchor='nw')
        self.viewframe.bind("<Configure>", self.scrollFrameMainFunc)
        self.canvasMain.configure(yscrollcommand=self.myscrollbarMain.set)
        self.paned.add(self.canvasMain)
        self.paned.pack(fill=tk.BOTH, expand=1)
        self.frameTw.rowconfigure(0, weight=1) # Weight 1 sur un layout grid, sans ça le composant ne changera pas de taille en cas de resize
        self.frameTw.columnconfigure(0, weight=1) # Weight 1 sur un layout grid, sans ça le composant ne changera pas de taille en cas de resize
        self.nbk.add(self.mainPageFrame, text="Main View ", image=self.main_tab_img, compound=tk.TOP, sticky='nsew')
    
    def searchbarSelectAll(self, _event):
        """
        Callback to select all the text in searchbar
        Args:
            _event: not used but mandatory
        """
        self.searchBar.select_range(0, 'end')
        self.searchBar.icursor('end')
        return "break"

    def boundToMousewheel(self, _event):
        """Called when the **command canvas** is on focus.
        Bind the command scrollbar button on linux to the command canvas
        Args:
            _event: not used but mandatory
        """
        self.canvas.bind_all("<Button-4>", self._onMousewheelCommand)
        self.canvas.bind_all("<Button-5>", self._onMousewheelCommand)

    def unboundToMousewheel(self, _event):
        """Called when the **command canvas** is unfocused.
        Unbind the command scrollbar button on linux to the command canvas
        Args:
            _event: not used but mandatory"""
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def boundToMousewheelMain(self, _event):
        """Called when the **main view canvas** is focused.
        Bind the main view scrollbar button on linux to the main view canvas
        Args:
            _event: not used but mandatory"""
        self.canvas.bind_all("<Button-4>", self._onMousewheelMain)
        self.canvas.bind_all("<Button-5>", self._onMousewheelMain)

    def unboundToMousewheelMain(self, _event):
        """Called when the **main view canvas** is unfocused.
        Unbind the main view scrollbar button on linux to the main view canvas
        Args:
            _event: not used but mandatory"""
        self.canvasMain.unbind_all("<Button-4>")
        self.canvasMain.unbind_all("<Button-5>")

    def _onMousewheelMain(self, event):
        """Called when a scroll occurs. boundToMousewheelMain must be called first.
        Performs the scroll on the main canvas.
        Args:
            event: Holds info on scroll within event.delta and event.num"""
        if event.num == 5 or event.delta == -120:
            count = 1
        if event.num == 4 or event.delta == 120:
            count = -1
        self.canvasMain.yview_scroll(count, "units")

    def _onMousewheelCommand(self, event):
        """Called when a scroll occurs. boundToMousewheel must be called first.
        Performs the scroll on the command canvas.
        Args:
            event: Holds info on scroll within event.delta and event.num"""
        if event.num == 5 or event.delta == -120:
            count = 1
        if event.num == 4 or event.delta == 120:
            count = -1
        self.canvas.yview_scroll(count, "units")

    def scrollFrameMainFunc(self, _event):
        """make the main canvas scrollable"""
        self.canvasMain.configure(scrollregion=self.canvasMain.bbox("all"), width=20, height=200)

    def scrollFrameFunc(self, _event):
        """make the command canvas scrollable"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"), width=20, height=200)

    def initCommandsView(self):
        """Populate the command tab menu view frame with cool widgets"""
        self.commandsPageFrame = ttk.Frame(self.nbk)
        self.commandPaned = tk.PanedWindow(self.commandsPageFrame, height=800)
        self.commandsFrameTw = ttk.Frame(self.commandPaned)
        self.canvas = tk.Canvas(self.commandPaned, bg="white")
        self.commandsFrameTw.pack(expand=True)
        self.commandsViewFrame = ttk.Frame(self.canvas)
        self.myscrollbarCommand = tk.Scrollbar(self.commandPaned, orient="vertical", command=self.canvas.yview)
        self.myscrollbarCommand.pack(side="right", fill=tk.BOTH)
        self.canvas.bind('<Enter>', self.boundToMousewheel)
        self.canvas.bind('<Leave>', self.unboundToMousewheel)
        self.canvas.bind('<Configure>', self.resizeCanvasFrame)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_frame = self.canvas.create_window((0, 0), window=self.commandsViewFrame, anchor='nw')
        self.commandsViewFrame.bind("<Configure>", self.scrollFrameFunc)
        self.canvas.configure(yscrollcommand=self.myscrollbarCommand.set)
        self.commandsTreevw = CommandsTreeview(self, self.commandsFrameTw)
        scbVSel = ttk.Scrollbar(self.commandsFrameTw,
                                orient=tk.VERTICAL,
                                command=self.commandsTreevw.yview)
        self.commandsTreevw.configure(yscrollcommand=scbVSel.set)
        self.commandsTreevw.grid(row=0, column=0, sticky=tk.NSEW)
        scbVSel.grid(row=0, column=1, sticky=tk.NS)
        self.commandPaned.add(self.commandsFrameTw)
        self.commandPaned.add(self.canvas)
        self.commandPaned.pack(fill=tk.BOTH, expand=1)
        self.commandsFrameTw.rowconfigure(0, weight=1) # Weight 1 sur un layout grid, sans ça le composant ne changera pas de taille en cas de resize
        self.commandsFrameTw.columnconfigure(0, weight=1) # Weight 1 sur un layout grid, sans ça le composant ne changera pas de taille en cas de resize
        self.nbk.bind("<<NotebookTabChanged>>", self.tabSwitch)
        self.nbk.add(self.commandsPageFrame, text="Commands", image=self.commands_tab_img, compound=tk.TOP)

    def resizeCanvasFrame(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)
    
    def resizeCanvasMainFrame(self, event):
        canvas_width = event.width
        self.canvasMain.itemconfig(self.canvas_main_frame, width=canvas_width)


    def showSearchHelp(self, _event=None):
        """Called when the searchbar help button is clicked. Display a floating help window with examples
        Args:
            _event: not used but mandatory
        """
        if self.helpFrame is None:
            x, y = self.btnHelp.winfo_rootx(), self.btnHelp.winfo_rooty()
            self.helpFrame = FloatingHelpWindow(410, 400, x-380, y+40, self)
        else:
            self.helpFrame.destroy()
            self.helpFrame = None

    def tabSwitch(self, event):
        """Called when the user click on the tab menu to switch tab. Add a behaviour before the tab switches.
        Args:
            event : hold informations to identify which tab was clicked.
        """
        tabName = self.nbk.tab(self.nbk.select(), "text").strip()
        self.searchBar.quit()
        if tabName == "Commands":
            self.commandsTreevw.initUI()
        mongoInstance = MongoCalendar.getInstance()
        if not mongoInstance.hasACalendarOpen():
            opened = self.promptCalendarName()
            if opened is None:
                return
        if tabName == "Scan":
            if mongoInstance.calendarName is not None:
                if mongoInstance.calendarName != "":
                    if os.name != 'nt': # Disable on windows
                        # if self.scanManager is None:
                        #    self.scanManager = ScanManager(mongoInstance.calendarName, self.settings)
                        self.scanManager.initUI(self.scanViewFrame)
                    else:
                        lbl = ttk.Label(self.scanViewFrame, text="Disabled on windows because celery does not support it.")
                        lbl.pack()
        elif tabName == "Settings":
            self.settings.reloadUI()
        else:
            for module in self.modules:
                if tabName.strip().lower() == module["name"].strip().lower():
                    module["object"].open()
        event.widget.winfo_children()[event.widget.index("current")].update()

    def initSettingsView(self):
        """Add the settings view frame to the notebook widget and initialize its UI."""
        self.settingViewFrame = ttk.Frame(self.nbk)
        self.settings.initUI(self.settingViewFrame)
        self.settingViewFrame.pack(fill=tk.BOTH, expand=1)
        self.nbk.add(self.settingViewFrame, text="  Settings  ", image=self.settings_tab_img, compound=tk.TOP)

    def initScanView(self):
        """Add the scan view frame to the notebook widget. This does not initialize it as it needs a database to be opened."""
        self.scanViewFrame = ttk.Frame(self.nbk)
        self.nbk.add(self.scanViewFrame, text="    Scan     ", image=self.scan_tab_img, compound=tk.TOP)

    def initUI(self):
        """
        initialize all the main windows objects. (Bar Menu, contextual menu, treeview, editing pane)
        """
        self.nbk = ttk.Notebook(self.parent)
        self.statusbar = StatusBar(self.parent, Settings.getTags(), self)
        self.statusbar.pack(fill=tk.X)
        self.nbk.enable_traversal()
        self.initMainView()
        self.initCommandsView()
        self.initScanView()
        self.initSettingsView()
        for module in self.modules:
            module["view"] = ttk.Frame(self.nbk)
            self.nbk.add(module["view"], text=module["name"],image=module["img"],compound=tk.TOP)
        self._initMenuBar()
        self.nbk.pack(fill=tk.BOTH, expand=1)

    def newSearch(self, _event=None):
        """Called when the searchbar is validated (click on search button or enter key pressed).
        Perform a filter on the main treeview.
        Args:
            _event: not used but mandatory"""
        filterStr = self.searchBar.get()
        self.settings.reloadSettings()
        success = self.treevw.filterTreeview(filterStr, self.settings)
        self.searchMode = (success and filterStr.strip() != "")
        if success:
            histo_filters = self.settings.local_settings.get("histo_filters", [])
            if filterStr.strip() != "":
                histo_filters.insert(0, filterStr)
                if len(histo_filters) > 10:
                    histo_filters = histo_filters[:10]
                self.settings.local_settings["histo_filters"] = histo_filters
                self.settings.saveLocalSettings()
            if self.helpFrame is not None:
                self.helpFrame.destroy()
                self.helpFrame = None

    def statusbarClicked(self, name):
        """Called when a button in the statusbar tag is clicked.
        filter the treeview to match the status bar tag clicked and enforce select of main view
        Args:
            name: not used but mandatory"""
        # get the index of the mouse click
        self.nbk.select(0)
        self.searchMode = True
        self.treevw.filterTreeview("\""+name+"\" in tags")

    def resetButtonClicked(self):
        """
        Called when the reset button of the status bar is clicked.
        """
        self.searchMode = False
        self.searchBar.reset()
        self.treevw.unfilter()

    def refreshView(self, _event=None):
        """
        Reload the currently opened tab
        Args:
            _event: not used but mandatory
        """
        setViewOn = None
        nbkOpenedTab = self.nbk.tab(self.nbk.select(), "text").strip()
        activeTw = None
        if nbkOpenedTab == "Main View":
            activeTw = self.treevw
        elif nbkOpenedTab == "Commands":
            activeTw = self.commandsTreevw
        elif nbkOpenedTab == "Scan":
            self.scanManager.initUI(self.scanViewFrame)
        elif nbkOpenedTab == "Settings":
            self.settings.reloadUI()
        else:
            for module in self.modules:
                if nbkOpenedTab.strip().lower() == module["name"].strip().lower():
                    module["object"].open()
        if activeTw is not None:
            if len(activeTw.selection()) == 1:
                setViewOn = activeTw.selection()[0]
            activeTw.refresh()
        if setViewOn is not None:
            try:
                activeTw.see(setViewOn)
                activeTw.focus(setViewOn)
                activeTw.selection_set(setViewOn)
                activeTw.openModifyWindowOf(setViewOn)
            except tk.TclError:
                pass

    def resetUnfinishedTools(self):
        """
        Reset all running tools to a ready state.
        """
        mongoInstance = MongoCalendar.getInstance()
        if mongoInstance.hasACalendarOpen():
            Utils.resetUnfinishedTools()
            self.statusbar.reset()
            self.treevw.load()

    def exportCalendar(self):
        """
        Dump a pentest database to an archive file gunzip.
        """
        mongoInstance = MongoCalendar.getInstance()
        dialog = ChildDialogCombo(self, mongoInstance.listCalendars()[::-1], "Choose a database to dump:")
        self.wait_window(dialog.app)
        if isinstance(dialog.rvalue, str):
            mongoInstance.dumpDb(dialog.rvalue)

    def exportCommands(self):
        """
        Dump pollenisator from database to an archive file gunzip.
        """
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.dumpDb("pollenisator", "commands")
        mongoInstance.dumpDb("pollenisator", "group_commands")
        tkinter.messagebox.showinfo(
            "Export pollenisator database", "Export completed in exports/pollenisator_commands.gzip and exports/pollenisator_group_commands.gzip")

    def importCalendar(self, name=None):
        """
        Import a calendar archive file gunzip to database.
        Args:
            name: The filename of the gunzip database exported previously
        """
        mongoInstance = MongoCalendar.getInstance()
        filename = ""
        if name is None:
            f = tkinter.filedialog.askopenfilename(defaultextension=".gzip")
            if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return
            filename = str(f)
        else:
            filename = name
        mongoInstance.importDatabase(filename)

    def importCommands(self, name=None):
        """
        Import a pollenisator archive file gunzip to database.
        Args:
            name: The filename of the gunzip command table exported previously
        Returns:
            None if name is None and filedialog is closed
            True if commands successfully are imported
            False otherwise.
        """
        filename = ""
        if name is None:
            f = tkinter.filedialog.askopenfilename(defaultextension=".gzip")
            if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return
            filename = str(f)
        else:
            filename = name
        try:
            mongoInstance = MongoCalendar.getInstance()
            mongoInstance.importCommands(filename)
            self.commandsTreevw.refresh()
        except IOError:
            tkinter.messagebox.showerror(
                "Import commands", "Import failed. "+str(filename)+" was not found or is not a file.")
            return False
        tkinter.messagebox.showinfo(
            "Import commands", "Import of "+filename+" completed")
        return True

    def onExit(self):
        """
        Exit the application
        """
        self.onClosing()

    def promptCalendarName(self, _event=None):
        """
        Ask a user to select an pentest database including a New database option.
        Args:
            _event: Not used but mandatory
        Returns:
            None if no database were selected
            datababase name otherwise
        """
        mongoInstance = MongoCalendar.getInstance()
        calendars = mongoInstance.listCalendars()
        if calendars is None:
            calendars = []
        dialog = ChildDialogCombo(self, ["New database"]+calendars[::-1], "Please select a database")
        self.wait_window(dialog.app)
        if dialog.rvalue is None:
            return None
        if isinstance(dialog.rvalue, str):
            if dialog.rvalue == "New database":
                self.selectNewCalendar()
            else:
                self.openCalendar(dialog.rvalue)
            return dialog.rvalue

    def deleteACalendar(self):
        """
        Ask a user a calendar name then delete it.
        """
        mongoInstance = MongoCalendar.getInstance()
        dialog = ChildDialogCombo(
            self, mongoInstance.listCalendars()[::-1], "Choose a database to delete:")
        self.wait_window(dialog.app)
        if isinstance(dialog.rvalue, str):
            calendarName = dialog.rvalue
            ret = tkinter.messagebox.askokcancel(
                "Delete tools on server", "Do you also want to delete resulting tool files on server sftp ?")
            if ret:
                self.removeFiles(calendarName)

            ret = tkinter.messagebox.askokcancel(
                "The document will be deleted", "You are going to delete permanently the database \""+calendarName+"\". Are you sure ?")
            if ret:
                mongoInstance.doDeleteCalendar(calendarName)

            self.treevw.deleteState(calendarName)

    def newCalendar(self, calendarName):
        """
        Register the given calendar name into database and opens it.

        Args:
            calendarName: The pentest database name to register in database.
        """
        succeed = False
        if calendarName is not None:
            mongoInstance = MongoCalendar.getInstance()
            succeed = mongoInstance.registerCalendar(calendarName, True, True)
        return succeed

    def selectNewCalendar(self):
        """
        Ask a user for a new calendar name. Then creates it.
        """
        validCalendar = False
        default = {}
        while not validCalendar:
            dialog = ChildDialogNewCalendar(self.parent, default)
            self.wait_window(dialog.app)
            if isinstance(dialog.rvalue, dict):
                default = dialog.rvalue
                dbName = dialog.rvalue["name"]
                pentest_type = dialog.rvalue["type"]
                start_date = dialog.rvalue["start"]
                end_date = dialog.rvalue["end"]
                scope = dialog.rvalue["scope"]
                settings = dialog.rvalue["settings"]
                pentesters = dialog.rvalue["pentesters"]
                validCalendar = self.newCalendar(dbName)
                if validCalendar:
                    self.openCalendar(dbName)
                    dialog = ChildDialogInfo(
                         self.parent, "New database created", "Database setup ...")
                    dialog.show()
                    self.prepareCalendar(dbName, pentest_type, start_date, end_date, scope, settings, pentesters)
                    dialog.destroy()


            else:
                return
            

    def prepareCalendar(self, dbName, pentest_type, start_date, end_date, scope, settings, pentesters):
        """
        Initiate a pentest database with wizard info
        Args:
            dbName: the database name
            pentest_type: a pentest type choosen from settings pentest_types. Used to select commands that will be launched by default
            start_date: a begining date and time for the pentest
            end_date: ending date and time for the pentest
            scope: a list of scope valid string (IP, network IP or host name)
            settings: a dict of settings with keys:
                * "Add domains whose IP are in scope": if 1, will do a dns lookup on new domains and check if found IP is in scope
                * "Add domains who have a parent domain in scope": if 1, will add a new domain if a parent domain is in scope
                * "Add all domains found":  Unsafe. if 1, all new domains found by tools will be considered in scope.
        """
        commands = Command.getList({"$or":[{"types":{"$elemMatch":{"$eq":pentest_type}}}, {"types":{"$elemMatch":{"$eq":"Commun"}}}]})
        if not commands:
            commandslist = Command.getList()
            if not commandslist:
                dialog = ChildDialogQuestion(self.parent, "No command found", "There is no registered command in the database. Would you like to import the default set?")
                self.parent.wait_window(dialog.app)
                if dialog.rvalue != "Yes":
                    return
                default = os.path.join(Utils.getMainDir(), "exports/pollenisator_commands.gzip")
                res = self.importCommands(default)
                if res:
                    default = os.path.join(Utils.getMainDir(), "exports/pollenisator_group_commands.gzip")
                    res = self.importCommands(default)
        #Duplicate commands in local database
        allcommands = Command.fetchObjects({})
        for command in allcommands:
            command.indb = MongoCalendar.getInstance().calendarName
            command.addInDb()
        Wave().initialize(dbName, commands).addInDb()
        Interval().initialize(dbName, start_date, end_date).addInDb()
        values = {"wave":dbName, "Scopes":scope, "Settings":False}
        ScopeController(Scope()).doInsert(values)
        self.settings.reloadSettings()
        self.settings.db_settings["pentest_type"] = pentest_type
        self.settings.db_settings["include_domains_with_ip_in_scope"] = settings['Add domains whose IP are in scope'] == 1
        self.settings.db_settings["include_domains_with_topdomain_in_scope"] = settings["Add domains who have a parent domain in scope"] == 1
        self.settings.db_settings["include_all_domains"] = settings["Add all domains found"] == 1
        self.settings.db_settings["pentesters"] = list(map(lambda x: x.strip(), pentesters.split("\n")))
        self.settings.save()

    def openCalendar(self, filename=""):
        """
        Open the given database name. Loads it in treeview.

        Args:
            filename: the pentest database name to load in application. If "" is given (default), will refresh the already opened database if there is one.
        """
        print("Start monitoring")
        calendarName = None
        mongoInstance = MongoCalendar.getInstance()
        if filename == "" and mongoInstance.hasACalendarOpen():
            calendarName = mongoInstance.calendarName
        elif filename != "":
            calendarName = filename.split(".")[0].split("/")[-1]
        if calendarName is not None:
            if self.scanManager is not None:
                self.scanManager.stop()
            if self.notifications_timers is not None:
                self.notifications_timers.cancel()
                self.notifications_timers = None
            mongoInstance.connectToDb(calendarName)
            for widget in self.viewframe.winfo_children():
                widget.destroy()
            for module in self.modules:
                module["object"].initUI(module["view"], self.nbk, self.treevw)
            self.statusbar.reset()
            self.treevw.refresh()
            if os.name != "nt": # On windows celery 4.X is not managed
                self.scanManager = ScanManager(self.nbk, self.treevw, mongoInstance.calendarName, self.settings)
                self.notifications_timers = threading.Timer(
                    0.5, self.readNotifications)
                self.notifications_timers.start()

    def wrapCopyDb(self, _event=None):
        """
        Call default copy database from a callback event.

        Args:
            _event: not used but mandatory
        """
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.copyDb()
