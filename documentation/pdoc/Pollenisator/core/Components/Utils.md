Module Pollenisator.core.Components.Utils
=========================================
Provide useful functions

Functions
---------

    
`execute(command, timeout=None, printStdout=True)`
:   Execute a bash command and print output
    
    Args:
        command: A bash command
        timeout: a date in the futur when the command will be stopped if still running or None to not use this option, default as None.
        printStdout: A boolean indicating if the stdout should be printed. Default to True.
    
    Returns:
        Return the return code of this command
    
    Raises:
        Raise a KeyboardInterrupt if the command was interrupted by a KeyboardInterrupt (Ctrl+c)

    
`fitNowTime(dated, datef)`
:   Check the current time on the machine is between the given start and end date.
    Args:
        dated: the starting date for the interval
        datef: the ending date for the interval
    Returns:
        True if the current time is between the given interval. False otherwise.
        If one of the args is None, returns False.

    
`getBadMarkIconPath()`
:   Returns:
    a bad mark icon path

    
`getHelpIconPath()`
:   Returns:
    a help icon path

    
`getIconDir()`
:   Returns:
    the icon directory path

    
`getMainDir()`
:   Returns:
    the pollenisator main folder

    
`getValidMarkIconPath()`
:   Returns:
    a validation mark icon path

    
`getWaitingMarkIconPath()`
:   Returns:
    a waiting icon path

    
`isIp(domain_or_networks)`
:   Check if the given scope string is a network ip or a domain.
    Args:
        domain_or_networks: the domain string or the network ipv4 range string
    Returns:
        Returns True if it is a network ipv4 range, False if it is a domain (any other possible case).

    
`isNetworkIp(domain_or_networks)`
:   Check if the given scope string is a network ip or a domain.
    Args:
        domain_or_networks: the domain string or the network ipv4 range string
    Returns:
        Returns True if it is a network ipv4 range, False if it is a domain (any other possible case).

    
`listPlugin()`
:   List the plugins.
    Returns:
        return the list of plugins file names.

    
`loadCfg(cfgfile)`
:   Load a json config file.
    Args:
        cfgfile: the path to a json config file
    Raises:
        FileNotFoundError if the given file does not exist
    Returns:
        Return the json converted values of the config file.

    
`loadClientConfig()`
:   Return data converted from json inside config/client.cfg
    Returns:
        Json converted data inside config/client.cfg

    
`loadPlugin(pluginName)`
:   Load a the plugin python corresponding to the given command name.
    The plugin must start with the command name and be located in plugins folder.
    Args:
        pluginName: the command name to load a plugin for
    
    Returns:
        return the module plugin loaded or default plugin if not found.

    
`loadPluginByBin(binName)`
:   Load a the plugin python corresponding to the given binary name.
    Args:
        binName: the binary name to load a plugin for
    Returns:
        return the module plugin loaded or default plugin if bin name was not found in conf file

    
`loadToolsConfig()`
:   Load tools config file in the config/tools.d/ folder starting with
    config/tools.d/tools.json as default values
    Args:
        cfgfile: the path to a json config file
    Returns:
        Return the json converted values of the config file.

    
`performLookUp(domain)`
:   Uses the socket module to get an ip from a domain.
    
    Args:
        domain: the domain to look for in dns
    
    Returns:
        Return the ip found from dns records, None if failed.

    
`resetUnfinishedTools()`
:   Reset all tools running to a ready state. This is useful if a command was running on a worker and the auto scanning was interrupted.

    
`saveClientConfig(configDict)`
:   Saves data in configDict to config/client.cfg as json
    Args:
        configDict: data to be stored in config/client.cfg

    
`splitRange(rangeIp)`
:   Check if the given range string is bigger than a /24, if it is, splits it in many /24.
    Args:
        rangeIp: network ipv4 range string
    Returns:
        Returns a list of IpNetwork objects corresponding to the range given as /24s.
        If the entry range is smaller than a /24 (like /25 ... /32) the list will be empty.

    
`stringToDate(datestring)`
:   Converts a string with format '%d/%m/%Y %H:%M:%S' to a python date object.
    Args:
        datestring: Returns the date python object if the given string is successfully converted, None otherwise