"""A registry for all subclasses of Plugin"""
REGISTRY = {}

def register_class(target_class):
    """Register the given class
    Args:
        target_class: type <class>
    """
    REGISTRY[target_class.__name__] = target_class()


class MetaPlugin(type):
    def __new__(meta, name, bases, class_dict):
        cls = type.__new__(meta, name, bases, class_dict)
        if name not in REGISTRY:
            register_class(cls)
        return cls


class Plugin(metaclass=MetaPlugin):
    """ Parent base plugin to be inherited
    Attributes:
        autoDetect: indicating to auto-detect that this plugin is able to auto detect.
    """
    autoDetect = True  # Authorize parsing function be used for autodetection

    def autoDetectEnabled(self):
        """Returns a boolean indicating if this plugin is able to recognize a file to be parsed by it.
        Returns: 
            bool
        """
        return self.__class__.autoDetect

    def getFileOutputArg(self):
        """Returns the command line paramater giving the output file
        Returns:
            string
        """
        return " > "

    def getFileOutputExt(self):
        """Returns the expected file extension for this command result file
        Returns:
            string
        """
        return ".log.txt"

    def changeCommand(self, command, outputDir, toolname):
        """
        Summary: Complete the given command with the tool output file option and filename absolute path.
        Args:
            * command : the command line to complete
            * outputDir : the directory where the output file must be generated
            * toolname : the tool name (to be included in the output file name)
        Return:
            The command completed with the tool output file option and filename absolute path.
        """
        # default is append at the end
        if self.getFileOutputArg() not in command:
            return command + self.getFileOutputArg()+outputDir+toolname
        return command

    def getFileOutputPath(self, commandExecuted):
        """Returns the output file path given in the executed command using getFileOutputArg
        Args:
            commandExecuted: the command that was executed with an output file inside.
        Returns:
            string: the path to file created
        """
        return commandExecuted.split(self.getFileOutputArg())[-1].strip()

    def checkReturnCode(self, _returncode):
        """Default check for return code
        Returns:
            Always True. To be overidden
        """
        return True

    def Parse(self, file_opened, **_kwargs):
        """
        Parse a opened file to extract information
        Args:
            file_opened: the open file
            _kwargs: not used
        Returns:
            a tuple with 4 values (All set to None if Parsing wrong file): 
                0. notes: notes to be inserted in tool giving direct info to pentester
                1. tags: a list of tags to be added to tool 
                2. lvl: the level of the command executed to assign to given targets
                3. targets: a list of composed keys allowing retrieve/insert from/into database targerted objects.
        """
        notes = ""
        tags = ["todo"]
        notes = file_opened.read()
        return notes, tags, "wave", {"wave": None}

    def getFilePath(self, commandExecuted):
        """Returns the output file path given in the executed command using getFileOutputArg
        Args:
            commandExecuted: the command that was executed with an output file inside.
        Returns:
            string: the path to file created
        """
        return self.getFileOutputPath(commandExecuted)

    def centralizeFile(self, filepath, remoteDir):
        """Upload the result file to sftp
        Args:
            filepath: local result file path
            remoteDir: remote path
        """
        from core.Components.FileStorage import FileStorage
        fs = FileStorage()
        fs.open()
        fs.putResult(filepath, remoteDir)
        fs.close()

    def getActions(self, _toolmodel):
        """
        Summary: Add buttons to the tool view.
        Args:
            * toolmodel : the tool model opened in the pollenisator client.
        Return:
            A dictionary with buttons text as key and function callback as value.
        """
        return {}
