"""View for multi selected object clicked. Present an multi modify form to user when interacted with."""

from tkinter import ttk
from core.Views.ViewElement import ViewElement
from core.Components.Settings import Settings
from bson.objectid import ObjectId
from bson.errors import InvalidId

class MultiSelectionView(ViewElement):
    """View for multi selected object clicked. Present an multi modify form to user when interacted with."""

    def __init__(self, appliTw, appViewFrame, mainApp):
        super().__init__(appliTw, appViewFrame, mainApp, None)

    def tagClicked(self, name):
        """Separate callback to apply when a tag button is clicked
        Applies the clicked tag to all selected objects
        Args:
            name: tag name clicked
        """
        return lambda _event: self.appliTw.setTagFromMenubar(name)

    def openModifyWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to update or perform actions on multiple different objects common properties like tags.
        """
        top_panel = self.form.addFormPanel()
        top_panel.addFormButton("Export", self.appliTw.exportSelection)
        top_panel.addFormButton("Hide", self.appliTw.hideSelection)
        top_panel.addFormButton("Custom Command", self.appliTw.customCommand)
        top_panel.addFormButton("Delete", self.appliTw.deleteSelected)
        panTags = self.form.addFormPanel(grid=True)
        registeredTags = Settings.getTags()
        keys = list(registeredTags.keys())
        column = 0
        listOfLambdas = [self.tagClicked(keys[i]) for i in range(len(keys))]
        for registeredTag, color in registeredTags.items():
            s = ttk.Style(self.mainApp.parent)
            s.configure(""+color+".TButton", background=color, foreground="black")
            s.map(""+color+".TButton", foreground=[('active', "dark gray")], background=[('active', color)])
            btn_tag = panTags.addFormButton(registeredTag, listOfLambdas[column], column=column)
            btn_tag.configure(style=""+color+".TButton")
            column += 1
        self.showForm()