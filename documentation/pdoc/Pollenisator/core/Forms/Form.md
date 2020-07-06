Module Pollenisator.core.Forms.Form
===================================
Describe custom tkinter widgets or extended tkinter widgets

Classes
-------

`Form(name)`
:   Describe custom tkinter widgets or extended tkinter widgets
    Form field empty, should be inherited to create a new Form.
    
    Constructor for an empty form.
    
    Args:
        name: the button text.

    ### Methods

    `checkForm(self)`
    :   Check if this form is correctly filled.
        
        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }

    `constructView(self, parent)`
    :   Create the view inside the parent view given
        Args:
            parent: parent tkinter container widget

    `getKw(self, key, default)`
    :   Read and delete the given key inside the stored kwargs.
        If key does not exist, default will be returned.
        Args:
            key: the key matching the wanted value in kwargs
            default: a default value to be returned in case the key does not exist.

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return None

    `setFocus(self)`
    :   Defines what item should be focused inside the form widget

    `setValue(self, newval)`
    :   Set the form value. Required for a form.
        Args:
           newval: new value to be setted