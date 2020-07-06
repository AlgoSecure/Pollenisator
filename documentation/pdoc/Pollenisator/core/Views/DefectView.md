Module Pollenisator.core.Views.DefectView
=========================================
View for defect object. Handle node in treeview and present forms to user when interacted with.

Classes
-------

`DefectView(appTw, appViewFrame, mainApp, controller)`
:   View for defect object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory.
    
    Constructor
    Args:
        appTw: a PollenisatorTreeview instance to put this view in
        appViewFrame: an view frame to build the forms in.
        mainApp: the Application instance
        controller: a CommandController for this view.

    ### Ancestors (in MRO)

    * core.Views.ViewElement.ViewElement

    ### Class variables

    `icon`
    :

    ### Static methods

    `DbToTreeviewListId(parent_db_id)`
    :   Converts a mongo Id to a unique string identifying a list of defects given its parent
        Args:
            parent_db_id: the parent node mongo ID
        Returns:
            A string that should be unique to describe the parent list of defect node

    `treeviewListIdToDb(treeviewId)`
    :   Extract from the unique string identifying a list of defects the parent db ID
        Args:
            treeviewId: the treeview node id of a list of defects node
        Returns:
            the parent object mongo id as string

    ### Methods

    `addAProof(self, _event, obj)`
    :   Callback when add proof is clicked.
        Add proof and update window
        Args
            _event: mandatory but not used
            obj: the clicked index proof

    `addInTreeview(self, parentNode=None)`
    :   Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            _addChildren: not used here

    `beforeDelete(self, iid=None)`
    :   Called before defect deletion.
        Will attempt to remove this defect from global defect table.
        Args:
            iid: the mongo ID of the deleted defect

    `deleteProof(self, _event, obj)`
    :   Callback when delete proof is clicked.
        remove remote proof and update window
        Args
            _event: mandatory but not used
            obj: the clicked index proof

    `insertReceived(self)`
    :   Called when a defect insertion is received by notification.
        Insert the node in treeview.
        Also insert it in global report of defect

    `openInsertWindow(self, notes='', addButtons=True)`
    :   Creates a tkinter form using Forms classes. This form aims to insert a new Defect
        Args:
            notes: default notes to be written in notes text input. Default is ""
            addButtons: boolean value indicating that insertion buttons should be visible. Default to True

    `openModifyWindow(self, addButtons=True)`
    :   Creates a tkinter form using Forms classes.
        This form aims to update or delete an existing Defect
        Args:
            addButtons: boolean value indicating that insertion buttons should be visible. Default to True

    `updateReceived(self)`
    :   Called when a defect update is received by notification.
        Update the defect node and the report defect table.

    `updateRiskBox(self)`
    :   Callback when ease or impact is modified.
        Calculate new resulting risk value
        Args
            _event: mandatory but not used

    `viewProof(self, _event, obj)`
    :   Callback when view proof is clicked.
        Download and display the file using xdg-open on linux or os.startfile (windows)
        Args
            _event: mandatory but not used
            obj: the clicked index proof