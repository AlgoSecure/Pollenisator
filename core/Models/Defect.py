"""Defect Model."""

import os
from bson.objectid import ObjectId
from core.Models.Element import Element
from core.Components.mongo import MongoCalendar
from core.Components.FileStorage import FileStorage


class Defect(Element):
    """
    Represents a Defect object that defines a security defect. A security defect is a note added by a pentester on a port or ip which describes a security defect.

    Attributes:
        coll_name: collection name in pollenisator database
    """
    coll_name = "defects"

    def __init__(self, valuesFromDb=None):
        """Constructor
        Args:
            valueFromDb: a dict holding values to load into the object. A mongo fetched defect is optimal.
                        possible keys with default values are : _id (None), parent (None), tags([]), infos({}),
                        ip(""), port(""), proto(""), title(""), ease(""), impact(""), risk(""),
                        redactor("N/A"), type([]), notes(""), proofs([]), index(None)
        """
        if valuesFromDb is None:
            valuesFromDb = {}
        self.proofs = []
        super().__init__(valuesFromDb.get("_id", None), valuesFromDb.get("parent", None), valuesFromDb.get(
            "tags", []), valuesFromDb.get("infos", {}))
        self.initialize(valuesFromDb.get("ip", ""), valuesFromDb.get("port", ""),
                        valuesFromDb.get(
                            "proto", ""), valuesFromDb.get("title", ""),
                        valuesFromDb.get("ease", ""), valuesFromDb.get(
                            "impact", ""),
                        valuesFromDb.get(
                            "risk", ""), valuesFromDb.get("redactor", "N/A"), list(valuesFromDb.get("type", [])),
                        valuesFromDb.get("notes", ""), valuesFromDb.get("proofs", []), valuesFromDb.get("infos", {}),
                        valuesFromDb.get("index", None))

    def initialize(self, ip, port, proto, title="", ease="", impact="", risk="", redactor="N/A", mtype=None, notes="", proofs=None, infos=None, index=None):
        """Set values of defect
        Args:
            ip: defect will be assigned to this IP, can be empty
            port: defect will be assigned to this port, can be empty but requires an IP.
            proto: protocol of the assigned port. tcp or udp.
            title: a title for this defect describing what it is
            ease: ease of exploitation for this defect described as a string 
            impact: impact the defect has on system. Described as a string 
            risk: the combination of impact/ease gives a resulting risk value. Described as a string
            redactor: A pentester that waill be the redactor for this defect.
            mtype: types of this security defects (Application, data, etc...). Default is None
            notes: notes took by pentesters
            proofs: a list of proof files, default to None.
            infos: a dictionnary with key values as additional information. Default to None
            index: the index of this defect in global defect table (only for unassigned defect)
        Returns:
            this object
        """
        self.title = title
        self.ease = ease
        self.impact = impact
        self.risk = risk
        self.redactor = redactor
        self.mtype = mtype if mtype is not None else []
        self.notes = notes
        self.ip = ip
        self.port = port
        self.proto = proto
        self.infos = infos if infos is not None else {}
        self.proofs = proofs if proofs is not None else []
        self.index = index
        return self

    @classmethod
    def getRisk(cls, ease, impact):
        """Dict to find a risk level given an ease and an impact.
        Args:
            ease: ease of exploitation of this defect as as tring
            impact: the defect impact on system security
        Returns:
            A dictionnary of dictionnary. First dict keys are eases of exploitation. Second key are impact strings.
        """
        risk_from_ease = {"Facile": {"Mineur": "Majeur", "Important": "Majeur", "Majeur": "Critique", "Critique": "Critique"},
                          "Modérée": {"Mineur": "Important", "Important": "Important", "Majeur": "Majeur", "Critique": "Critique"},
                          "Difficile": {"Mineur": "Mineur", "Important": "Important", "Majeur": "Majeur", "Critique": "Majeur"},
                          "Très difficile": {"Mineur": "Mineur", "Important": "Mineur", "Majeur": "Important", "Critique": "Important"}}
        return risk_from_ease.get(ease, {}).get(impact, "N/A")

    def delete(self):
        """
        Delete the defect represented by this model in database.
        """
        ret = self._id
        self.rmProofs()
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.delete("defects", {"_id": ret})

    def addInDb(self):
        """
        Add this defect to pollenisator database.
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise 
        """
        base = self.getDbKey()
        # add to base parameters defined or not depending on the lvl.
        # Checking unicity
        mongoInstance = MongoCalendar.getInstance()
        existing = mongoInstance.find("defects", base, False)
        if existing is not None:
            return False, existing["_id"]

        # Those are added to base after tool's unicity verification
        parent = self.getParent()

        base["parent"] = parent
        base["notes"] = self.notes
        base["ease"] = self.ease
        base["impact"] = self.impact
        base["risk"] = self.risk
        base["redactor"] = self.redactor
        base["type"] = list(self.mtype)
        base["proofs"] = self.proofs
        if self.index is not None:
            base["index"] = self.index
        # Get parent for notifications
        res = mongoInstance.insert("defects", base, parent)
        self._id = res.inserted_id
        if self.isAssigned():
            # Set global defect
            base["ip"] = ""
            base["port"] = ""
            base["proto"] = ""
            base["parent"] = ""
            base["notes"] = ""
            glob_defect = Defect(base)
            glob_defect.addInDb()
        return True, res.inserted_id

    def update(self, pipeline_set=None):
        """Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.
        """
        mongoInstance = MongoCalendar.getInstance()
        if pipeline_set is None:
            mongoInstance.update("defects", {"_id": ObjectId(self._id)}, {
                "$set": {"ip": self.ip, "title": self.title, "port": self.port,
                         "proto": self.proto, "notes": self.notes, "ease": self.ease, "impact": self.impact,
                         "risk": self.risk, "redactor": self.redactor, "type": list(self.mtype), "proofs": self.proofs, "infos": self.infos, "index":self.index}})
        else:
            mongoInstance.update("defects", {"_id": ObjectId(self._id)}, {
                "$set": pipeline_set})

    def _getParent(self):
        """
        Return the mongo ObjectId _id of the first parent of this object. For a Defect it is either an ip or a port depending on the Defect's level.

        Returns:
            Returns the parent's ObjectId _id".
        """
        try:
            port = self.port
        except AttributeError:
            port = None
        mongoInstance = MongoCalendar.getInstance()
        if port is None:
            port = ""
        if port == "":
            obj = mongoInstance.find("ips", {"ip": self.ip}, False)
        else:
            obj = mongoInstance.find(
                "ports", {"ip": self.ip, "port": self.port, "proto": self.proto}, False)
        return obj["_id"]

    def calcDirPath(self):
        """Returns a directory path constructed for this defect.
        Returns:
            path as string
        """
        mongoInstance = MongoCalendar.getInstance()
        path_calc = str(mongoInstance.calendarName)+"/"+str(self.ip)
        try:
            port = self.port
        except AttributeError:
            port = None
        if port is not None:
            path_calc += "/"+str(self.port)+"_"+str(self.proto)
        path_calc += "/"+str(self._id)
        return path_calc

    def uploadProof(self, proof_local_path):
        """Upload the given proof file to the server
        Args:
            proof_local_path: a path to a local proof file
        Returns:
            the basename of the file 
        """
        fs = FileStorage()
        fs.open()
        remote_dirpath = self.calcDirPath()
        fs.putProof(proof_local_path, remote_dirpath)
        fs.close()
        return os.path.basename(proof_local_path)

    def getProof(self, index):
        """Download the proof file at given proof index
        Args:
            index: an integer refering to self.proofs list. The proof to be downloaded.
        Returns:
            A string giving the local path of the downloaded proof
        """
        ret = None
        fs = FileStorage()
        fs.open()
        remote_dirpath = self.calcDirPath()
        ret = fs.getProof(remote_dirpath+"/"+self.proofs[index])
        fs.close()
        return ret

    def removeProof(self, index):
        """Removes the proof file at given proof index
        Args:
            index: an integer refering to self.proofs list. The proof to be removed.
        """
        fs = FileStorage()
        fs.open()
        remote_dirpath = self.calcDirPath()
        fs.rmProof(remote_dirpath+"/"+self.proofs[index])
        fs.close()
        self.proofs.remove(self.proofs[index])
        self.update()

    def rmProofs(self):
        """Removes all the proof file in this defect
        """
        proofs = self.proofs
        fs = FileStorage()
        fs.open()
        remote_dirpath = self.calcDirPath()
        fs.rmProofs(remote_dirpath)
        fs.close()
        del proofs
        self.proofs = []
        self.update()

    def __str__(self):
        """
        Get a string representation of a defect.

        Returns:
            Returns the defect +title.
        """
        return self.title

    def getDetailedString(self):
        """Returns a detailed string describing for this defect.
        Returns:
            the defect title. If assigned, it will be prepended with ip and (udp/)port
        """
        ret = ""
        if self.ip is not None:
            ret += str(self.ip)
        if self.proto is not None and self.port is not None:
            if self.proto != "tcp":
                ret += ":"+self.proto+"/"+self.port
            else:
                ret += ":"+self.port
        ret += " "+self.__str__()
        return ret

    def getDbKey(self):
        """Return a dict from model to use as unique composed key.
        Returns:
            A dict (4 keys :"ip", "port", "proto", "title")
        """
        return {"ip": self.ip, "port": self.port, "proto": self.proto, "title": self.title}

    def isAssigned(self):
        """Returns a boolean indicating if this defect is assigned to an ip or is global.
        Returns:
            bool
        """
        return self.ip != ""
