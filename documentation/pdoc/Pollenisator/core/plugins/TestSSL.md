Module Pollenisator.core.plugins.TestSSL
========================================
A plugin to parse testssl.sh

Functions
---------

    
`parseWarnings(file_opened)`
:   Parse the result of a testssl json output file
        Args:
            file_opened:  the opened file reference
    
        Returns:
            Returns a tuple with (None values if not matching a testssl output):
                - a list of string for each testssl NOT ok, WARN, or MEDIUM warnings
                - a dict of targeted objects with database id as key and a unique key as a mongo search pipeline ({})

Classes
-------

`TestSSL()`
:   Parent base plugin to be inherited
    Attributes:
        autoDetect: indicating to auto-detect that this plugin is able to auto detect.

    ### Ancestors (in MRO)

    * core.plugins.plugin.Plugin

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

    `changeCommand(self, command, outputDir, toolname)`
    :   Summary: Complete the given command with the tool output file option and filename absolute path.
        Args:
            * command : the command line to complete
            * outputDir : the directory where the output file must be generated
            * toolname : the tool name (to be included in the output file name)
        Return:
            The command complete with the tool output file option and filename absolute path.

    `checkReturnCode(self, _returncode)`
    :   Default check for return code
        Returns:
            Always True. To be overidden

    `getFileOutputArg(self)`
    :   Return the expected argument for the tool that will create an output file.
        Returns:
            Returns a string containing the argument to look for, with a space at the beginning and at the end.

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