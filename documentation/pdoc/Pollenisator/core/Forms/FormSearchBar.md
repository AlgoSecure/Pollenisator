Module Pollenisator.core.Forms.FormSearchBar
============================================

Classes
-------

`FormSearchBar(name, searchCallback, panel_to_fill, list_of_forms_to_fill, default='', **kwargs)`
:   Form field representing a string input.
    
    Constructor for a form entry
    
    Args:
        name: the entry name (id).
        regexValidation: a regex used to check the input in the checkForm function., default is ""
        default: a default value for the Entry, defauult is ""

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `constructView(self, parent)`
    :   Create the string view inside the parent view given
        
        Args:
            parent: parent FormPanel.

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return the entry value as string.

    `postSelect(self)`
    :

    `selectAll(self, _event)`
    :

    `setFocus(self)`
    :   Defines what item should be focused inside the form widget

    `updateValues(self)`
    :