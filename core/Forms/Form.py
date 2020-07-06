"""Describe custom tkinter widgets or extended tkinter widgets"""
import tkinter as tk

class Form(object):
    """
    Describe custom tkinter widgets or extended tkinter widgets
    Form field empty, should be inherited to create a new Form.
    """

    def __init__(self, name):
        """
        Constructor for an empty form.

        Args:
            name: the button text.
        """
        self.name = name
        self.val = tk.StringVar()
        self.kwargs = dict()

    def constructView(self, parent):
        """
        Create the view inside the parent view given
        Args:
            parent: parent tkinter container widget
        """
        # pass

    def getValue(self):
        """
        Return the form value. Required for a form.

        Returns:
            Return None
        """
        return None

    def setValue(self, newval):
        """
        Set the form value. Required for a form.
        Args:
           newval: new value to be setted
        """
        self.val.set(newval)

    def checkForm(self):
        """
        Check if this form is correctly filled.

        Returns:
            {
                "correct": True if the form is correctly filled, False otherwise.
                "msg": A message indicating what is not correctly filled.
            }
        """
        return True, ""

    def setFocus(self):
        """Defines what item should be focused inside the form widget"""
        return

    def getKw(self, key, default):
        """Read and delete the given key inside the stored kwargs.
        If key does not exist, default will be returned.
        Args:
            key: the key matching the wanted value in kwargs
            default: a default value to be returned in case the key does not exist.
        """
        if key in self.kwargs:
            v = self.kwargs[key]
            del self.kwargs[key]
            return v
        return default