Module Pollenisator.core.Forms.FormCombo
========================================
Describe tkinter combobox with default common args

Classes
-------

`FormCombo(name, choicesList, default, **kwargs)`
:   Form field representing a combobox.
    Default setted values: 
        state="readonly"
        if pack : padx = pady = 5, side = "right"
        if grid: row = column = 0 sticky = "west"
    Additional values to kwargs:
        binds:  a dictionnary of tkinter binding with shortcut as key and callback as value
    
    Constructor for a form checkbox
    
    Args:
        name: the checklist name (id).
        choicesList: a list of string forming all the possible choices.
        default: a list of string that should be prechecked if in the choice list.
        kwargs: same keyword args as you would give to ttk.Combobox

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `checkForm(self)`
    :   Check if this form is correctly filled. Formal verification if the selected value is still on the choice list.
        
        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }

    `constructView(self, parent)`
    :   Create the combobox view inside the parent view given
        
        Args:
            parent: parent FormPanel.

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return the selected text inside the comboxbox.

    `setFocus(self)`
    :   Set the focus to the ttk combobox.

    `setValue(self, newval)`
    :   Set the combo value.
        Args:
            newval: the new value to be set inside the combobox