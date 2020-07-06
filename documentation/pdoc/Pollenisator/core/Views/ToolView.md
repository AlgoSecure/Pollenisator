Module Pollenisator.core.Views.ToolView
=======================================
View for tool object. Handle node in treeview and present forms to user when interacted with.

Classes
-------

`ToolView(appTw, appViewFrame, mainApp, controller)`
:   View for tool object. Handle node in treeview and present forms to user when interacted with.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory
        done_icon: icon filename for done tools
        ready_icon: icon filename for ready tools
        running_icon: icon filename for running tools
        not_ready_icon: icon filename for not ready tools
        cached_icon: a cached loaded PIL image icon of ToolView.icon. Starts as None.
        cached_done_icon: a cached loaded PIL image icon of ToolView.done_icon. Starts as None.
        cached_ready_icon: a cached loaded PIL image icon of ToolView.ready_icon. Starts as None.
        cached_running_icon: a cached loaded PIL image icon of ToolView.running_icon. Starts as None.
        cached_not_ready_icon: a cached loaded PIL image icon of ToolView.not_ready_icon. Starts as None.
        
    
    Constructor
    Args:
        appTw: a PollenisatorTreeview instance to put this view in
        appViewFrame: an view frame to build the forms in.
        mainApp: the Application instance
        controller: a CommandController for this view.

    ### Ancestors (in MRO)

    * core.Views.ViewElement.ViewElement

    ### Class variables

    `cached_done_icon`
    :

    `cached_icon`
    :

    `cached_not_ready_icon`
    :

    `cached_ready_icon`
    :

    `cached_running_icon`
    :

    `done_icon`
    :

    `icon`
    :

    `not_ready_icon`
    :

    `ready_icon`
    :

    `running_icon`
    :

    ### Static methods

    `DbToTreeviewListId(parent_db_id)`
    :   Converts a mongo Id to a unique string identifying a list of tools given its parent
        Args:
            parent_db_id: the parent node mongo ID
        Returns:
            A string that should be unique to describe the parent list of tool node

    `treeviewListIdToDb(treeview_id)`
    :   Extract from the unique string identifying a list of tools the parent db ID
        Args:
            treeview_id: the treeview node id of a list of tools node
        Returns:
            the parent object mongo id as string

    ### Methods

    `addInTreeview(self, parentNode=None)`
    :   Add this view in treeview. Also stores infos in application treeview.
        Args:
            parentNode: if None, will calculate the parent. If setted, forces the node to be inserted inside given parentNode.
            _addChildren: not used for tools

    `createDefectCallback(self)`
    :   Callback for tool click #TODO move to ToolController
        Creates an empty defect view and open it's insert window with notes = tools notes.

    `downloadResultFile(self)`
    :   Callback for tool click #TODO move to ToolController
        Download the tool result file and asks the user if he or she wants to open it. 
        If OK, tries to open it using xdg-open or os.startsfile
        Args:
            _event: not used

    `getIcon(self)`
    :   Load the object icon in cache if it is not yet done, and returns it
        
        Return:
            Returns the icon representing this object.

    `launchCallback(self)`
    :   Callback for the launch tool button. Will queue this tool to a celery worker. #TODO move to ToolController
        Will try to launch respecting limits first. If it does not work, it will asks the user to force launch.
        
        Args:
            _event: Automatically generated with a button Callback, not used.

    `localLaunchCallback(self)`
    :   Callback for the launch tool button. Will launch it on localhost pseudo 'worker'.  #TODO move to ToolController
        
        Args:
            event: Automatically generated with a button Callback, not used.

    `openModifyWindow(self)`
    :   Creates a tkinter form using Forms classes. This form aims to update or delete an existing Tool

    `resetCallback(self)`
    :   Callback for the reset tool stop button. Will reset the tool to a ready state. #TODO move to ToolController
        
        Args:
            event: Automatically generated with a button Callback, not used.

    `safeLaunchCallback(self)`
    :   Callback for the launch tool button. Will queue this tool to a celery worker. #TODO move to ToolController
        Args:
            event: Automatically generated with a button Callback, not used.
        Returns:
            None if failed.

    `stopCallback(self)`
    :   Callback for the launch tool stop button. Will stop this celery task. #TODO move to ToolController
        
        Args:
            _event: Automatically generated with a button Callback, not used.

    `updateReceived(self)`
    :   Called when a tool update is received by notification.
        Update the tool treeview item (resulting in icon reloading)