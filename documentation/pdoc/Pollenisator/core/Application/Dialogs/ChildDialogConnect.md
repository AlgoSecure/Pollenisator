Module Pollenisator.core.Application.Dialogs.ChildDialogConnect
===============================================================
Defines a sub-swindow window for connecting to the server

Classes
-------

`ChildDialogConnect(parent, displayMsg='Connect to backend:')`
:   Open a child dialog of a tkinter application to ask server and login infos
    
    Open a child dialog of a tkinter application to connect to a pollenisator server.
    
    Args:
        parent: the tkinter parent view to use for this window construction.
        displayMsg: The message that will explain to the user what the form is.

    ### Class variables

    `cbad_icon`
    :

    `cvalid_icon`
    :

    `cwaiting_icon`
    :

    ### Methods

    `badIcon(self)`
    :   Returns a icon indicating a bad state.
        Returns:
            ImageTk PhotoImage

    `getForm(self)`
    :   Return the content of this form
        Returns:
            a dict with values: host, mongo_port, sftp_port, ssl (string with value True or False),
                                user, password, sftp_user, sftp_password

    `onOk(self)`
    :   Called when the user clicked the validation button.
        Try a full connection with authentication to the host given.
        Side effects:
            - Open dialogs if the connection failed. Does not close this dialog.
            - If the connections succeeded : write the client.cfg file accordingly.

    `tryConnection(self, config)`
    :   Try to connect to the given host with mongo and with sftp.
        Args:
            - config: A dictionnary with thoses values set : host, mongo_port, user, password, ssl, sftp_port, sftp_user, sftp_password
        Returns:
            - True if the server is reachable on both mongo and sftp services, False otherwise. Does not test authentication.

    `trySFTP(self, config)`
    :   Try to connect to the given host on the given sftp port with the given sftp_user/sftp_password
        Args:
            - config: A dictionnary with thoses values set : host, sftp_port, sftp_user, sftp_password
        Returns:
            - True if connected, False otherwaise
        Raise:
            - ValueError : if the host/port is correct but the authentication failed
            - SSHException : from the paramiko.ssh_exception package if the host/port does not respond to an sftp connection.

    `validIcon(self)`
    :   Returns a icon indicating a valid state.
        Returns:
            ImageTk PhotoImage

    `validateHost(self)`
    :   Validate host on both mongo and sftp connections. Change icons on the dialog accordingly.
        Returns:
            - True if the server is reachable on both mongo and sftp services, False otherwise. Does not test authentication.

    `waitingIcon(self)`
    :   Returns a icon indicating a waiting state.
        Returns:
            ImageTk PhotoImage