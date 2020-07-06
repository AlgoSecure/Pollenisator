"""View for ip list object. Present an multi insertion form to user when interacted with."""

from core.Views.ViewElement import ViewElement


class MultipleIpView(ViewElement):
    """View for ip list object. Present an multi insertion form to user when interacted with."""


    def openInsertWindow(self):
        """
        Creates a tkinter form using Forms classes. This form aims to insert many new Ips
        """
        toppanel = self.form.addFormPanel(grid=True)
        toppanel.addFormLabel("IPs")
        toppanel.addFormHelper(
            "Add IP or hostnames that you want to include in the scans\nEach ip/hostname must on a separated line", column=1)
        self.form.addFormText("IPs", r"^(?!https?://).+$",
                              "", None, side="top")
        self.completeInsertWindow()
