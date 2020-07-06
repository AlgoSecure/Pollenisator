Module Pollenisator.core.Components.Settings
============================================
Hold functions to interact with the settings

Classes
-------

`Settings()`
:   Represents the settings of pollenisator.
    There are three level of settings:
        * local settings: stored in a file under ../../config/settings.cfg
        * pentest db settings: stored in the pentest database under settings collection
        * global settings: stored in the pollenisator database under settings collection
    
    Load the tree types of settings and stores them in dictionnaries

    ### Static methods

    `getPentestTypes()`
    :   Returns pentest types and associeted defect type defined in settings.
        Returns:
            If none are defined returns {"Web":["Socle", "Application", "Données", "Politique"], "LAN":["Infrastructure", "Active Directory", "Données", "Politique"]}
            otherwise returns a dict with defined key values

    `getTags()`
    :   Returns tags defined in settings.
        Returns:
            If none are defined returns {"todo":"orange", "P0wned!":"red", "Interesting":"dark green", "Uninteresting":"sky blue", "Neutral":"white"}
            otherwise returns a dict with defined key values

    ### Methods

    `boundToMousewheel(self, _event)`
    :   Called when the main view canvas is focused.
        Bind the command scrollbar button on linux to the main view canvas
        Args:
            _event: not used but mandatory

    `getFavoriteTerm(self)`
    :   Returns favorite terminal configured 
        Returns:
            If none are defined returns first in the list of terms
            Otherwise returns the favorite terminal configured

    `getPentestType(self)`
    :   Return selected database pentest type.
        Returns:
            Open database pentest type. string "None" if not defined

    `getPentesters(self)`
    :   Return a list of pentesters registered for open pentest database
        Returns:
            List of pentesters names

    `getTerms(self)`
    :   Returns terminals configured 
        Returns:
            If none are defined returns ['''gnome-terminal --window --title="Pollenisator terminal" -- bash --rcfile setupTerminalForPentest.sh''',
             '''xfce4-terminal -x bash --rcfile setupTerminalForPentest.sh''',
             '''xterm -e bash --rcfile setupTerminalForPentest.sh''']
            otherwise returns a list with defined  values

    `initUI(self, parent)`
    :   Create settings widgets and initialize them
        Args:
            parent: parent tkinter container widget

    `on_ok(self)`
    :   Callback on click save button. loads some data and calls save.
        Args:
            parent: parent tkinter container widget

    `reloadSettings(self)`
    :   Reload local, database and global settings.

    `reloadUI(self)`
    :   Reload all settings and refresh view with values

    `save(self)`
    :   Save all the settings (local, database and global)

    `saveLocalSettings(self)`
    :   Save local settings to conf file

    `setFavoriteTerm(self)`
    :   Change favorite term

    `unboundToMousewheel(self, _event)`
    :   Called when the main view canvas is unfocused.
        Unbind the command scrollbar button on linux to the main view canvas
        Args:
            _event: not used but mandatory