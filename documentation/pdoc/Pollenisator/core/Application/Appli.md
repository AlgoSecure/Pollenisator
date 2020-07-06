Module Pollenisator.core.Application.Appli
==========================================
Pollenisator client GUI window.

Functions
---------

    
`iter_namespace(ns_pkg)`
:   

Classes
-------

`Appli(parent)`
:   Main tkinter graphical application object.
    
    Initialise the application
    
    Args:
        parent: The main tk window.

    ### Ancestors (in MRO)

    * tkinter.ttk.Frame
    * tkinter.ttk.Widget
    * tkinter.Widget
    * tkinter.BaseWidget
    * tkinter.Misc
    * tkinter.Pack
    * tkinter.Place
    * tkinter.Grid

    ### Static methods

    `fixedMap(option, style)`
    :   Fix color tag in treeview not appearing under some linux distros
        Args:
            option: the string option you want to affect on treeview ("background" for example)
            strle: the style object of ttk

    ### Methods

    `boundToMousewheel(self, _event)`
    :   Called when the **command canvas** is on focus.
        Bind the command scrollbar button on linux to the command canvas
        Args:
            _event: not used but mandatory

    `boundToMousewheelMain(self, _event)`
    :   Called when the **main view canvas** is focused.
        Bind the main view scrollbar button on linux to the main view canvas
        Args:
            _event: not used but mandatory

    `deleteACalendar(self)`
    :   Ask a user a calendar name then delete it.

    `exportCalendar(self)`
    :   Dump a pentest database to an archive file gunzip.

    `exportCommands(self)`
    :   Dump pollenisator from database to an archive file gunzip.

    `getCentralizedFiles(self)`
    :   Download from SFTP server all files of current database in local directory

    `importCalendar(self, name=None)`
    :   Import a calendar archive file gunzip to database.
        Args:
            name: The filename of the gunzip database exported previously

    `importCommands(self, name=None)`
    :   Import a pollenisator archive file gunzip to database.
        Args:
            name: The filename of the gunzip command table exported previously
        Returns:
            None if name is None and filedialog is closed
            True if commands successfully are imported
            False otherwise.

    `initCommandsView(self)`
    :   Populate the command tab menu view frame with cool widgets

    `initMainView(self)`
    :   Fill the main view tab menu

    `initModules(self)`
    :

    `initScanView(self)`
    :   Add the scan view frame to the notebook widget. This does not initialize it as it needs a database to be opened.

    `initSettingsView(self)`
    :   Add the settings view frame to the notebook widget and initialize its UI.

    `initUI(self)`
    :   initialize all the main windows objects. (Bar Menu, contextual menu, treeview, editing pane)

    `newCalendar(self, calendarName)`
    :   Register the given calendar name into database and opens it.
        
        Args:
            calendarName: The pentest database name to register in database.

    `newSearch(self)`
    :   Called when the searchbar is validated (click on search button or enter key pressed).
        Perform a filter on the main treeview.
        Args:
            _event: not used but mandatory

    `onClosing(self)`
    :   Close the application properly.

    `onExit(self)`
    :   Exit the application

    `openCalendar(self, filename='')`
    :   Open the given database name. Loads it in treeview.
        
        Args:
            filename: the pentest database name to load in application. If "" is given (default), will refresh the already opened database if there is one.

    `prepareCalendar(self, dbName, pentest_type, start_date, end_date, scope, settings, pentesters)`
    :   Initiate a pentest database with wizard info
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

    `promptCalendarName(self)`
    :   Ask a user to select an pentest database including a New database option.
        Args:
            _event: Not used but mandatory
        Returns:
            None if no database were selected
            datababase name otherwise

    `promptForConnection(self)`
    :   Close current database connection and open connection form for the user
        
        Returns: 
            The number of pollenisator database found, 0 if the connection failed.

    `readNotifications(self)`
    :   Read notifications from database every 0.5 or so second. Notifications are used to exchange informations between applications.

    `refreshView(self)`
    :   Reload the currently opened tab
        Args:
            _event: not used but mandatory

    `removeFiles(self, calendarName)`
    :   Open git issues in browser
        Args:
            calendarName: database name to be removed.

    `resetButtonClicked(self)`
    :   Called when the reset button of the status bar is clicked.

    `resetUnfinishedTools(self)`
    :   Reset all running tools to a ready state.

    `resizeCanvasFrame(self, event)`
    :

    `resizeCanvasMainFrame(self, event)`
    :

    `scrollFrameFunc(self, _event)`
    :   make the command canvas scrollable

    `scrollFrameMainFunc(self, _event)`
    :   make the main canvas scrollable

    `searchbarSelectAll(self, _event)`
    :   Callback to select all the text in searchbar
        Args:
            _event: not used but mandatory

    `selectNewCalendar(self)`
    :   Ask a user for a new calendar name. Then creates it.

    `setStyle(self)`
    :   Set the pollenisator window widget style using ttk.Style
        Args:
            _event: not used but mandatory

    `showSearchHelp(self)`
    :   Called when the searchbar help button is clicked. Display a floating help window with examples
        Args:
            _event: not used but mandatory

    `show_error(self, *args)`
    :   Callback for tk.Tk.report_callback_exception.
        Open a window to display exception with some actions possible
        
        Args:
            args: 3 args are required for tk.Tk.report_callback_exception event to be given to traceback.format_exception(args[0], args[1], args[2])
        
        Raises:
            If an exception occurs in this handler thread, will print it and exit with exit code 1

    `statusbarClicked(self, name)`
    :   Called when a button in the statusbar tag is clicked.
        filter the treeview to match the status bar tag clicked and enforce select of main view
        Args:
            name: not used but mandatory

    `submitIssue(self)`
    :   Open git issues in browser

    `tabSwitch(self, event)`
    :   Called when the user click on the tab menu to switch tab. Add a behaviour before the tab switches.
        Args:
            event : hold informations to identify which tab was clicked.

    `unboundToMousewheel(self, _event)`
    :   Called when the **command canvas** is unfocused.
        Unbind the command scrollbar button on linux to the command canvas
        Args:
            _event: not used but mandatory

    `unboundToMousewheelMain(self, _event)`
    :   Called when the **main view canvas** is unfocused.
        Unbind the main view scrollbar button on linux to the main view canvas
        Args:
            _event: not used but mandatory

    `wrapCopyDb(self)`
    :   Call default copy database from a callback event.
        
        Args:
            _event: not used but mandatory

