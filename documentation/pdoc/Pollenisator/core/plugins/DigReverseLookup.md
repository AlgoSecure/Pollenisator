Module Pollenisator.core.plugins.DigReverseLookup
=================================================
A plugin to parse a dig scan

Functions
---------

    
`parse_reverse_dig(result_dig)`
:   Parse the results of a reverse lookup by dig
        Args:
            result_dig:  the output of the command dig -x
        Returns:
            Returns the domain found by dig -x as a string or None if no domains was found.

Classes
-------

`DigReverseLookup()`
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

    `checkReturnCode(self, returncode)`
    :   Check if the command was executed successfully using the final exit code.
        Args:
            returncode: the exit code of the command executed.
        Returns:
            bool: True if successful returncode, False otherwise.

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