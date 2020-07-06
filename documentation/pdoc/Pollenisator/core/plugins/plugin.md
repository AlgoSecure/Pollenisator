Module Pollenisator.core.plugins.plugin
=======================================
A registry for all subclasses of Plugin

Functions
---------

    
`register_class(target_class)`
:   Register the given class
    Args:
        target_class: type <class>

Classes
-------

`MetaPlugin(name, bases, class_dict)`
:   type(object_or_name, bases, dict)
    type(object) -> the object's type
    type(name, bases, dict) -> a new type

    ### Ancestors (in MRO)

    * builtins.type

`Plugin()`
:   Parent base plugin to be inherited
    Attributes:
        autoDetect: indicating to auto-detect that this plugin is able to auto detect.

    ### Class variables

    `autoDetect`
    :

    ### Methods

    `Parse(self, file_opened, **_kwargs)`
    :   Parse a opened file to extract information
        Args:
            file_opened: the open file
            _kwargs: not used
        Returns:
            a tuple with 4 values (All set to None if Parsing wrong file): 
                0. notes: notes to be inserted in tool giving direct info to pentester
                1. tags: a list of tags to be added to tool 
                2. lvl: the level of the command executed to assign to given targets
                3. targets: a list of composed keys allowing retrieve/insert from/into database targerted objects.

    `autoDetectEnabled(self)`
    :   Returns a boolean indicating if this plugin is able to recognize a file to be parsed by it.
        Returns: 
            bool

    `centralizeFile(self, filepath, remoteDir)`
    :   Upload the result file to sftp
        Args:
            filepath: local result file path
            remoteDir: remote path

    `changeCommand(self, command, outputDir, toolname)`
    :   Summary: Complete the given command with the tool output file option and filename absolute path.
        Args:
            * command : the command line to complete
            * outputDir : the directory where the output file must be generated
            * toolname : the tool name (to be included in the output file name)
        Return:
            The command completed with the tool output file option and filename absolute path.

    `checkReturnCode(self, _returncode)`
    :   Default check for return code
        Returns:
            Always True. To be overidden

    `getActions(self, _toolmodel)`
    :   Summary: Add buttons to the tool view.
        Args:
            * toolmodel : the tool model opened in the pollenisator client.
        Return:
            A dictionary with buttons text as key and function callback as value.

    `getFileOutputArg(self)`
    :   Returns the command line paramater giving the output file
        Returns:
            string

    `getFileOutputExt(self)`
    :   Returns the expected file extension for this command result file
        Returns:
            string

    `getFileOutputPath(self, commandExecuted)`
    :   Returns the output file path given in the executed command using getFileOutputArg
        Args:
            commandExecuted: the command that was executed with an output file inside.
        Returns:
            string: the path to file created

    `getFilePath(self, commandExecuted)`
    :   Returns the output file path given in the executed command using getFileOutputArg
        Args:
            commandExecuted: the command that was executed with an output file inside.
        Returns:
            string: the path to file created