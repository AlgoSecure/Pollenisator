Module Pollenisator.core.Components.Modules.Report
==================================================
Module to add defects and export them

Classes
-------

`Report(parent, settings)`
:   Store elements to report and create docx or xlsx with them
    
    Constructor

    ### Class variables

    `iconName`
    :

    `tabName`
    :

    ### Static methods

    `getEases()`
    :   Returns: 
            Returns a list of ease of exploitation levels for a security defect.

    `getImpacts()`
    :   Returns: 
            Returns a list of impact levels for a security defect.

    `getRisks()`
    :   Returns: 
            Returns a list of risk levels for a security defect.

    `getTypes()`
    :   Returns: 
            Returns a list of type for a security defect.

    ### Methods

    `OnDoubleClick(self, event)`
    :   Callback for double click on treeview.
        Opens a window to update the double clicked defect view.
        Args:
            event: automatically created with the event catch. stores data about line in treeview that was double clicked.

    `addDefect(self, defect_o)`
    :   Add the given defect object in the treeview
        Args:
            defect_o: a Models.Defect object to be inserted in treeview

    `addDefectCallback(self)`
    :   Open an insert defect view form in a child window

    `deleteSelectedItem(self)`
    :   Remove selected defect from treeview
        Args:
            _event: not used but mandatory

    `fillWithDefects(self)`
    :   Fetch defects that are global (not assigned to an ip) and fill the defect table with them.

    `findInsertIndex(self, defect_o)`
    :   Find the inserting position for the given defect (treeview is sorted by risk)
        Args:
            defect_o: a Models.Defect object to be inserted in treeview
        Returns:
            the string "end" to insert at the end of the treeview
            an integer between 0 and the nb of lines-1 otherwise

    `generateReportExcel(self)`
    :   Export a calendar status to an excel file.

    `generateReportPowerpoint(self)`
    :   Export a calendar defects to a pptx formatted file.

    `generateReportWord(self)`
    :   Export a calendar defects to a word formatted file.

    `getDefectsAsDict(self)`
    :   Returns a dictionnary with treeview defects stored inside
        Returns:
            The returned dict will be formed this way (shown as json):
            {
                "Risk level describer 1":{
                    "defect title 1": {
                        "description":{
                            "title": "defect title 1",
                            "risk": "Risk level 1",
                            "ease": "Ease of exploitation 1",
                            "impact": "Impact 1",
                            "redactor": "Redactor name",
                            "type": ['D', 'T', ...]
                        },
                        "defects_ids":[
                            id 1,
                            id 2...
                        ]
                    },
                    "defect title 2":{
                        ...
                    }
                    ...
                },
                "Risk level describer 2":{
                    ...
                }
                ...
            }

    `initUI(self, parent, nbk, treevw)`
    :   Initialize window and widgets.

    `moveItemDown(self)`
    :   Swap the selected treeview item with the one down below it.
        Args:
            _event: not used but mandatory
        Returns:
            returns "break" to stop the interrupt the event thus preventing cursor to move down

    `moveItemUp(self)`
    :   Swap the selected treeview item with the one up above it.
        Args:
            _event: not used but mandatory
        Returns:
            returns "break" to stop the interrupt the event thus preventing cursor to move up

    `on_click(self)`
    :   Callback for selecting word template.
        Open a filedialog window and sets the entry value to the selected file
        Args:
            _event: not used but mandatory

    `on_click_pptx(self)`
    :   Callback for selecting powerpoint template.
        Open a filedialog window and sets the entry value to the selected file
        Args:
            _event: not used but mandatory

    `open(self)`
    :

    `refreshUI(self)`
    :   Reload informations and reload them into the widgets

    `removeItem(self, toDeleteIid)`
    :   Remove defect from given iid in defect treeview
        Args:
            toDeleteIid: database ID of defect to delete

    `reset(self)`
    :   reset defect treeview by deleting every item inside.

    `resizeDefectTreeview(self)`
    :

    `selectAll(self, _event)`
    :   Select all text in an entry
        Args:
            _event: not used but mandatory
        Returns:
            returns "break" to stop the interrupt the event thus preventing the shortcut key to be written

    `setMainRedactor(self)`
    :   Sets a main redactor for a pentest. Each not assigned defect will be assigned to him/her

    `updateDefectInTreevw(self, defect_m, redactor=None)`
    :   Change values of a selected defect in the treeview
        Args:
            defect_m: a defect model with updated values
            redactor: a redactor name for this defect, can be None (default)