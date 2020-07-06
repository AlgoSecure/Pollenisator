Module Pollenisator.core.Forms.FormCheckbox
===========================================
Describe tkinter checkbox with default common args

Classes
-------

`FormCheckbox(name, text, default, **kwargs)`
:   Form field representing a checkbox.
    Default setted values: 
        if pack : padx = pady = 5, side = right
        if grid: row = column = 0 sticky = "west"
    
    Constructor for a form checkbox
    
    Args:
        name: the checkbox name (id).
        text: the text on the checkbox
        default: boolean indicating if the checkbox should be checked by default.
        kwargs: same keyword args as you would give to ttk.CheckButton

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `checkForm(self)`
    :   Check if this form is correctly filled. A checkbox cannot be malformed.
        
        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }

    `constructView(self, parent)`
    :   Create the checkbox view inside the parent view given
        
        Args:
            parent: parent form panel.

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return True if the checkbox was checked, False otherwise.

    `setFocus(self)`
    :   Set the focus to the ttk checkbutton.