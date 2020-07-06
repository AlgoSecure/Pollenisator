Module Pollenisator.core.Application.Dialogs.ChildDialogDefectView
==================================================================
This class pop a defect view form in a subdialog

Classes
-------

`ChildDialogDefectView(parent, settings, defectModel=None)`
:   Open a child dialog of a tkinter application to answer a question.
    
    Open a child dialog of a tkinter application to choose autoscan settings.
    
    Args:
        parent: the tkinter parent view to use for this window construction.
        defectModel : A Defect Model object to load default values. None to have empty fields, default is None.

    ### Methods

    `cancel(self)`
    :   called when canceling the window.
        Close the window and set rvalue to False
        Args:
            _event: Not used but mandatory

    `okCallback(self)`
    :   called when pressing the validating button
        Close the window if the form is valid.
        Set rvalue to True and perform the defect update/insert if validated.
        Args:
            _event: Not used but mandatory

`DummyMainApp(settings)`
: