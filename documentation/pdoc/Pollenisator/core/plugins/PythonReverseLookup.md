Module Pollenisator.core.plugins.PythonReverseLookup
====================================================
A plugin to parse python reverse lookup scan

Functions
---------

    
`parse_reverse_python(result_socket)`
:   Parse the result of a reverse lookup from python socket module
        Args:
            result_socket:  the response of the socket module for a dns reverse lookup
        Returns:
            Returns a tuple with (all value are None if not a valid python reverse lookup):
                0. the domain found by the socket module or None if no domain was found.
                1. its ip
    EXAMPLE FILE:
    pythonReverseLookup//10.0.0.1//('foe.lan', [], ['10.0.0.1'])

Classes
-------

`PythonReverseLookup()`
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

    `checkReturnCode(self, _returncode)`
    :   Default check for return code
        Returns:
            Always True. To be overidden

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