Module Pollenisator.core.Forms.FormDate
=======================================
Widget with an entry to type a date and a calendar button to choose a date.

Classes
-------

`FormDate(name, root, default='', dateformat='%d/%m/%Y %H:%M:%S', **kwargs)`
:   Form field representing a date.
    Default setted values: 
        state="readonly"
        if pack : padx = pady = 5, side = "right"
        if grid: row = column = 0 sticky = "west"
    
    Constructor for a form checkbox
    
    Args:
        name: the date name (id).
        root: the tkinter root window
        default: a list of string that should be prechecked if in the choice list.
        dateformat: a date format as a string see datetime.strptime documentation.
        kwargs: same keyword args as you would give to ttk.Frame

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `checkForm(self)`
    :   Check if this form is correctly filled. Check with the dateformat given in constructorn or "None".
        
        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }

    `constructView(self, parent)`
    :   Create the date view inside the parent view given
        
        Args:
            parent: parent FormPanel.

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return the date as string text.

    `selectAll(self, _event)`
    :   Callback to select all the text in the date Entry.
        Args:
            _event: mandatory but not used
        Returns:
            Returns the string "break" to prevent the event to be treated by the Entry, thus inserting unwanted value.

    `setFocus(self)`
    :   Set the focus to the ttk entry part of the widget.

    `showDatePicker(self)`
    :   Callback to start displaying the date picker calendar window
        Args:
            _event: mandatory but not used