`AutocompleteEntry(settings, *args, **kwargs)`
:   Inherit ttk.Entry.
    An entry with an autocompletion ability.
    Found on the internet : http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
    But a bit modified.
    
    Constructor
    Args:
        settings: a dict of Settings:
            * histo_filters: number of history search to display
        args: not used
        kwargs: 
            * width: default to 100

    ### Ancestors (in MRO)

    * tkinter.ttk.Entry
    * tkinter.ttk.Widget
    * tkinter.Entry
    * tkinter.Widget
    * tkinter.BaseWidget
    * tkinter.Misc
    * tkinter.Pack
    * tkinter.Place
    * tkinter.Grid
    * tkinter.XView

    ### Methods

    `changed(self)`
    :   Called when the entry is modified. Perform autocompletion.
        Args:
            _name: not used but mandatory for tk.StringVar.trace
            _index: not used but mandatory for tk.StringVar.trace
            _mode: not used but mandatory for tk.StringVar.trace

    `comparison(self)`
    :   Search suggestions in regard of what is in the entry

    `downArrow(self, _event)`
    :   Called when the down arrow is pressed. Navigate in autocompletion options
        Args:
            _event: not used but mandatory

    `quit(self)`
    :   Callback function to destroy the label shown
        Args:
            _event: not used but mandatory

    `reset(self)`
    :   quit and reset filter bar

    `selection(self, _event)`
    :   Called when an autocompletion option is chosen. 
        Change entry content and close autocomplete.
        Args:
            _event: not used but mandatory

    `upArrow(self, _event)`
    :   Called when the up arrow is pressed. Navigate in autocompletion options
        Args:
            _event: not used but mandatory

`FloatingHelpWindow(w, h, posx, posy, *args, **kwargs)`
:   floating basic window with helping text inside
    Inherit tkinter TopLevel
    Found on the internet (stackoverflow) but did not keep link sorry...
    
    Construct a toplevel widget with the parent MASTER.
    
    Valid resource names: background, bd, bg, borderwidth, class,
    colormap, container, cursor, height, highlightbackground,
    highlightcolor, highlightthickness, menu, relief, screen, takefocus,
    use, visual, width.

    ### Ancestors (in MRO)

    * tkinter.Toplevel
    * tkinter.BaseWidget
    * tkinter.Misc
    * tkinter.Wm

    ### Methods

    `onMotion(self, event)`
    :   Floating window dragging ongoing
        Args:
            event: event.x and event.y hold the new position of the window

    `startMove(self, event)`
    :   Floating window dragging started
        Args:
            event: event.x and event.y hold the new position of the window

    `stopMove(self, _event)`
    :   Floating window dragging stopped
        Args:
            _event: Not used but mandatory