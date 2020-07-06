Module Pollenisator.core.plugins.HttpMethods
============================================
A plugin to parse nmap httpmethods scan

Functions
---------

    
`parse(text)`
:   Args:
            text: raw httpmerhof results
        Returns
            A tuple with 5 values: (every value will be empty if not matching a httpmethods scan)
                0. host scanned
                1. port scanned
                2. proto of the port scanned
                3. service scanned (http or https) 
                4. a list of risky methods found
                5. a list of supported methods found
        Example of output :
    Starting Nmap 7.01 ( https://nmap.org ) at 2019-08-06 16:59 CEST
    Nmap scan report for httprs.primx.fr (172.22.0.6)
    Host is up (0.00040s latency).
    rDNS record for 172.22.0.6: autodiscover.primx.fr
    PORT    STATE SERVICE
    443/tcp open  https
    | http-methods:
    |   Supported Methods: OPTIONS TRACE GET HEAD POST
    |_  Potentially risky methods: TRACE
    MAC Address: 00:E0:81:C1:FD:7E (Tyan Computer)
    Nmap done: 1 IP address (1 host up) scanned in 0.95 seconds

Classes
-------

`HttpMethods()`
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