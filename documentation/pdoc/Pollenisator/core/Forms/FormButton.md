Module Pollenisator.core.Forms.FormButton
=========================================
Describe tkinter button with default common args

Classes
-------

`FormButton(name, callback, **kwargs)`
:   Form field representing a button.
    Default setted values: 
        if pack : padx = pady = 5, side = right
        if grid: row = column = 0 sticky = "west
    
    Constructor for a form button
    
    Args:
        name: the button text.
        callback: a function that will be called when the button is clicked.
        kwargs: same keyword args as you would give to ttk.Button

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `configure(self, **kwargs)`
    :   Change kwargs to given one. Must be called before constructView
        Args:
            **kwargs: any ttk Button keyword arguments.

    `constructView(self, parent)`
    :   Create the button view inside the parent view given
        
        Args:
            parent: parent form panel.

    `setFocus(self)`
    :   Set the focus to the ttk button.