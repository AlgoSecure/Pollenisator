Module Pollenisator.core.Forms.FormText
=======================================
Describe tkinter Text with default common args and an attached scrollbar

Classes
-------

`FormText(name, regexValidation='', default='', contextualMenu=None, **kwargs)`
:   Form field representing a multi-lined input.
    Default setted values:
        width=20, height=20
        if pack : padx = pady = 5, side = left
        if grid: row = column = 0 sticky = "East"
    
    Constructor for a form text
    
    Args:
        name: the entry name (id).
        regexValidation: a regex used to check the input
                         in the checkForm function. default is ""
        default: a default value for the Entry, default is ""
        contextualMenu: (Opt.) a contextualMenu to open when right clicked. default is None
        kwargs: same keyword args as you would give to ttk.Text

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `checkForm(self)`
    :   Check if this form is correctly filled.
        Check with the regex validation given in constructor.
        
        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }

    `close(self)`
    :   Option of the contextual menu : Close the contextual menu by doing nothing

    `constructView(self, parent)`
    :   Create the text view inside the parent view given
        
        Args:
            parent: parent FormPanel.

    `copy(self)`
    :   Option of the contextual menu : Copy entry text to clipboard

    `cut(self)`
    :   Option of the contextual menu : Cut entry text to clipboard

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return the entry value as string.

    `paste(self)`
    :   Option of the contextual menu : Paste clipboard content to entry

    `popup(self, event)`
    :   Fill the self.widgetMenuOpen and reraise the event in the editing window contextual menu
        
        Args:
            event: a ttk Treeview event autofilled.
            Contains information on what treeview node was clicked.

    `popupFocusOut(self)`
    :   Callback for focus out event. Destroy contextual menu
        Args:
            _event: not used but mandatory

    `selectAll(self, _event)`
    :   Callback to select all the text in the date Entry.
        Args:
            _event: mandatory but not used
        Returns:
            Returns the string "break" to prevent the event to be treated by the Entry, thus inserting unwanted value.

    `setFocus(self)`
    :   Set the focus to the ttk entry widget.