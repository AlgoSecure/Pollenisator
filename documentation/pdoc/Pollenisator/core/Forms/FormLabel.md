Module Pollenisator.core.Forms.FormLabel
========================================
Describe tkinter Label with default common args

Classes
-------

`FormLabel(name, text, **kwargs)`
:   Form field representing a label.
    Default setted values:
        width=500
        if pack : padx = pady = 5, side = left
        if grid: row = column = 0 sticky = "East"
    
    Constructor for a form label
    Args:
        name: the label name.
        text: the text showed by the label.
        kwargs: same keyword args as you would give to ttk.Label

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `constructView(self, parent)`
    :   Create the label view inside the parent view given
        
        Args:
            parent: parent FormPanel.

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return the label text.

    `setValue(self, _newval)`
    :   nothing to set so overwrite
        Args:
            _newval: not used