Module Pollenisator.core.plugins.Knockpy
========================================
A plugin to parse knockpy scan

Functions
---------

    
`parse_knockpy_line(line)`
:   Parse one line of knockpy result file
        Args:
            line:  one line of knockpy result file
    
        Returns:
            a tuple with 3 values:
                0. the ip found by knockpy on this line or None if no domain exists on this line.
                1. the domain found by knockpy on this line or None if no domain exists on this line.
                2. a boolean indicating that knockpy marked this domain as alias

Classes
-------

`Knockpy()`
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