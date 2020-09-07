"""A special form that contains all other forms"""

import tkinter.ttk as ttk
from core.Forms.FormCombo import FormCombo
from core.Forms.FormChecklist import FormChecklist
from core.Forms.FormStr import FormStr
from core.Forms.FormText import FormText
from core.Forms.FormButton import FormButton
from core.Forms.FormDate import FormDate
from core.Forms.FormLabel import FormLabel
from core.Forms.FormImage import FormImage
from core.Forms.FormFile import FormFile
from core.Forms.FormHidden import FormHidden
from core.Forms.FormTreevw import FormTreevw
from core.Forms.FormCheckbox import FormCheckbox
from core.Forms.FormHelper import FormHelper
from core.Forms.FormSearchBar import FormSearchBar
from core.Forms.Form import Form


class FormPanel(Form):
    """
    Form field representing a panel. It is composed of other forms.
    Additional kwargs values:
        grid: set the layout to grid, default to False
    Default setted values:
        width=500
        if pack : padx = 10, pady = 5, side = top, fill = x
        if grid: row = column = 0 sticky = "East"
    """

    def __init__(self, **kwargs):
        """
        Constructor for a panel.
        """
        super().__init__("panel")
        self.subforms = []
        self.kwargs = kwargs
        self.gridLayout = self.getKw("grid", False)
        self.panel = None

    def constructView(self, parent):
        """
        Create the panel view by constructing all subforms views inside a tkinter panel the parent view given.
        Args:
            parent: parent view or parent FormPanel.
        """
        if isinstance(parent, FormPanel):  # Panel is a subpanel
            self.panel = ttk.Frame(parent.panel)
        else:
            self.panel = ttk.Frame(parent)
        for form in self.subforms:
            form.constructView(self)
        if isinstance(parent, FormPanel):  # Panel is a subpanel
            if parent.gridLayout:
                self.panel.grid_rowconfigure(0, weight=1)
                self.panel.grid_columnconfigure(0, weight=1)
                self.panel.grid(column=self.getKw(
                    "column", 0), row=self.getKw("row", 0), sticky=tk.NSEW, **self.kwargs)
            else:
                self.panel.pack(fill=self.getKw("fill", "both"), side=self.getKw(
                    "side", "top"), pady=self.getKw("pady", 5), padx=self.getKw("padx", 10), expand=True, **self.kwargs)
        else:  # Master panel, packing
            self.panel.pack(fill="both", side="top", pady="5", padx="30", expand=True)

    def checkForm(self):
        """
        Check if this form is correctly filled. A panel is correctly filled if all subforms composing it are correctly filled.

        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }
        """
        for form in self.subforms:
            res, msg = form.checkForm()
            if res == False:
                return False, msg
        return True, ""

    def setFocusOn(self, name):
        """Set focus on the given form name
        Args:
            name: the form name to set the focus on
        """
        for form in self.subforms:
            if name == form.name:
                form.setFocus()

    def getValue(self):
        """
        Return the form value. Required for a form.
        Returns:
            returns a list of tuple with subform's name and values.
        """
        res = []
        for form in self.subforms:
            val = form.getValue()
            if val is not None:
                if type(val) is list:
                    res += val
                else:
                    res.append((form.name, val))
        return res

    def addFormTreevw(self, name, headers,
                      default_values=None, **kwargs):
        """
        Add a form table to this panel.
        Args:
            name: the table desired name
            headers: a list of 2 strings for the table headers
            default_values: a dictionnary with key = column 0 and value = column 1
            kwargs: Keywords for FormTreevw
        """
        ret = FormTreevw(name, headers, default_values, **kwargs)
        self.subforms.append(ret)
        return ret

    def addFormCombo(self, name, choicesList, default=None, **kwargs):
        """
        Add a form combo to this panel.
        Args:
            name: the combobox desired name
            choicesList: a list of options as strings
            default: a string within the choicesList that will be selected by default. optional.
            kwargs: keywords for FormCombo
        """
        formCombo = FormCombo(name, choicesList, default, **kwargs)
        self.subforms.append(formCombo)
        return formCombo

    def addFormChecklist(self, name, choicesList, default=None, **kwargs):
        """
        Add a form checklist to this panel.
        Args:
            name: the checklist desired name
            choicesList: a list of options as strings
            default: a list of string within the choicesList that will be selected by default
            kwargs: keywords for FormCheckList
        """
        if default is None:
            default = []
        f = FormChecklist(
            name, choicesList, default, **kwargs)
        self.subforms.append(f)
        return f

    def addFormCheckbox(self, name, text, default, **kwargs):
        """
        Add a form checkbox to this panel.

        Args:
            name: the checkbox desired name
            text: a label that will be in front of the checkbox
            default: a boolean indicating if the checkbox should be check by default
            kwargs: keywords for FormCheckbox
        """
        f = FormCheckbox(name, text, default, **kwargs)
        self.subforms.append(f)
        return f

    def addFormStr(self, name, regexvalidation="", default="", contextualMenu=None, **kwargs):
        """
        Add a form String to this panel.

        Args:
            name: the string var desired name
            regexvalidation: a regex to validate this input
            default: a default value for this input
            width: the width size of the input
            kwargs: keywords for FormStr
        """
        f = FormStr(name, regexvalidation, default, contextualMenu, **kwargs)
        self.subforms.append(f)
        return f

    def addFormSearchBar(self, name, searchCallback, list_of_forms_to_fill, default="", **kwargs):
        """
        Add a form String to this panel.

        Args:
            name: the string var desired name
            searchCallback: a callback
            list_of_forms_to_fill: a list of form that this searchbar callback should be able to fill
            default: a default value for this input
            kwargs: keywords for FormSearchbar
        """
        f = FormSearchBar(
            name, searchCallback, self, list_of_forms_to_fill, default, **kwargs)
        self.subforms.append(f)
        return f

    def addFormFile(self, name, regexvalidation="", default="", **kwargs):
        """
        Add a form String to this panel.

        Args:
            name: the string var desired name
            regexvalidation: a regex validating the form
            default: a default value for this input
            kwargs: keywords for FormFile
        """
        f = FormFile(name, regexvalidation, default, **kwargs)
        self.subforms.append(f)
        return f

    def addFormText(self, name, regexvalidation="", default="", contextualMenu=None, **kwargs):
        """
        Add a form Text to this panel.

        Args:
            name: the text var desired name
            regexvalidation: a regex to validate this input
            default: a default value for this input
            kwargs: keywords for FormText
        """
        f = FormText(name, regexvalidation, default, contextualMenu, **kwargs)
        self.subforms.append(f)
        return f

    def addFormDate(self, name, root, default="", dateformat='%d/%m/%Y %H:%M:%S', **kwargs):
        """
        Add a form Date to this panel.

        Args:
            name: the text var desired name
            default: a default value for this input
            dateformat: a date format to validate this input. Default to dd/mm/YYYY hh:mm:ss.
            kwargs: keywords for FormDate
        """
        f = FormDate(name, root, default, dateformat, **kwargs)
        self.subforms.append(f)
        return f

    def addFormLabel(self, name, text="", **kwargs):
        """
        Add a form Label to this panel.

        Args:
            name: the label desired name
            text: the text printed by the label
            kwargs: keywords for FormLabel
        """
        f = FormLabel(name, text, **kwargs)
        self.subforms.append(f)
        return f

    def addFormImage(self, path, **kwargs):
        """
        Add a form Label to this panel.

        Args:
            path: the image path
            kwargs: keywords for FormImage (same as tk label)
        """
        f = FormImage(path, **kwargs)
        self.subforms.append(f)
        return f

    def addFormHelper(self, helper, **kwargs):
        """
        Add a form Label to this panel.

        Args:
            helper: the text printed by the helper
            kwargs: keywords for FormHelper
        """
        f = FormHelper("", helper, **kwargs)
        self.subforms.append(f)
        return f

    def addFormButton(self, name, callback, **kwargs):
        """
        Add a form Button to this panel.

        Args:
            name: the button desired name and text
            callback: a function that will be called when the button is pressed.
            kwargs: keywords for FormButton
        """
        f = FormButton(name, callback, **kwargs)
        self.subforms.append(f)
        return f

    def addFormHidden(self, name, default=""):
        """
        Add a form Hidden to this panel.

        Args:
            name: the hidden value desired name and text
            default: the value to be hidden
        """
        f = FormHidden(name, default)
        self.subforms.append(f)
        return f

    def addFormPanel(self, **kwargs):
        """
        Add a form Pannel to this panel.

        Args:
            kwargs: can indicate grid=True if a grid layout must be set for subelements.
        Returns:
            Return the new panel to add other forms in.
        """
        pan = FormPanel(**kwargs)
        self.subforms.append(pan)
        return pan

    def clear(self):
        """
        Empties the panel's subforms.
        """
        del self.subforms
        self.subforms = []
