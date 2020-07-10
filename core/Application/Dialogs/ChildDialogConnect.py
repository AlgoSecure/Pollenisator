"""Defines a sub-swindow window for connecting to the server"""

import tkinter as tk
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from paramiko.ssh_exception import SSHException
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
from core.Components.mongo import MongoCalendar
from core.Components.FileStorage import FileStorage
from core.Components.Utils import loadClientConfig, saveClientConfig, getValidMarkIconPath, getBadMarkIconPath, getWaitingMarkIconPath


class ChildDialogConnect:
    """
    Open a child dialog of a tkinter application to ask server and login infos
    """
    cvalid_icon = None
    cbad_icon = None
    cwaiting_icon = None

    def validIcon(self):
        """Returns a icon indicating a valid state.
        Returns:
            ImageTk PhotoImage"""
        if self.__class__.cvalid_icon is None:
            self.__class__.cvalid_icon = ImageTk.PhotoImage(
                Image.open(getValidMarkIconPath()))
        return self.__class__.cvalid_icon

    def badIcon(self):
        """Returns a icon indicating a bad state.
        Returns:
            ImageTk PhotoImage"""
        if self.__class__.cbad_icon is None:
            self.__class__.cbad_icon = ImageTk.PhotoImage(
                Image.open(getBadMarkIconPath()))
        return self.__class__.cbad_icon

    def waitingIcon(self):
        """Returns a icon indicating a waiting state.
        Returns:
            ImageTk PhotoImage"""
        if self.__class__.cwaiting_icon is None:
            self.__class__.cwaiting_icon = ImageTk.PhotoImage(
                Image.open(getWaitingMarkIconPath()))
        return self.__class__.cwaiting_icon

    def __init__(self, parent, displayMsg="Connect to backend:"):
        """
        Open a child dialog of a tkinter application to connect to a pollenisator server.

        Args:
            parent: the tkinter parent view to use for this window construction.
            displayMsg: The message that will explain to the user what the form is.
        """
        self.parent = parent
        self.app = tk.Toplevel(parent)
        self.app.resizable(False, False)
        appFrame = ttk.Frame(self.app)
        self.rvalue = None
        self.parent = parent
        self.clientCfg = loadClientConfig()
        lbl = ttk.Label(appFrame, text=displayMsg)
        lbl.pack()
        lbl_hostname = ttk.Label(appFrame, text="Host : ")
        lbl_hostname.pack(side=tk.TOP)
        self.ent_hostname = tk.Entry(
            appFrame, width="20", validate="focusout", validatecommand=self.validateHost)
        self.ent_hostname.insert(tk.END, self.clientCfg["host"])
        self.ent_hostname.bind('<Return>', self.validateHost)
        self.ent_hostname.bind('<KP_Enter>', self.validateHost)
        self.ent_hostname.pack(side=tk.TOP)
        lbl_mongo = ttk.LabelFrame(
            appFrame, text="Mongo:")
        lbl_mongo.pack(padx=10, pady=10, side=tk.TOP,
                       anchor=tk.W, fill=tk.X, expand=tk.YES)
        lbl_port = ttk.Label(lbl_mongo, text="Mongo Port : ")
        lbl_port.grid(row=1, column=0, sticky=tk.E)
        self.ent_port = ttk.Entry(
            lbl_mongo, width="5", validate="focusout", validatecommand=self.validateHost)
        self.ent_port.insert(tk.END, self.clientCfg.get("mongo_port", 27017), )
        self.ent_port.bind('<Return>', self.validateHost)
        self.ent_port.bind('<KP_Enter>', self.validateHost)
        self.ent_port.grid(row=1, column=1, sticky=tk.W)
        self.img_indicator = ttk.Label(lbl_mongo, image=self.waitingIcon())
        self.img_indicator.grid(row=1, column=2)
        lbl_ssl = ttk.Label(lbl_mongo, text="SSL : ")
        lbl_ssl.grid(row=3, column=0, sticky=tk.E)
        self.chk_ssl_val = tk.IntVar(
            value=1 if self.clientCfg.get("ssl", "True") == "True" else 0)
        chk_ssl = ttk.Checkbutton(
            lbl_mongo, variable=self.chk_ssl_val, command=self.validateHost)
        chk_ssl.grid(row=3, column=1, sticky=tk.W)
        lbl_user = ttk.Label(lbl_mongo, text="Mongo username : ")
        lbl_user.grid(row=4, column=0, sticky=tk.E)
        self.ent_user = ttk.Entry(lbl_mongo, width="20")
        self.ent_user.insert(tk.END, self.clientCfg["user"])
        self.ent_user.grid(row=4, column=1, sticky=tk.W)
        lbl_password = ttk.Label(lbl_mongo, text="Mongo password : ")
        lbl_password.grid(row=5, column=0, sticky=tk.E)
        self.ent_password = ttk.Entry(lbl_mongo, show="*", width="20")
        self.ent_password.insert(tk.END, self.clientCfg["password"])
        self.ent_password.grid(row=5, column=1, sticky=tk.W)

        lbl_sftp = ttk.LabelFrame(
            appFrame, text="SFTP:")
        lbl_sftp.pack(padx=10, pady=10, side=tk.TOP,
                      anchor=tk.W, fill=tk.X, expand=tk.YES)
        lbl_port_sftp = ttk.Label(lbl_sftp, text="SFTP Port : ")
        lbl_port_sftp.grid(row=2, column=0, sticky=tk.E)
        self.ent_port_sftp = ttk.Entry(
            lbl_sftp, width="5", validate="focusout", validatecommand=self.validateHost)
        self.ent_port_sftp.insert(
            tk.END, self.clientCfg.get("sftp_port", 22))
        self.ent_port_sftp.grid(row=2, column=1, sticky=tk.W)
        self.ent_port_sftp.bind('<Return>', self.validateHost)
        self.ent_port_sftp.bind('<KP_Enter>', self.validateHost)
        self.img_indicator_sftp = ttk.Label(
            lbl_sftp, image=self.waitingIcon())
        self.img_indicator_sftp.grid(row=2, column=2)

        lbl_user_sftp = ttk.Label(lbl_sftp, text="SFTP username : ")
        lbl_user_sftp.grid(row=6, column=0, sticky=tk.E)
        self.ent_user_sftp = ttk.Entry(lbl_sftp, width="20")
        self.ent_user_sftp.insert(tk.END, self.clientCfg["sftp_user"])
        self.ent_user_sftp.grid(row=6, column=1, sticky=tk.W)
        lbl_password_sftp = ttk.Label(lbl_sftp, text="SFTP Password : ")
        lbl_password_sftp.grid(row=7, column=0, sticky=tk.E)
        self.ent_password_sftp = ttk.Entry(lbl_sftp, show="*", width="20")
        self.ent_password_sftp.insert(tk.END, self.clientCfg["sftp_password"])
        self.ent_password_sftp.grid(row=7, column=1, sticky=tk.W)
        self.ok_button = ttk.Button(appFrame, text="OK", command=self.onOk)
        self.ok_button.pack(pady=10)
        self.validateHost()
        appFrame.pack(ipadx=10, ipady=10)
        try:
            self.app.wait_visibility()
            self.app.transient(parent)
            self.app.grab_set()
        except tk.TclError:
            pass

    def getForm(self):
        """Return the content of this form
        Returns:
            a dict with values: host, mongo_port, sftp_port, ssl (string with value True or False),
                                user, password, sftp_user, sftp_password"""
        config = {}
        config["host"] = self.ent_hostname.get()
        config["mongo_port"] = self.ent_port.get()
        config["sftp_port"] = self.ent_port_sftp.get()
        config["ssl"] = str(self.chk_ssl_val.get() == 1)
        config["user"] = self.ent_user.get()
        config["password"] = self.ent_password.get()
        config["sftp_user"] = self.ent_user_sftp.get()
        config["sftp_password"] = self.ent_password_sftp.get()
        return config

    def trySFTP(self, config):
        """Try to connect to the given host on the given sftp port with the given sftp_user/sftp_password
        Args:
            - config: A dictionnary with thoses values set : host, sftp_port, sftp_user, sftp_password
        Returns:
            - True if connected, False otherwaise
        Raise:
            - ValueError : if the host/port is correct but the authentication failed
            - SSHException : from the paramiko.ssh_exception package if the host/port does not respond to an sftp connection.
        """
        fs = FileStorage(config)
        try:
            fs.open()
        except SSHException as e:
            # SSH unreachable
            raise e
        except ValueError as e:
            # password incorrect
            raise e
        if fs.isConnected():
            fs.close()
            return True
        return False

    def tryConnection(self, config):
        """Try to connect to the given host with mongo and with sftp.
        Args:
            - config: A dictionnary with thoses values set : host, mongo_port, user, password, ssl, sftp_port, sftp_user, sftp_password
        Returns:
            - True if the server is reachable on both mongo and sftp services, False otherwise. Does not test authentication.
        """
        try:
            mongoInstance = MongoCalendar.getInstance()
            res = mongoInstance.connect(config, 500)
        except ServerSelectionTimeoutError:
            return False, False
        except OperationFailure:
            return True, False  # Authentication failed, so mongo was reached
        if res:
            self.img_indicator.config(image=self.validIcon())
            self.img_indicator.image = self.validIcon()
        else:
            self.img_indicator.config(image=self.badIcon())
            self.img_indicator.image = self.badIcon
        try:
            res_sftp = self.trySFTP(config)
        except SSHException:
            self.img_indicator_sftp.config(image=self.badIcon())
            self.img_indicator_sftp.image = self.badIcon()
            return True, False
        except ValueError:
            res_sftp = True  # Authentication failed, so sftp was reached
        if res_sftp:
            self.img_indicator_sftp.config(image=self.validIcon())
            self.img_indicator_sftp.image = self.validIcon()
        return True and True

    def validateHost(self, _event=None):
        """Validate host on both mongo and sftp connections. Change icons on the dialog accordingly.
        Returns:
            - True if the server is reachable on both mongo and sftp services, False otherwise. Does not test authentication.
        """
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.reinitConnection()
        config = self.getForm()
        config["user"] = ""
        config["password"] = ""
        config["sftp_user"] = ""
        config["sftp_password"] = ""
        self.img_indicator.config(image=self.waitingIcon())
        self.img_indicator_sftp.config(image=self.waitingIcon())
        return self.tryConnection(config)

    def onOk(self):
        """
        Called when the user clicked the validation button.
        Try a full connection with authentication to the host given.
        Side effects:
            - Open dialogs if the connection failed. Does not close this dialog.
            - If the connections succeeded : write the client.cfg file accordingly.
        """
        # send the data to the parent
        config = self.getForm()
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.reinitConnection()
        res = True
        try:
            res = mongoInstance.connect(config, 2000)
        except OperationFailure:
            tk.messagebox.showerror(
                "Mongo authentication failed", "Mongo user or password is incorrect", master=self.parent)
            res = False
        except ServerSelectionTimeoutError:
            tk.messagebox.showerror(
                "Mongo connection failed", "The mongo database is not reachable", master=self.parent)
            res = False
        try:
            res = res and self.trySFTP(config)
        except SSHException:
            # Unreachable
            tk.messagebox.showerror(
                "SFTP connection failed", "This sftp port is not open on host.", master=self.parent)
            res = False
        except ValueError:
            # Authentication failed
            tk.messagebox.showerror(
                "SFTP authentication failed", "SFTP user or password is incorrect", master=self.parent)
            res = False
        self.rvalue = False
        if res:
            #  pylint: disable=len-as-condition
            self.rvalue = len(mongoInstance.listCalendars()) > 0
            for key, value in self.clientCfg.items():
                if key not in config.keys():
                    config[key] = value
            saveClientConfig(config)
            self.app.destroy()
