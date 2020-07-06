Module Pollenisator.core.Models.Defect
======================================
Defect Model.

Classes
-------

`Defect(valuesFromDb=None)`
:   Represents a Defect object that defines a security defect. A security defect is a note added by a pentester on a port or ip which describes a security defect.
    
    Attributes:
        coll_name: collection name in pollenisator database
    
    Constructor
    Args:
        valueFromDb: a dict holding values to load into the object. A mongo fetched defect is optimal.
                    possible keys with default values are : _id (None), parent (None), tags([]), infos({}),
                    ip(""), port(""), proto(""), title(""), ease(""), impact(""), risk(""),
                    redactor("N/A"), type([]), notes(""), proofs([]), index(None)

    ### Ancestors (in MRO)

    * core.Models.Element.Element

    ### Class variables

    `coll_name`
    :

    ### Static methods

    `getRisk(ease, impact)`
    :   Dict to find a risk level given an ease and an impact.
        Args:
            ease: ease of exploitation of this defect as as tring
            impact: the defect impact on system security
        Returns:
            A dictionnary of dictionnary. First dict keys are eases of exploitation. Second key are impact strings.

    ### Methods

    `addInDb(self)`
    :   Add this defect to pollenisator database.
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise

    `calcDirPath(self)`
    :   Returns a directory path constructed for this defect.
        Returns:
            path as string

    `delete(self)`
    :   Delete the defect represented by this model in database.

    `getDbKey(self)`
    :   Return a dict from model to use as unique composed key.
        Returns:
            A dict (4 keys :"ip", "port", "proto", "title")

    `getDetailedString(self)`
    :   Returns a detailed string describing for this defect.
        Returns:
            the defect title. If assigned, it will be prepended with ip and (udp/)port

    `getProof(self, index)`
    :   Download the proof file at given proof index
        Args:
            index: an integer refering to self.proofs list. The proof to be downloaded.
        Returns:
            A string giving the local path of the downloaded proof

    `initialize(self, ip, port, proto, title='', ease='', impact='', risk='', redactor='N/A', mtype=None, notes='', proofs=None, infos=None, index=None)`
    :   Set values of defect
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

    `isAssigned(self)`
    :   Returns a boolean indicating if this defect is assigned to an ip or is global.
        Returns:
            bool

    `removeProof(self, index)`
    :   Removes the proof file at given proof index
        Args:
            index: an integer refering to self.proofs list. The proof to be removed.

    `rmProofs(self)`
    :   Removes all the proof file in this defect

    `update(self, pipeline_set=None)`
    :   Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.

    `uploadProof(self, proof_local_path)`
    :   Upload the given proof file to the server
        Args:
            proof_local_path: a path to a local proof file
        Returns:
            the basename of the file