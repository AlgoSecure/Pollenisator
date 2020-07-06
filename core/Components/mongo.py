"""Handle mongo database connection and add shortcut functions to common stuff."""
import os
import ssl
import tkinter.messagebox
import tkinter.simpledialog
import tkinter.filedialog
import datetime
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError, OperationFailure
import core.Components.Utils as Utils


class MongoCalendar:
    # pylint: disable=unsubscriptable-object
    """
    Centralize all direct contacts with the database.
    """
    __instances = {}

    @staticmethod
    def getInstance():
        """ Singleton Static access method.
        """
        pid = os.getpid()  # HACK : One mongo per process.
        instance = MongoCalendar.__instances.get(pid, None)
        if instance is None:
            MongoCalendar()
        return MongoCalendar.__instances[pid]

    def __init__(self):
        """ DO NOT USE THIS CONSTRUCTOR IT IS A
        Virtually private constructor.  Use MongoCalendar.getInstance()
        Args:
            client: a MongoClient instance or None
            host: the host where the database is running
            user: a user login to the database
            password: a password corresponding with the user to connect to the database
            ssl: A boolean string "True" or "False" indicating if ssl should be used to connect with the database.
            calendarName: the calendar name the db has connected to. Or None if not connected to any calendar.
            ssldir: The string path to a folder where all the ssl certificates are to be found.
            db: The database to the client last connected.
            forbiddenNames: A list of names forbidden for calendars because they are reserved by mongo, celery or this application. ("admin", "config", "local", "broker_pollenisator", "pollenisator")
        Raises:
            Exception if it is instanciated.
        """
        pid = os.getpid()  # HACK : One mongo per process.
        if MongoCalendar.__instances.get(pid, None) is not None:
            raise Exception("This class is a singleton!")
        else:
            self.client = None
            self.host = ""
            self.password = ""
            self.user = ""
            self.ssl = ""
            self.port = ""
            self.calendarName = None
            self.ssldir = ""
            self.db = None
            self.forbiddenNames = ["admin", "config", "local",
                                   "broker_pollenisator", "pollenisator"]
            self._observers = []
            MongoCalendar.__instances[pid] = self

    def reinitConnection(self):
        """Reset client connection"""
        self.client = None

    def getWorkers(self):
        """Return workers documents from database
        Returns:
            Mongo result of workers. Cursor of dictionnary."""
        return self.findInDb("pollenisator", "workers")

    def removeInactiveWorkers(self):
        """Remove workers that did not sent a heart beat in 30 sec."""
        nowTime = datetime.datetime.now()
        deltaTime = nowTime - datetime.timedelta(seconds=30)
        res = self.deleteFromDb("pollenisator", "workers", {
            "last_heartbeat": {"$lt": deltaTime}}, True, True)
        print("Removed inactive workers:"+str(res.deleted_count))


    def updateWorkerLastHeartbeat(self, worker_hostname):
        """Update a worker last heart beat sent
        Args:
            worker_hostname: the worker shortname to update.
        """
        self.updateInDb("pollenisator", "workers", {"name": worker_hostname}, {
                        "$set": {"last_heartbeat": datetime.datetime.now()}})

    def connect(self, config=None, timeoutInMS=500):
        """
        Connect the mongo client to the database using the login provided and ssl certificates if ssl is activated.
        Args:
            config: A dictionnary with client.cfg config values (host, mongo_port, password, user, ssl).
                    Default to None. If None, the client.cfg file will be read.
            timeoutInMs: milliseconds to wait before timeout. Default to 500ms.
        Raises:
            ServerSelectionTimeoutError: if unable to connect to the mongo database
            OperationFailure: if unable to authenticate using user/password.
        Returns:
            None if not connected
            False if connection failed
            True if connected succeeded
        """
        if self.client is not None:
            return
        dir_path = os.path.dirname(os.path.realpath(__file__))
        cfg = config if config is not None else Utils.loadCfg(
            os.path.join(dir_path, "../../config/client.cfg"))
        try:
            self.host = str(cfg["host"])
            self.port = str(cfg.get("mongo_port", 27017))
            self.password = str(cfg["password"])
            self.user = str(cfg["user"])
            self.ssl = str(cfg["ssl"])
            connectionString = ""
            if self.user != "":
                connectionString = self.user+':'+self.password+'@'
            self.calendarName = None
            try:
                if cfg["ssl"] == "True":
                    self.ssldir = os.path.abspath(
                        os.path.join(dir_path, "../../ssl/"))
                    self.client = MongoClient('mongodb://'+connectionString+self.host+":"+self.port, ssl=True, ssl_certfile=os.path.join(
                        self.ssldir, "client.pem"), ssl_cert_reqs=ssl.CERT_REQUIRED, ssl_ca_certs=os.path.join(self.ssldir, "ca.pem"), serverSelectionTimeoutMS=timeoutInMS, socketTimeoutMS=2000, connectTimeoutMS=2000)
                else:
                    self.client = MongoClient(
                        'mongodb://'+connectionString+self.host+":"+self.port, serverSelectionTimeoutMS=timeoutInMS)
                server_info = self.client.server_info()
                return True and self.client is not None and server_info is not None
            except ServerSelectionTimeoutError as e:  # Unable to connect
                raise e
            except OperationFailure as e:  #  Authentication failed
                raise e
        except KeyError as e:
            raise e
        return False

    def isUserConnected(self):
        """Return True if the user is able to list databases. False otherwise.
        Returns: bool"""
        return self.listCalendars() is not None

    def connectToDb(self, calendarName):
        """
        Connect to the pentest database given by calendarName (pentestName).

        Args:
            calendarName: the pentest name to which you want to connect
        """
        try:
            if self.client is None:
                self.connect()
                if self.client is None:
                    raise IOError()
            self.calendarName = calendarName
            if calendarName is not None:
                self.db = self.client[calendarName]
        except IOError as e:
            print("Failed to connect." + str(e))
            print("Please verify that the mongod service is running on host " +
                  self.host + " and has a user mongAdmin with the correct password.")
            self.client = None

    def removeWorker(self, worker_name):
        """Remove the given worker shortname from database.
        Args:
            worker_name: the worker shortname to be deleted from database."""
        print("Remove worker as offline received")
        self.deleteFromDb("pollenisator", "workers", {
            "name": worker_name}, False, True)

    def registerCommands(self, worker_name, command_names):
        """Update or insert the worker name with given commands.
        Args:
            worker_name: the worker shortname.
            command_names: a list of commands that the worker want to register."""
        try:
            if self.client is None:
                self.connect()
                if self.client is None:
                    raise IOError("Failed to register commands")
            res = self.findInDb("pollenisator", "workers", {
                "name": worker_name}, False)
            worker_shortname = worker_name.split("@")[-1]
            if res is not None:
                print("UPDATE COMMANDS")
                self.updateInDb("pollenisator", "workers",
                                {"name": worker_name}, {"$set": {"registeredCommands": command_names}}, False, True)
            else:
                print("INSERT COMMANDS")
                self.insertInDb("pollenisator", "workers", {
                    "name": worker_name, "shortname": worker_shortname, "registeredCommands": command_names}, '', True)
            print("Registered commands "+str(command_names) +
                  " for  "+str(worker_name))
        except IOError as e:
            print("Failed to connect." + str(e))
            print("Please verify that the mongod service is running on host " +
                  self.host + " and has a user mongAdmin with the correct password.")
            self.client = None

    def getRegisteredCommands(self, worker_name):
        """Return the commands list registered by the given worker name
        Args:
            worker_name: the wworker shortname.
        """
        try:
            if self.client is None:
                self.connect()
                if self.client is None:
                    raise ServerSelectionTimeoutError()
            worker_res = self.findInDb("pollenisator", "workers", {
                "name": worker_name}, False)
            if worker_res is not None:
                return worker_res["registeredCommands"]
        except ServerSelectionTimeoutError as e:
            print("Failed to connect." + str(e))
            print("Please verify that the mongod service is running on host " +
                  self.host + " and has a user mongAdmin with the correct password.")
            self.client = None

    def attach(self, observer):
        """
        Attach an observer to the database. All attached observers will be notified when a modication is done to a calendar through the methods presented below.

        Args:
            observer: the observer that implements a notify(collection, iid, action) function
        """
        self._observers.append(observer)

    def dettach(self, observer):
        """
        Dettach the given observer from the database.

        Args:
            observer: the observer to detach
        """
        try:
            self._observers.remove(observer)
        except ValueError:
            pass

    def notify(self, db, collection, iid, action, parentId=""):
        """
        Notify all observers of the modified record from database.
        Uses the observer's notify implementation. This implementation must take the same args as this.

        Args:
            collection: the collection where a document has been modified
            iid: the mongo ObjectId of the document that has been modified
            action: the type of modification performed on this document ("insert", "update" or "delete")
            parentId: (not used) default to "", a node parent id as str
        """
        if self._observers is not None:
            if len(self._observers) > 1:
                for observer in self._observers:
                    observer.notify(db, collection, iid, action)
            else:
                self.client["pollenisator"]["notifications"].insert_one(
                    {"iid": iid, "db": db, "collection": collection, "action": action, "parent": parentId})

    def update(self, collection, pipeline, updatePipeline, many=False, notify=True):
        """
        Wrapper for the pymongo update and update_many functions. Then notify observers.

        Args:
            collection: the collection that holds the document to update
            pipeline: a first "match" pipeline mongo to select which document to update
            updatePipeline: a second "action" pipeline mongo to apply changes to the selected document(s)
            many: a boolean defining if eventually many documents can be modified at once. (If False, only zero or one document will be updated.). Default to False
            notify: a boolean asking for all client to be notified of this update. Default to True.
        Returns:
            Return the pymongo result of the update or update_many function.
        """
        return self._update(self.calendarName, collection, pipeline, updatePipeline, many=many, notify=notify)

    def updateInDb(self, db, collection, pipeline, updatePipeline, many=False, notify=False):
        """
        update something in the database.
        Args:
            db: the database name where the object to update is
            collection: the collection that holds the document to update
            pipeline: a first "match" pipeline mongo to select which document to update
            updatePipeline: a second "action" pipeline mongo to apply changes to the selected document(s)
            many: a boolean defining if eventually many documents can be modified at once. (If False, only zero or one document will be updated.). Default to False
            notify: a boolean asking for all client to be notified of this update. Default to False.
        Returns:
            Return the pymongo result of the find command for the command collection
        """
        self.connect()
        return self._update(db, collection, pipeline, updatePipeline, many=many, notify=notify)

    def _update(self, dbName, collection, pipeline, updatePipeline, many=False, notify=True):
        """
        Wrapper for the pymongo update and update_many functions. Then notify observers  if notify is true.

        Args:
            dbName: the database name to use
            collection: the collection that holds the document to update
            pipeline: a first "match" pipeline mongo to select which document to update
            updatePipeline: a second "action" pipeline mongo to apply changes to the selected document(s)
            many: a boolean defining if eventually many documents can be modified at once. (If False, only zero or one document will be updated.). Default to False
            notify: a boolean asking for all client to be notified of this update. Default to True.
        Returns:
            Return the pymongo result of the update or update_many function.
        """
        self.connect()
        db = self.client[dbName]
        if many:
            res = db[collection].update_many(
                pipeline, updatePipeline)
            elems = db[collection].find(pipeline)
            if notify:
                for elem in elems:
                    self.notify(dbName, collection, elem["_id"], "update")
        else:
            res = db[collection].update(pipeline, updatePipeline)
            elem = db[collection].find_one(pipeline)
            if elem is not None:
                if notify:
                    self.notify(dbName, collection, elem["_id"], "update")
        return res

    def insert(self, collection, values, parent=''):
        """
        Wrapper for the pymongo insert_one. Then notify observers.

        Args:
            collection: the collection that will hold the document to insert
            values: the document to insert into the given collection
            parent: not used, default to ''. Was used to give info about parent node

        Returns:
            Return the pymongo result of the insert_one function.
        """
        return self._insert(self.calendarName, collection, values, True, parent)

    def insertInDb(self, db, collection, values, _parent='', notify=False):
        """
        insert something in the database after ensuring connection.
        Args:
            db: the database name to use
            collection: the collection that holds the document to insert
            values: the document to insert into the given collection
            parent: not used, default to ''. Was used to give info about parent node
            notify: a boolean asking for all client to be notified of this update. Default to False.
        Returns:
            Return the pymongo result of the find command for the command collection
        """
        self.connect()
        return self._insert(db, collection, values, notify)

    def _insert(self, dbName, collection, values, notify=True, parentId=''):
        """
        Perform insertion in the database".
        Args:
            dbName: the database name object to use
            collection: the collection that holds the document to insert
            values: the document to insert into the given collection
            notify: a boolean asking for all client to be notified of this update. Default to True.
            parentId: not used, default to ''. Was used to give info about parent node

        Returns:
            Return the pymongo result of the find command for the command collection
        """
        self.connect()
        db = self.client[dbName]
        res = db[collection].insert_one(values)
        if notify:
            self.notify(dbName, collection,
                        res.inserted_id, "insert", parentId)
        return res

    def find(self, collection, pipeline=None, multi=True):
        """
        Wrapper for the pymongo find and find_one.

        Args:
            collection: the collection to search for
            pipeline: the document caracteristics to search for, default to None which means no filtering.
            multi: a boolean defining if eventually many documents can be found at once. (If False, only zero or one document will be found). Default to True.

        Returns:
            Return the pymongo result of the find or find_one function.
        """
        if pipeline is None:
            pipeline = {}
        return self._find(self.db, collection, pipeline, multi)

    def findInDb(self, db, collection, pipeline=None, multi=True):
        """
        find something in the database.
        Args:
            collection: the collection to search for
            pipeline: the document caracteristics to search for, default to None which means no filtering.
            multi: a boolean defining if eventually many documents can be found at once. (If False, only zero or one document will be found). Default to True.
        Returns:
            Return the pymongo result of the find command for the command collection
        """
        if pipeline is None:
            pipeline = {}
        self.connect()
        dbMongo = self.client[db]
        return self._find(dbMongo, collection, pipeline, multi)

    def _find(self, db, collection, pipeline=None, multi=True):
        """
        Wrapper for the pymongo find and find_one.

        Args:
            db: the database name to search in
            collection: the collection to search in
            pipeline: the document caracteristics to search for, default to None which means no filtering.
            multi: a boolean defining if eventually many documents can be found at once. (If False, only zero or one document will be found). Default to True.

        Returns:
            Return the pymongo result of the find or find_one function.
        """
        if pipeline is None:
            pipeline = {}
        self.connect()
        try:
            if multi:
                res = db[collection].find(pipeline)
            else:
                res = db[collection].find_one(pipeline)
        except TypeError:
            return None
        return res

    def aggregate(self, collection, pipelines=None):
        """
        Wrapper for the pymongo aggregate.

        Args:
            collection: the collection to aggregate.
            pipelines: the mongo pipeline for aggregation. Default to None which means empty list pipeline

        Returns:
            Return the pymongo result of the aggregate function
        """
        if pipelines is None:
            pipelines = []
        return self._aggregate(self.db, collection, pipelines)

    def aggregateFromDb(self, db, collection, pipelines=None):
        """
        aggregate something in the database.
        Args:
            db: the database name to search in
            collection: the collection to search in
            pipelines: the mongo pipeline for aggregation. Default to None which means empty list pipeline
        Returns:
            Return the pymongo result of the find command for the command collection
        """
        if pipelines is None:
            pipelines = []
        self.connect()
        dbMongo = self.client[db]
        return self._aggregate(dbMongo, collection, pipelines)

    def _aggregate(self, db, collection, pipelines=None):
        """
        Wrapper for the pymongo aggregate.

        Args:
            db: the database to search in as mongo object
            collection: the collection to aggregate as str.
            pipelines: the mongo pipeline for aggregation.  Default to None which means empty list pipeline

        Returns:
            Return the pymongo result of the aggregate function
        """
        if pipelines is None:
            pipelines = []
        self.connect()
        return db[collection].aggregate(pipelines)

    def delete(self, collection, pipeline, many=False):
        """
        Wrapper for the pymongo delete_one or delete_many. Then notify observers.

        Args:
            collection: the collection that holds the document to delete
            pipeline: the document caracteristics to search for deletion.
            many: a boolean defining if eventually many documents can be deleted at once. (If False, only zero or one document will be deleted.). Default to False

        Returns:
            Return the pymongo result of the delete_one or delete_many function.
        """
        return self._delete(self.calendarName, collection, pipeline, many, True)

    def deleteFromDb(self, db, collection, pipeline, many=False, notify=False):
        """
        aggregate something in the database.
        Args:
            db: the target database name 
            collection: the collection that holds the document to delete
            pipeline: the document caracteristics to search for deletion.
            many: a boolean defining if eventually many documents can be deleted at once. (If False, only zero or one document will be deleted.). Default to False
            notify: a boolean asking for all client to be notified of this update. Default to False.
        Returns:
            Return the pymongo result of the find command for the command collection
        """
        self.connect()
        return self._delete(db, collection, pipeline, many, notify)

    def _delete(self, dbName, collection, pipeline, many=False, notify=True):
        """
        Wrapper for the pymongo delete_one or delete_many. Then notify observers.

        Args:
            dbName: the database to search in
            collection: the collection that holds the document to delete
            pipeline: the document caracteristics to search for deletion.
            many: a boolean defining if eventually many documents can be deleted at once. (If False, only zero or one document will be deleted.). Default to False
            notify: a boolean asking for all client to be notified of this update. Default to True.
        Returns:
            Return the pymongo result of the delete_one or delete_many function.
        """
        self.connect()
        db = self.client[dbName]
        res = None
        if many:
            elems = db[collection].find(pipeline)
            if notify:
                for elem in elems:
                    self.notify(dbName, collection, elem["_id"], "delete")
            res = db[collection].delete_many(pipeline)
        else:
            elem = db[collection].find_one(pipeline)
            if elem is not None:
                if notify:
                    self.notify(dbName, collection, elem["_id"], "delete")
                res = db[collection].delete_one(pipeline)
        return res

    def listCalendars(self):
        """Return the list of pollenisator databases.
        Raises:
            Raise Exception if client is not connected to database
        Returns:
            None if the server connection is not established. A list of string with pollenisator databases.
        """
        ret = []
        try:
            if self.client is None:
                self.connect()
                if self.client is None:
                    raise Exception()
            calendars = self.findInDb("pollenisator", "calendars")
            try:
                for calendar in calendars:
                    ret.append(calendar["nom"])
            except OperationFailure:
                print("The connected user has no rights")
                return None
        except ServerSelectionTimeoutError as e:
            print("Failed to connect." + str(e))
            print("Please verify that the mongod service is running on host " +
                  self.host + " and has a user mongAdmin with the correct password.")
            self.client = None
            return None
        return ret

    def hasACalendarOpen(self):
        """
        Return wether or not a calendar is open.

        Returns:
            Return True if a calendar is open, False otherwise.
        """
        return self.calendarName is not None

    def doDeleteCalendar(self, calendarName):
        """
        Remove the given calendar name from the database.

        Args:
            calendarName: the calendar name to delete.
        """
        result = self.deleteFromDb(
            "pollenisator", "calendars", {"nom": calendarName})
        if result is not None:
            if result.deleted_count == 1:
                self.client.drop_database(calendarName)
                tkinter.messagebox.showinfo(
                    "Success", "Deleted from "+"calendars"+" \""+str(calendarName)+"\"")
                return

        tkinter.messagebox.showinfo(
            "Error", "Deleting "+str(calendarName)+" is not allowed because it is not a database.")

    def validateCalendarName(self, calendarName):
        """Check the database name to see if it usable.
        Checks mongo and pollenisator name overlapping.
        Check space and dot in name.
        Check existing pollenisator pentest database names.
        Returns: a boolean"""
        # check for forbidden names
        if calendarName.strip().lower() in self.forbiddenNames:
            msg = "This name is forbidden."
            return False, msg
        elif "." in calendarName.strip():
            msg = "The name cannot contain a dot (.)."
            return False, msg
        elif " " in calendarName.strip():
            msg = "The name cannot contain a space."
            return False, msg
        calendars = [x.lower() for x in self.listCalendars()]
        if calendarName.strip().lower() in calendars:
            msg = "A database with the same name already exists."
            return False, msg
        return True, ""

    def registerCalendar(self, saveAsName, askDeleteIfExists=True, autoconnect=True):
        """
        Register a new calendar into database.

        Args:
            saveAsName: the calendar name to register
            askDeleteIfExists: boolean to ask the user for a deletion in case of an already existing calendar with the same name.
                                If false, and the case appends, calendar will not be registered. Default is True.
            autoconnect: boolean indicating if the database should connect to the calendar after it is registered. Default to True.

        Returns:
            Returns True if calendar was successfully registered, False otherwise.
        """
        oldConnection = self.calendarName
        authorized, msg = self.validateCalendarName(saveAsName.strip().lower())
        # check for forbidden names
        if not authorized:
            tkinter.messagebox.showinfo("add database attempt:", msg)
            return False
        else:
            # check if already exists
            self.connectToDb("pollenisator")
            if self.db.calendars.find_one({"nom": saveAsName.strip()}) is not None and askDeleteIfExists:
                authorized = tkinter.messagebox.askyesno(
                    "Already exists", "A database already exists with that name, override (cannot be reversed)?")
                if not authorized:
                    msg = "The database has not been overwritten choose a different name to save it."
                else:
                    self.doDeleteCalendar(saveAsName.strip())
            # If authorized to registered from previous tests
            if authorized:
                # insert in database  calendars
                self.connectToDb("pollenisator")
                self.db.calendars.insert({"nom": saveAsName.strip()})
                self.connectToDb(saveAsName.strip())
            if autoconnect:
                self.connectToDb(saveAsName.strip())
            else:
                self.connectToDb(oldConnection)
        return True

    def copyDb(self, ToCopyName="", fromCopyName=""):
        """
        Copy a database.

        Args:
            ToCopyName: the output calendar will have this name. If default empty string is given, a user window prompt will be used.
            fromCopyName: the calendar name to be copied. If default empty string is given, the opened calendar will be used.

        Returns:
            Returns the output database name or None if the copy failed.
        """
        if self.calendarName is None and fromCopyName == "":
            tkinter.messagebox.showinfo(
                "Copy database failed:", "You must open a database before duplicating it.")
            return None
        if fromCopyName == "" and self.calendarName is not None:
            fromCopyName = self.calendarName
        if ToCopyName == "":
            ToCopyName = tkinter.simpledialog.askstring(
                "Copy name", "New copy of "+fromCopyName+" database name :")
        if ToCopyName is not None:
            succeed = self.registerCalendar(
                ToCopyName, True, True)
            if succeed:
                self.client.admin.command('copydb',
                                          fromdb=fromCopyName,
                                          todb=ToCopyName)
            else:
                return None

            return ToCopyName
        else:
            tkinter.messagebox.showinfo("Copy database canceled", "Canceled.")
            return None

    def dumpDb(self, dbName, collection=""):
        """
        Export a database dump into the exports/ folder as a gzip archive.
        It uses the mongodump utily installed with mongodb-org-tools

        Args:
            dbName: the database name to dump
            collection: (Opt.) the collection to dump.
        """
        from core.Components.Utils import execute
        dir_path = os.path.dirname(os.path.realpath(__file__))
        out_path = os.path.join(
            dir_path, "../../exports/", dbName if collection == "" else dbName+"_"+collection)
        connectionString = '' if self.user == '' else "-u "+self.user + \
            " -p "+self.password + " --authenticationDatabase admin "
        cmd = "mongodump "+connectionString+"--host " + \
            self.host+"  --db "+dbName+" --archive="+out_path+".gzip --gzip"
        if collection.strip() != "":
            cmd += " -c "+str(collection).strip()
        if self.ssl == "True":
            cmd += " --ssl --sslPEMKeyFile "+self.ssldir+"/client.pem --sslCAFile " + \
                self.ssldir+"/ca.pem --sslAllowInvalidHostnames"
        execute(cmd)

    def importDatabase(self, filename):
        """
        Import a database dump into a calendar database.
            It uses the mongorestore utily installed with mongodb-org-tools

        Args:
            filename: the gzip archive name that was exported to be reimported.

        Returns:
            returns True if the import is successfull, False
        """
        from core.Components.Utils import execute
        success = self.registerCalendar(os.path.splitext(
            os.path.basename(filename))[0], True, False)
        if success:
            connectionString = '' if self.user == '' else "-u "+self.user + \
                " -p "+self.password + " --authenticationDatabase admin "
            cmd = "mongorestore "+connectionString+"--host " + \
                self.host+" --archive="+filename+" --gzip"
            if self.ssl == "True":
                cmd += " --ssl --sslPEMKeyFile "+self.ssldir+"/client.pem --sslCAFile " + \
                    self.ssldir+"/ca.pem --sslAllowInvalidHostnames"
            execute(cmd, None, False)
        return success

    def importCommands(self, filename):
        """
        Import a database dump into a calendar database.
            It uses the mongorestore utily installed with mongodb-org-tools

        Args:
            filename: the gzip archive name that was exported to be reimported.

        Returns:
            returns True if the import is successfull, False
        """
        from core.Components.Utils import execute
        if not os.path.isfile(filename):
            raise IOError("File does not exist")
        connectionString = '' if self.user.strip() == '' else "-u "+self.user + \
            " -p "+self.password + " --authenticationDatabase admin "
        cmd = "mongorestore "+connectionString+"--host " + \
            self.host+" --archive="+filename+" --gzip"
        if self.ssl == "True":
            cmd += " --ssl --sslPEMKeyFile "+self.ssldir+"/client.pem --sslCAFile " + \
                self.ssldir+"/ca.pem --sslAllowInvalidHostnames"

        execute(cmd, None, False)
        return True
