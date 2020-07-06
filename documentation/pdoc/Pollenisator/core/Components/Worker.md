Module Pollenisator.core.Components.Worker
==========================================
Handle Workers specific work

Classes
-------

`Worker(name)`
:   Represents one worker state.
    
    Constructor.
    Args:
        name: The celery worker name

    ### Methods

    `getNbOfLaunchedCommand(self, commandName)`
    :   Get the total number of running commands which have the given command name
        
        Args:
            commandName: The command name to count running tools.
        
        Returns:
            Return the total of running tools with this command's name as an integer.

    `hasRegistered(self, launchableTool)`
    :   Returns a bool indicating if the worker has registered a given tool
        Args:
            launchableTool: the tool object to check registration of.
        Returns:
            Return bool.

    `hasSpaceFor(self, launchableTool)`
    :   Check if this worker has space for the given tool. (this checks the command and every group of commands max_thred settings)
        
        Args:
            launchableTool: a tool documents fetched from database that has to be launched
        
        Returns:
            Return True if a command of the tool's type can be launched on this worker, False otherwise.