Module Pollenisator.pollenisator
================================
@author: Fabien Barré for AlgoSecure
# Date: 11/07/2017
# Major version released: 09/2019
# @version: 1.0

Functions
---------

    
`main()`
:   Main function. Start pollenisator application

Classes
-------

`GracefulKiller(app)`
:   Signal handler to shut down properly.
    
    Attributes:
        kill_now: a boolean that can checked to know that it's time to stop.
    
    Constructor. Hook the signals SIGINT and SIGTERM to method exitGracefully
    
    Args:
        app: The appli object to stop

    ### Class variables

    `kill_now`
    :

    ### Methods

    `exitGracefully(self, _signum, _frame)`
    :   Set the kill_now class attributes to True. Call the onClosing function of the application given at init.
        
        Args:
            signum: not used
            frame: not used