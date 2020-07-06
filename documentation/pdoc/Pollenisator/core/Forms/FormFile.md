Module Pollenisator.core.Forms.FormFile
=======================================
Widget with an entry to type a file path and a '...' button to pick from file explorer.

Classes
-------

`FormFile(name, regexValidation='', default='', **kwargs)`
:   Form field representing a path input.
    Default setted values: 
        state="readonly"
        if pack : padx = pady = 5, side = "right"
        if grid: row = column = 0 sticky = "west"
        entry "width"=  20
    Additional values to kwargs:
        modes: either "file" or "directory" to choose which type of path picker to open
    
    Constructor for a form file
    
    Args:
        name: the entry name (id).
        regexValidation: a regex used to check the input in the checkForm function., default is ""
        default: a default value for the Entry, default is ""
        kwargs: same keyword args as you would give to ttk.Frame + "modes" which is either "file" or "directory" 
                to choose which type of path picker to open

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `checkForm(self)`
    :   Check if this form is correctly filled. Check with the regex validation given in constructor.
        
        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }

    `constructView(self, parent)`
    :   Create the string view inside the parent view given
        
        Args:
            parent: parent FormPanel.

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return the entry value as string.

    `on_click(self)`
    :   Callback when '...' is clicked and modes Open a file selector (tkinter.filedialog.askopenfilename)
        Args:
            _event: not used but mandatory
        Returns:
            None if no file name is picked,
            the selected file full path otherwise.

    `on_click_dir(self)`
    :   Callback when '...' is clicked and modes="directory" was set.
        Open a directory selector (tkinter.filedialog.askdirectory)
        Args:
            _event: not used but mandatory
        Returns:
            None if no directory is picked,
            the selected directory full path otherwise.

    `selectAll(self, _event)`
    :   Callback to select all the text in the date Entry.
        Args:
            _event: mandatory but not used
        Returns:
            Returns the string "break" to prevent the event to be treated by the Entry, thus inserting unwanted value.

    `setFocus(self)`
    :   Set the focus to the ttk entry part of the widget.