Module Pollenisator.core.Forms.FormHelper
=========================================
Widget with a button that display an helping message when hovered

Classes
-------

`FormHelper(name, text, **kwargs)`
:   Form field representing a helper button.
    Default setted values: 
        state="readonly"
        if pack : padx = pady = 5, side = "right"
        if grid: row = column = 0 sticky = "west"
        entry "width"=  20
    
    Constructor for a form button
    
    Args:
        name: the helper name. Should not matter as it does not return data
        text: the helping message to be displayed
        kwargs: same keyword args as you would give to ttk.Label

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Class variables

    `img_class`
    :

    ### Methods

    `close(self)`
    :   Callback for the <Leave> event
        Stops displaying the help message
        Args:
            _event: not used but mandatory

    `constructView(self, parent)`
    :   Create the button view inside the parent view given
        
        Args:
            parent: parent form panel.

    `enter(self)`
    :   Callback for the <Enter> event
        Starts displaying the help message
        Args:
            _event: not used but mandatory