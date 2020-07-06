Module Pollenisator.core.Components.FileStorage
===============================================
Interface for pysftp

Classes
-------

`FileStorage(cfg=None)`
:   Interface for pysftp
    
    Constructor
    Args:
        cfg: a dict with keys host, sftp_port, sftp_user, sftp_password.
            If None, reads configuration file in config/client.cfg
            Default to None.

    ### Methods

    `close(self)`
    :   Close sftp connection. If not open, does nothing.

    `getProof(self, remote_path)`
    :   Download remote given proof to local results directory keeping its remote local path.
        Args:
            remote_path: remote desired path excluding the /files/proofs/ forced directory part
        Return: None if failed, the local path to the downloaded file (string) otherwise.

    `getResults(self)`
    :   Download all remote results to local results directory keeping theire remote local path.

    `getToolResult(self, outputDir)`
    :   Download remote given tool result to local results directory keeping its remote local path.
        Args:
            outputDir: the file output directory path in remote and local location (should be matching)
        Returns: 
            None if failed, the local path to the downloaded file otherwise.
        Raises:
            FileNotFoundError: file not found if remote path or local path does not exist.

    `isConnected(self)`
    :   Return True if there is an active pysftp connection
        Return: bool

    `open(self)`
    :   Open connection to remote SFTP in directory /files
        Raises:
            SSHException: if the host/port does not respond to ssh connections
            ValueError: if the username/password fail to authenticate

    `putProof(self, local_path, remote_path)`
    :   Upload local given file into remote proofs/ at the same path
        Args:
            local_path: local file path
            remote_path: remote desired path that will be added to the /proofs/ folder

    `putResult(self, local_path, remote_path)`
    :   Upload local given file in the local results directory into remote /results/ at the same path
        Args:
            local_path: local file path in the Pollenisator/results directory
            remote_path: remote desired path with /results/ in it.

    `rmDbProofs(self, dbName)`
    :   Remove all remote proofs for the given database.
        Args:
            dbName: the database name you want to remove all proofs of.

    `rmDbResults(self, dbName)`
    :   Remove all remote results for the given database.
        Args:
            dbName: the database name you want to remove all results of.

    `rmProof(self, path)`
    :   Remove remote proof given the remote proof path.
        Args:
            path: the remote proof path without the /files/proofs/

    `rmProofs(self, defect_iid)`
    :   Remove remote proofs for the given defect db id.
        Args:
            defect_iid: the mongo db id of a defect. All its proof will be removed.