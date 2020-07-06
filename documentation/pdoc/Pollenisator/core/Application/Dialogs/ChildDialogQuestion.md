Module Pollenisator.core.Application.Dialogs.ChildDialogQuestion
================================================================
Ask a question to the user.

Classes
-------

`ChildDialogQuestion(parent, title, question, answers=('Yes', 'No'))`
:   Open a child dialog of a tkinter application to ask a question.
    
    Open a child dialog of a tkinter application to ask a question.
    
    Args:
        parent: the tkinter parent view to use for this window construction.
        title: title of the new window
        question: question to answer
        answers: a tuple with possible answers. Default to ("Yes" ,"No")

    ### Methods

    `onOk(self, event)`
    :   Called when the user clicked the validation button.
        Set the rvalue attributes to the answer string choosen.