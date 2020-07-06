"""Interface for pysftp"""
import os
import pysftp
from paramiko.ssh_exception import SSHException
import core.Components.Utils as Utils


class FileStorage(object):
    """Interface for pysftp"""

    def __init__(self, cfg=None):
        """
        Constructor
        Args:
            cfg: a dict with keys host, sftp_port, sftp_user, sftp_password.
                If None, reads configuration file in config/client.cfg
                Default to None.
        """
        # /home/barre/Documents/Pollenisator/core/Components/FileStorage.py
        if cfg is None:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_path = os.path.join(dir_path, "../../config/client.cfg")
            cfg = Utils.loadCfg(dir_path)
        self.hostname = cfg["host"]
        self.port = int(cfg["sftp_port"])
        self.username = cfg["sftp_user"]
        self.password = cfg["sftp_password"]
        self.sftp_connection = None

    def isConnected(self):
        """Return True if there is an active pysftp connection
        Return: bool"""
        return self.sftp_connection is not None

    def open(self):
        """Open connection to remote SFTP in directory /files
        Raises:
            SSHException: if the host/port does not respond to ssh connections
            ValueError: if the username/password fail to authenticate"""
        try:
            cnopts = pysftp.CnOpts()
            cnopts.hostkeys = None
            self.sftp_connection = pysftp.Connection(
                self.hostname, port=self.port, username=self.username, password=self.password, cnopts=cnopts)
            if self.sftp_connection is not None:
                # temporarily chdir to public
                self.sftp_connection.chdir('/files')
            else:
                print("Impossible to connect to sftp.")
        except SSHException as e:
            self.sftp_connection = None
            if "[Errno 111] Connection refused" in str(e):
                raise e
            elif "Authentication failed" in str(e):
                raise ValueError()

    def close(self):
        """Close sftp connection. If not open, does nothing."""
        if self.sftp_connection is not None:
            try:
                self.sftp_connection.close()
            except SSHException:
                pass

    def putResult(self, local_path, remote_path):
        """Upload local given file in the local results directory into remote /results/ at the same path
        Args:
            local_path: local file path in the Pollenisator/results directory
            remote_path: remote desired path with /results/ in it.
        """
        if self.sftp_connection is not None:
            remote = "results/"+remote_path.split("/results/")[1]
            self._put(local_path, remote)

    def putProof(self, local_path, remote_path):
        """Upload local given file into remote proofs/ at the same path
        Args:
            local_path: local file path
            remote_path: remote desired path that will be added to the /proofs/ folder
        """
        if self.sftp_connection is not None:
            remote = "proofs/"+str(remote_path)+"/" + \
                os.path.basename(local_path)
            self._put(local_path, remote)

    def getProof(self, remote_path):
        """Download remote given proof to local results directory keeping its remote local path.
        Args:
            remote_path: remote desired path excluding the /files/proofs/ forced directory part
        Return: None if failed, the local path to the downloaded file (string) otherwise.
        """
        if self.sftp_connection is not None:
            remote = str(remote_path)
            local_path = os.path.dirname(os.path.realpath(__file__))
            local_path = os.path.join(local_path, "../../results/")
            local_path += os.path.dirname(remote_path)
            self.sftp_connection.chdir('/files/proofs/')
            res = self._get(remote, local_path)
            if not res:
                return None
            return os.path.join(local_path, os.path.basename(remote_path))
        return None

    def getResults(self):
        """Download all remote results to local results directory keeping theire remote local path.
        """
        if self.sftp_connection is not None:
            # /home/barre/Documents/Pollenisator/core/Components/FileStorage.py
            dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_path = os.path.join(dir_path, "../../results/")
            self.sftp_connection.chdir('/files/results/')
            self.sftp_connection.get_r(
                './', dir_path, preserve_mtime=True)  # get recursif

    def getToolResult(self, outputDir):
        """Download remote given tool result to local results directory keeping its remote local path.
        Args:
            outputDir: the file output directory path in remote and local location (should be matching)
        Returns: 
            None if failed, the local path to the downloaded file otherwise.
        Raises:
            FileNotFoundError: file not found if remote path or local path does not exist.
        """
        if self.sftp_connection is not None:
            # /home/barre/Documents/Pollenisator/core/Components/FileStorage.py
            dir_path = os.path.dirname(os.path.realpath(__file__))
            dir_path = os.path.join(dir_path, "../../results/", outputDir)
            self.sftp_connection.chdir('/files/results/')
            try:
                try:
                    os.makedirs(os.path.dirname(dir_path))
                except FileExistsError:
                    pass
                self.sftp_connection.get(
                    outputDir, dir_path, preserve_mtime=True)
            except FileNotFoundError as e:
                print("File not found : remote:" +
                      str(outputDir) + "-> local:"+str(dir_path))
                raise e
            return dir_path
        return None

    def rmDbResults(self, dbName):
        """Remove all remote results for the given database.
        Args:
            dbName: the database name you want to remove all results of.
        """
        if self.sftp_connection is not None:
            path = '/files/results/'+str(dbName)
            self._rm(path)

    def rmDbProofs(self, dbName):
        """Remove all remote proofs for the given database.
        Args:
            dbName: the database name you want to remove all proofs of.
        """
        if self.sftp_connection is not None:
            path = '/files/proofs/'+str(dbName)
            self._rm(path)

    def rmProof(self, path):
        """Remove remote proof given the remote proof path.
        Args:
            path: the remote proof path without the /files/proofs/
        """
        if self.sftp_connection is not None:
            remote = "proofs/"+str(path)
            try:
                self.sftp_connection.remove(remote)
                if len(self.sftp_connection.listdir(os.path.dirname(remote))) == 0:
                    self.sftp_connection.rmdir(os.path.dirname(remote))
            except SSHException as e:
                print(str(e))
            except FileNotFoundError as e:
                pass

    def rmProofs(self, defect_iid):
        """Remove remote proofs for the given defect db id.
        Args:
            defect_iid: the mongo db id of a defect. All its proof will be removed.
        """
        if self.sftp_connection is not None:
            remote = "proofs/"+str(defect_iid)
            try:
                self._rm(remote)
            except SSHException as e:
                print(str(e))

    def _rm(self, path):
        """recursively Delete remote file(s) in the given path.
        Args:
            path: remote path to delete.
        """
        if self.sftp_connection is not None:
            try:
                files = self.sftp_connection.listdir(path)
            except FileNotFoundError:
                files = []
            for f in files:
                filepath = os.path.join(path, f)
                try:
                    self.sftp_connection.remove(filepath)
                except IOError:
                    self._rm(filepath)
            try:
                self.sftp_connection.rmdir(path)
            except IOError:
                pass

    def _get(self, remote_path, local_path):
        """download remote file at the given remote path to local path.
        Args:
            remote_path: remote path to file.
            local_path: desired destination for the download.
        Returns: True if download was successful, False otherwise.
        """
        if self.sftp_connection is not None:
            currdir = os.getcwd()
            try:
                os.makedirs(local_path)
            except FileExistsError:
                pass
            os.chdir(local_path)
            try:
                self.sftp_connection.get(remote_path, preserve_mtime=True)
            except FileNotFoundError:
                return False
            os.chdir(currdir)
            return True
        return False

    def _put(self, local_path, remote_path):
        """Upload local file to remote path.
        Args:
            local_path: local file path
            remote_path: remote path to upload. /files/ wille be prepended.
        """
        if self.sftp_connection is not None:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            pysftp.cd(dir_path)
            remote_path = os.path.dirname(remote_path)
            self.sftp_connection.makedirs("/files/"+remote_path)
            self.sftp_connection.chdir('/files/'+remote_path)
            filename = os.path.basename(local_path)
            try:
                # upload file to files/ on remote
                self.sftp_connection.put(
                    local_path, filename, None, True, preserve_mtime=True)
            except IOError:
                print("Log: remote path does not exist : " +
                      str(local_path) + " -> remote:"+str(filename))
            # Marked as duplicate except by pylint but still following the pysftp.put doc.
            except OSError:
                print("Log: Local path does not exist : " +
                      str(local_path) + " -> remote:"+str(filename))
