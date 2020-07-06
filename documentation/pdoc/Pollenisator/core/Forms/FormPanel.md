Module Pollenisator.core.Forms.FormPanel
========================================
A special form that contains all other forms

Classes
-------

`FormPanel(**kwargs)`
:   Form field representing a panel. It is composed of other forms.
    Additional kwargs values:
        grid: set the layout to grid, default to False
    Default setted values:
        width=500
        if pack : padx = 10, pady = 5, side = top, fill = x
        if grid: row = column = 0 sticky = "East"
    
    Constructor for a panel.

    ### Ancestors (in MRO)

    * core.Forms.Form.Form

    ### Methods

    `addFormButton(self, name, callback, **kwargs)`
    :   Add a form Button to this panel.
        
        Args:
            name: the button desired name and text
            callback: a function that will be called when the button is pressed.
            kwargs: keywords for FormButton

    `addFormCheckbox(self, name, text, default, **kwargs)`
    :   Add a form checkbox to this panel.
        
        Args:
            name: the checkbox desired name
            text: a label that will be in front of the checkbox
            default: a boolean indicating if the checkbox should be check by default
            kwargs: keywords for FormCheckbox

    `addFormChecklist(self, name, choicesList, default=None, **kwargs)`
    :   Add a form checklist to this panel.
        Args:
            name: the checklist desired name
            choicesList: a list of options as strings
            default: a list of string within the choicesList that will be selected by default
            kwargs: keywords for FormCheckList

    `addFormCombo(self, name, choicesList, default=None, **kwargs)`
    :   Add a form combo to this panel.
        Args:
            name: the combobox desired name
            choicesList: a list of options as strings
            default: a string within the choicesList that will be selected by default. optional.
            kwargs: keywords for FormCombo

    `addFormDate(self, name, root, default='', dateformat='%d/%m/%Y %H:%M:%S', **kwargs)`
    :   Add a form Date to this panel.
        
        Args:
            name: the text var desired name
            default: a default value for this input
            dateformat: a date format to validate this input. Default to dd/mm/YYYY hh:mm:ss.
            kwargs: keywords for FormDate

    `addFormFile(self, name, regexvalidation='', default='', **kwargs)`
    :   Add a form String to this panel.
        
        Args:
            name: the string var desired name
            regexvalidation: a regex validating the form
            default: a default value for this input
            kwargs: keywords for FormFile

    `addFormHelper(self, helper, **kwargs)`
    :   Add a form Label to this panel.
        
        Args:
            helper: the text printed by the helper
            kwargs: keywords for FormHelper

    `addFormHidden(self, name, default='')`
    :   Add a form Hidden to this panel.
        
        Args:
            name: the hidden value desired name and text
            default: the value to be hidden

    `addFormLabel(self, name, text='', **kwargs)`
    :   Add a form Label to this panel.
        
        Args:
            name: the label desired name
            text: the text printed by the label
            kwargs: keywords for FormLabel

    `addFormPanel(self, **kwargs)`
    :   Add a form Pannel to this panel.
        
        Args:
            kwargs: can indicate grid=True if a grid layout must be set for subelements.
        Returns:
            Return the new panel to add other forms in.

    `addFormSearchBar(self, name, searchCallback, list_of_forms_to_fill, default='', **kwargs)`
    :   Add a form String to this panel.
        
        Args:
            name: the string var desired name
            searchCallback: a callback
            list_of_forms_to_fill: a list of form that this searchbar callback should be able to fill
            default: a default value for this input
            kwargs: keywords for FormSearchbar

    `addFormStr(self, name, regexvalidation='', default='', contextualMenu=None, **kwargs)`
    :   Add a form String to this panel.
        
        Args:
            name: the string var desired name
            regexvalidation: a regex to validate this input
            default: a default value for this input
            width: the width size of the input
            kwargs: keywords for FormStr

    `addFormText(self, name, regexvalidation='', default='', contextualMenu=None, **kwargs)`
    :   Add a form Text to this panel.
        
        Args:
            name: the text var desired name
            regexvalidation: a regex to validate this input
            default: a default value for this input
            kwargs: keywords for FormText

    `addFormTreevw(self, name, headers, default_values=None, **kwargs)`
    :   Add a form table to this panel.
        Args:
            name: the table desired name
            headers: a list of 2 strings for the table headers
            default_values: a dictionnary with key = column 0 and value = column 1
            kwargs: Keywords for FormTreevw

    `checkForm(self)`
    :   Check if this form is correctly filled. A panel is correctly filled if all subforms composing it are correctly filled.
        
        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }

    `clear(self)`
    :   Empties the panel's subforms.

    `constructView(self, parent)`
    :   Create the panel view by constructing all subforms views inside a tkinter panel the parent view given.
        Args:
            parent: parent view or parent FormPanel.

    `getValue(self)`
    :   Return the form value. Required for a form.
        Returns:
            returns a list of tuple with subform's name and values.

    `setFocusOn(self, name)`
    :   Set focus on the given form name
        Args:
            name: the form name to set the focus on