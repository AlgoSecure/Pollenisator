Module Pollenisator.core.Components.mongo
=========================================
Handle mongo database connection and add shortcut functions to common stuff.

Classes
-------

`MongoCalendar()`
:   Centralize all direct contacts with the database.
    
    DO NOT USE THIS CONSTRUCTOR IT IS A
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

    ### Static methods

    `getInstance()`
    :   Singleton Static access method.

    ### Methods

    `aggregate(self, collection, pipelines=None)`
    :   Wrapper for the pymongo aggregate.
        
        Args:
            collection: the collection to aggregate.
            pipelines: the mongo pipeline for aggregation. Default to None which means empty list pipeline
        
        Returns:
            Return the pymongo result of the aggregate function

    `aggregateFromDb(self, db, collection, pipelines=None)`
    :   aggregate something in the database.
        Args:
            db: the database name to search in
            collection: the collection to search in
            pipelines: the mongo pipeline for aggregation. Default to None which means empty list pipeline
        Returns:
            Return the pymongo result of the find command for the command collection

    `attach(self, observer)`
    :   Attach an observer to the database. All attached observers will be notified when a modication is done to a calendar through the methods presented below.
        
        Args:
            observer: the observer that implements a notify(collection, iid, action) function

    `connect(self, config=None, timeoutInMS=500)`
    :   Connect the mongo client to the database using the login provided and ssl certificates if ssl is activated.
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

    `connectToDb(self, calendarName)`
    :   Connect to the pentest database given by calendarName (pentestName).
        
        Args:
            calendarName: the pentest name to which you want to connect

    `copyDb(self, ToCopyName='', fromCopyName='')`
    :   Copy a database.
        
        Args:
            ToCopyName: the output calendar will have this name. If default empty string is given, a user window prompt will be used.
            fromCopyName: the calendar name to be copied. If default empty string is given, the opened calendar will be used.
        
        Returns:
            Returns the output database name or None if the copy failed.

    `delete(self, collection, pipeline, many=False)`
    :   Wrapper for the pymongo delete_one or delete_many. Then notify observers.
        
        Args:
            collection: the collection that holds the document to delete
            pipeline: the document caracteristics to search for deletion.
            many: a boolean defining if eventually many documents can be deleted at once. (If False, only zero or one document will be deleted.). Default to False
        
        Returns:
            Return the pymongo result of the delete_one or delete_many function.

    `deleteFromDb(self, db, collection, pipeline, many=False, notify=False)`
    :   aggregate something in the database.
        Args:
            db: the target database name 
            collection: the collection that holds the document to delete
            pipeline: the document caracteristics to search for deletion.
            many: a boolean defining if eventually many documents can be deleted at once. (If False, only zero or one document will be deleted.). Default to False
            notify: a boolean asking for all client to be notified of this update. Default to False.
        Returns:
            Return the pymongo result of the find command for the command collection

    `dettach(self, observer)`
    :   Dettach the given observer from the database.
        
        Args:
            observer: the observer to detach

    `doDeleteCalendar(self, calendarName)`
    :   Remove the given calendar name from the database.
        
        Args:
            calendarName: the calendar name to delete.

    `dumpDb(self, dbName, collection='')`
    :   Export a database dump into the exports/ folder as a gzip archive.
        It uses the mongodump utily installed with mongodb-org-tools
        
        Args:
            dbName: the database name to dump
            collection: (Opt.) the collection to dump.

    `find(self, collection, pipeline=None, multi=True)`
    :   Wrapper for the pymongo find and find_one.
        
        Args:
            collection: the collection to search for
            pipeline: the document caracteristics to search for, default to None which means no filtering.
            multi: a boolean defining if eventually many documents can be found at once. (If False, only zero or one document will be found). Default to True.
        
        Returns:
            Return the pymongo result of the find or find_one function.

    `findInDb(self, db, collection, pipeline=None, multi=True)`
    :   find something in the database.
        Args:
            collection: the collection to search for
            pipeline: the document caracteristics to search for, default to None which means no filtering.
            multi: a boolean defining if eventually many documents can be found at once. (If False, only zero or one document will be found). Default to True.
        Returns:
            Return the pymongo result of the find command for the command collection

    `getRegisteredCommands(self, worker_name)`
    :   Return the commands list registered by the given worker name
        Args:
            worker_name: the wworker shortname.

    `getWorkers(self)`
    :   Return workers documents from database
        Returns:
            Mongo result of workers. Cursor of dictionnary.

    `hasACalendarOpen(self)`
    :   Return wether or not a calendar is open.
        
        Returns:
            Return True if a calendar is open, False otherwise.

    `importCommands(self, filename)`
    :   Import a database dump into a calendar database.
            It uses the mongorestore utily installed with mongodb-org-tools
        
        Args:
            filename: the gzip archive name that was exported to be reimported.
        
        Returns:
            returns True if the import is successfull, False

    `importDatabase(self, filename)`
    :   Import a database dump into a calendar database.
            It uses the mongorestore utily installed with mongodb-org-tools
        
        Args:
            filename: the gzip archive name that was exported to be reimported.
        
        Returns:
            returns True if the import is successfull, False

    `insert(self, collection, values, parent='')`
    :   Wrapper for the pymongo insert_one. Then notify observers.
        
        Args:
            collection: the collection that will hold the document to insert
            values: the document to insert into the given collection
            parent: not used, default to ''. Was used to give info about parent node
        
        Returns:
            Return the pymongo result of the insert_one function.

    `insertInDb(self, db, collection, values, notify=False)`
    :   insert something in the database after ensuring connection.
        Args:
            db: the database name to use
            collection: the collection that holds the document to insert
            values: the document to insert into the given collection
            parent: not used, default to ''. Was used to give info about parent node
            notify: a boolean asking for all client to be notified of this update. Default to False.
        Returns:
            Return the pymongo result of the find command for the command collection

    `isUserConnected(self)`
    :   Return True if the user is able to list databases. False otherwise.
        Returns: bool

    `listCalendars(self)`
    :   Return the list of pollenisator databases.
        Raises:
            Raise Exception if client is not connected to database
        Returns:
            None if the server connection is not established. A list of string with pollenisator databases.

    `notify(self, db, collection, iid, action, parentId='')`
    :   Notify all observers of the modified record from database.
        Uses the observer's notify implementation. This implementation must take the same args as this.
        
        Args:
            collection: the collection where a document has been modified
            iid: the mongo ObjectId of the document that has been modified
            action: the type of modification performed on this document ("insert", "update" or "delete")
            parentId: (not used) default to "", a node parent id as str

    `registerCalendar(self, saveAsName, askDeleteIfExists=True, autoconnect=True)`
    :   Register a new calendar into database.
        
        Args:
            saveAsName: the calendar name to register
            askDeleteIfExists: boolean to ask the user for a deletion in case of an already existing calendar with the same name.
                                If false, and the case appends, calendar will not be registered. Default is True.
            autoconnect: boolean indicating if the database should connect to the calendar after it is registered. Default to True.
        
        Returns:
            Returns True if calendar was successfully registered, False otherwise.

    `registerCommands(self, worker_name, command_names)`
    :   Update or insert the worker name with given commands.
        Args:
            worker_name: the worker shortname.
            command_names: a list of commands that the worker want to register.

    `reinitConnection(self)`
    :   Reset client connection

    `removeInactiveWorkers(self)`
    :   Remove workers that did not sent a heart beat in 30 sec.

    `removeWorker(self, worker_name)`
    :   Remove the given worker shortname from database.
        Args:
            worker_name: the worker shortname to be deleted from database.

    `update(self, collection, pipeline, updatePipeline, many=False, notify=True)`
    :   Wrapper for the pymongo update and update_many functions. Then notify observers.
        
        Args:
            collection: the collection that holds the document to update
            pipeline: a first "match" pipeline mongo to select which document to update
            updatePipeline: a second "action" pipeline mongo to apply changes to the selected document(s)
            many: a boolean defining if eventually many documents can be modified at once. (If False, only zero or one document will be updated.). Default to False
            notify: a boolean asking for all client to be notified of this update. Default to True.
        Returns:
            Return the pymongo result of the update or update_many function.

    `updateInDb(self, db, collection, pipeline, updatePipeline, many=False, notify=False)`
    :   update something in the database.
        Args:
            db: the database name where the object to update is
            collection: the collection that holds the document to update
            pipeline: a first "match" pipeline mongo to select which document to update
            updatePipeline: a second "action" pipeline mongo to apply changes to the selected document(s)
            many: a boolean defining if eventually many documents can be modified at once. (If False, only zero or one document will be updated.). Default to False
            notify: a boolean asking for all client to be notified of this update. Default to False.
        Returns:
            Return the pymongo result of the find command for the command collection

    `updateWorkerLastHeartbeat(self, worker_hostname)`
    :   Update a worker last heart beat sent
        Args:
            worker_hostname: the worker shortname to update.

    `validateCalendarName(self, calendarName)`
    :   Check the database name to see if it usable.
        Checks mongo and pollenisator name overlapping.
        Check space and dot in name.
        Check existing pollenisator pentest database names.
        Returns: a boolean