Module Pollenisator.core.Forms.FormTreevw
=========================================
Widget "Table" using a ttk Treeview

Classes
-------

`FormTreevw(name, headings, default_values=None, **kwargs)`
:   Form field representing a multi-lined input.
    
    Constructor for a form text
    
    Args:
        name: the treeview name (id).
        headings: table headers
        default_values: default values for the Table as a dict, default is None
        kwargs: same keyword args as you would give to ttk.Treeview

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `OnDoubleClick(self, event)`
    :   Callback for double click event
        Edit value of double clicked item
        Args:
            event: automatically filled when event is triggered.

    `close(self)`
    :   Option of the contextual menu : Close the contextual menu by doing nothing

    `constructView(self, parent)`
    :   Create the text view inside the parent view given
        
        Args:
            parent: parent FormPanel.

    `copy(self)`
    :   Option of the contextual menu : Copy entry text to clipboard

    `deleteItem(self)`
    :   Callback for <Del> event
        Remove the selected item in the treeview
        Args:
            _event: not used but mandatory

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return the entry value as string.

    `popup(self, event)`
    :   Fill the self.widgetMenuOpen and reraise the event in the editing window contextual menu
        
        Args:
            event: a ttk Treeview event autofilled.
            Contains information on what treeview node was clicked.

    `popupFocusOut(self)`
    :   Callback for focus out event. Destroy contextual menu
        Args:
            _event: not used but mandatory

    `recurse_insert(self, values, parent='', columnsLen=None, odd=False)`
    :   Recursive insert of a value in a table:
        Args:
            values: values to insert in the treeview
                    * If it is a dict : Recurse
                    * If it is a list : Add key without value and list values as subchildren
                    * If it is a str : Insert into parent
            parent: the parent node treeview id to insert values into
            columnsLen: a table with the width of each column as list of 2 int
            odd: insert value as an odd value (the line will be tagged odd and change color). Default is False
        Returns:
            Final size of columns as list of two int

    `reset(self)`
    :   Reset the treeview values (delete all lines)