"""View parent object. Handle node in treeview and present forms to user when interacted with."""

from core.Forms.FormPanel import FormPanel
from core.Components.Settings import Settings
from core.Application.Dialogs.ChildDialogToast import ChildDialogToast
import tkinter.messagebox
from tkinter import ttk
from tkinter import TclError
import os


class ViewElement(object):
    """
    Defines a basic view to be inherited. Those functions are generic entry points to models.
    Most of them should not be redefined in other Views.
    Attributes:
        icon: icon name to show in treeview. Icon filename must be in icon directory
        cachedClassIcon: a cached loaded PIL image icon of ViewElement.icon. Starts as None.
    """
    icon = 'undefined.png'
    cachedClassIcon = None

    def __init__(self, appTw, appViewFrame, mainApp, controller):
        """Constructor
        Args:
            appTw: a PollenisatorTreeview instance to put this view in
            appViewFrame: an view frame to build the forms in.
            mainApp: the Application instance
            controller: a CommandController for this view.
        """
        self.appliTw = appTw
        self.appliViewFrame = appViewFrame
        self.mainApp = mainApp
        self.controller = controller
        self.form = FormPanel()

    @classmethod
    def getClassIcon(cls):
        """
        Load the class icon in cache if it is not yet done, and returns it

        Return:
            Returns the ImageTk.PhotoImage icon representing this class .
        """
        from PIL import Image, ImageTk
        if cls.cachedClassIcon == None:
            abs_path = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(abs_path, "../../icon/"+cls.icon)
            cls.cachedClassIcon = ImageTk.PhotoImage(Image.open(path))
        return cls.cachedClassIcon

    def getIcon(self):
        """
        Load the object icon in cache if it is not yet done, and returns it

        Return:
            Returns the icon representing this object.
        """
        return self.__class__.getClassIcon()

    def addChildrenBaseNodes(self, newNode):
        """
        Add to the given node from a treeview the mandatory childrens.
        Will be redefined in children.

        Args:
            newNode: the newly created node we want to add children to.
        """
        # pass

    def delete(self, _event=None, showWarning=True):
        """
        Entry point to the model doDelete function.

        Args:
            _event: automatically filled if called by an event. Not used
            showWarning: a boolean. If true, the user will be asked a confirmation before supression. Default to True.
        """
        ret = True
        if showWarning:
            ret = tkinter.messagebox.askokcancel(
                "Delete", "You are going to delete this element, do you want to continue?")
        if(ret):
            self.controller.doDelete()

    def update(self, event=None):
        """
        Entry point to the model doUpdate function.

        Args:
            event: automatically filled if called by an event. Holds info on update clicked widget.
        Returns:
            * a boolean to shwo success or failure
            * an empty message on success, an error message on failure
        """
        res, msg = self.form.checkForm()
        if(res):
            form_values = self.form.getValue()
            form_values_as_dicts = ViewElement.list_tuple_to_dict(form_values)
            self.controller.doUpdate(form_values_as_dicts)
            if event is not None:
                caller = event.widget
                toast = ChildDialogToast(self.appliViewFrame, "Done" , x=caller.winfo_rootx(), y=caller.winfo_rooty()+caller.winfo_reqheight(), width=caller.winfo_reqwidth())
                toast.show()
            return True, ""
        else:
            tkinter.messagebox.showwarning(
                "Form not validated", msg, parent=self.appliViewFrame)
            return False, msg

    def insert(self, _event=None):
        """
        Entry point to the model doInsert function.

        Args:
            _event: automatically filled if called by an event. Not used
        Returns:
            * a boolean to shwo success or failure
            * an empty message on success, an error message on failure
        """
        res, msg = self.form.checkForm()
        if(res):
            form_values = self.form.getValue()
            form_values_as_dicts = ViewElement.list_tuple_to_dict(form_values)
            res, nbErrors = self.controller.doInsert(form_values_as_dicts)
            if not res:
                msg = "This element cannot be inserted, check for conflicts with existings elements."
                tkinter.messagebox.showerror(
                    "Insertion failed", msg, parent=self.appliViewFrame)
                return False, msg
            else:
                if nbErrors > 0:
                    msg = str(len(
                        res))+" were inserted, "+str(nbErrors)+" were not to avoid conflicts or out of wave elements."
                    tkinter.messagebox.showwarning(
                        "Insertion succeeded with warnings", msg, parent=self.appliViewFrame)
                    return True, msg
                else:
                    return True, ""
        else:
            tkinter.messagebox.showwarning(
                "Form not validated", msg, parent=self.appliViewFrame)
            return False, msg

    def tagClicked(self, name):
        """Callback intermediate for tag clicked
        Ensure that the tag name clicked is added to View item
        Args:
            name: a tag name
        """
        return lambda _event: self.tagButtonClicked(name)
    
    def tagButtonClicked(self, name):
        """Callback for tag button clicked
        Ensure that the tag name clicked is set to View item
        Args:
            name: a tag name
        """
        self.controller.setTags([name])

    def completeModifyWindow(self):
        """
        Add the buttons for an update window.
            -Submit button that validates the form with the update function.
            -Delete button that asks the user to delete the object with the delete function.
        """
        pan = self.form.addFormPanel()
        pan.addFormButton("Submit", self.update)
        pan.addFormButton("Delete", self.delete)
        
        registeredTags = Settings.getTags()
        keys = list(registeredTags.keys())
        column = 0
        listOfLambdas = [self.tagClicked(keys[i]) for i in range(len(keys))]
        for registeredTag, color in registeredTags.items():
            if not hasattr(self.mainApp, "parent"):
                break
            if column == 0:
                panTags = self.form.addFormPanel(pady=0)
            s = ttk.Style(self.mainApp.parent)
            s.configure(""+color+".TButton", background=color, foreground="black")
            s.map(""+color+".TButton", foreground=[('active', "dark gray")], background=[('active', color)])
            btn_tag = panTags.addFormButton(registeredTag, listOfLambdas[column], side="left", padx=0, pady=0)
            btn_tag.configure(style=""+color+".TButton")
            column += 1
            if column == 4:
                column = 0
        self.showForm()

    def showForm(self):
        """Resets the application view frame and start displaying the form in it
        """
        for widget in self.appliViewFrame.winfo_children():
            widget.destroy()
        self.form.constructView(self.appliViewFrame)

    def completeInsertWindow(self):
        """
        Add the button for an insert window.
            -Insert button that validate the form with the insert function.
        """
        pan = self.form.addFormPanel()
        pan.addFormButton("Insert", self.insert)
        for widget in self.appliViewFrame.winfo_children():
            widget.destroy()
        self.form.constructView(self.appliViewFrame)

    def hide(self):
        """Tells the application treeview to hide this node
        """
        self.appliTw.hide(str(self.controller.getDbId()))

    def unhide(self):
        """Tells the application treeview to unhide this node
        """
        self.appliTw.unhide(self)

    def __str__(self):
        """
        Return the __str__ method of the model
        """
        return str(self.controller.getModelRepr())

    @classmethod
    def DbToTreeviewListId(cls, parent_db_id):
        """Converts a mongo Id to a unique string identifying a list of view elemnt given its parent
        Args:
            parent_db_id: the parent node mongo ID
        Returns:
            A string that should be unique to describe the parent list of viewelement node
        """
        return str(parent_db_id)

    def getParent(self):
        """
        Return the id of the parent node in treeview.

        Returns:
            return the model parent id DbToTreeviewListId
        """
        return self.__class__.DbToTreeviewListId(self.controller.getParent())

    def updateReceived(self):
        """Called when any view element update is received by notification.
        Resets the node tags according to database and hide it if "hidden" is in tags
        """
        if self.controller.getDbId() is None:
            return
        tags = self.controller.getTags()
        try:
            self.appliTw.item(str(self.controller.getDbId()), tags=tags)
        except TclError:
            pass
        if "hidden" in tags:
            self.hide()

    def insertReceived(self):
        """Called when any view element insert is received by notificaiton
        To be overriden
        """
        pass

    def key(self):
        """Returns a key for sorting this node
        Returns:
            string, basic key: string so alphanumerical sorting will be used
        """
        return str(self.controller.getModelRepr())

    @classmethod
    def list_tuple_to_dict(cls, list_of_tuple):
        """Transforms a list of 2-tuple to a dictionnary
        Args:
            list_of_tuple: a 2-tuple with (key, value)
        Returns:
            A dictionnary with all key-values pair inserted
        """
        ret = dict()
        for key, value in list_of_tuple:
            ret[key] = value
        return ret
