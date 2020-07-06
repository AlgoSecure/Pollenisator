Module Pollenisator.core.Forms.FormChecklist
============================================
Widget with a list of checkbox packed and wrapping. A checkbox to check or uncheck all is at the top
#TODO improve looking and constructing

Classes
-------

`FormChecklist(name, choicesList, default, **kwargs)`
:   Form field representing a checklist.
    Default setted values: 
        if pack : padx = 10, pady = 5, side = top, fill = "x"
        if grid: row = column = 0
    
    Constructor for a form checklist
    Args:
        name: the checklist name (id).
        choicesList: a list of string forming all the possible choices.
        default: a list of string that should be prechecked if in the choice list.
        kwargs: same keyword args as you would give to ttk.Frame

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `checkForm(self)`
    :   Check if this form is correctly filled. A checklist cannot be malformed.
        
        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }

    `checkall(self)`
    :   Will check all the checkbox or uncheck same depending on the checkbox state.

    `constructView(self, parent)`
    :   Create the checlist view inside the parent view given
        
        Args:
            FormPanel: parent form panel.

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return a dictionnary of all checkboxs with texts as keys and 0 or 1 as value. 1 is if the checkbox was ticked.

    `setFocus(self)`
    :   Set the focus to the first ttk checkbox of the list.

    `setValue(self, newval)`
    :   Set value of checkboxes defined in given list.
        Args:
            newval: A list with checkbox texts. If a checkbox text matches one in the list, it will checked.