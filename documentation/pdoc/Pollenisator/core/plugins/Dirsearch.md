Module Pollenisator.core.plugins.Dirsearch
==========================================
A plugin to parse a dirsearch scan

Functions
---------

    
`parse_dirsearch_file(notes)`
:   Parse a dirsearch resulting raw text file
    Args:
        notes: the dirsearch raw text
    Returns:
        a dict with scanned hosts has keys and another dict as value:
            this dict has scanned ports as keys and another dict as value:
                this dict has 3 keys:
                    * service: "http" or "https"
                    * paths: a list of path found on port
                    * statuscode: a list of status code matching the list of paths

Classes
-------

`Dirsearch()`
:   Parent base plugin to be inherited
    Attributes:
        autoDetect: indicating to auto-detect that this plugin is able to auto detect.
    
    Constructor

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

    `getActions(self, toolmodel)`
    :   Summary: Add buttons to the tool view.
        Args:
            toolmodel : the tool model opened in the pollenisator client.
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

    `openInBrowser(self)`
    :   Callback of action  Open 200 in browser
        Open all 200 status code in browser as tabs. If more that 10 status code 200 are to be opened, shows a warning.
        Args:
            _event: not used but mandatory