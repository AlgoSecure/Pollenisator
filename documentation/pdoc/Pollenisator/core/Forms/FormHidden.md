Module Pollenisator.core.Forms.FormHidden
=========================================
Widget with no display that holds a value

Classes
-------

`FormHidden(name, default='')`
:   Form field hidden, to store a value.
    
    Constructor for a hidden form.
    
    Args:
        name: the form name.
        default: a default value to store in it.

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `getValue(self)`
    :   Return the form value. Required for a form.
        
        Returns:
            Return the form value.