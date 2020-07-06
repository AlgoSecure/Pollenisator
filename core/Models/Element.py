"""Element parent Model. Common ground for every model"""

from core.Components.mongo import MongoCalendar
from bson.objectid import ObjectId
from core.Components.Settings import Settings

class Element(object):
    """
    Parent element for all model. This class should only be inherited.

    Attributes:
        coll_name:  collection name in pollenisator database
    """
    coll_name = None

    def __init__(self, _id, parent, tags, infos):
        """
        Constructor to be inherited. Child model will all use this constructor.

        Args:
            _id: mongo database id
            parent: a parent mongo id object for this model.
            tags: a list of tags applied on this object
            infos: a dicitonnary of custom information 
        """
        # Initiate a cachedIcon for a model, not a class.
        self._id = _id
        self.tags = tags
        self.parent = parent
        self.infos = infos
        self.cachedIcon = None

    @classmethod
    def fetchObject(cls, pipeline):
        """Fetch one element from database and return the CommandGroup object 
        Args:
            pipeline: a Mongo search pipeline (dict)
        Returns:
            Returns the model object or None if nothing matches the pipeline.
        """
        mongoInstance = MongoCalendar.getInstance()
        d = mongoInstance.find(cls.coll_name, pipeline, False)
        if d is None:
            return d
        # disabling this error as it is an abstract function
        return cls(d)  #  pylint: disable=no-value-for-parameter

    @classmethod
    def fetchObjects(cls, pipeline):
        """Fetch many commands from database and return a Cursor to iterate over model objects
        Args:
            pipeline: a Mongo search pipeline (dict)
        Returns:
            Returns a cursor to iterate on model objects
        """
        mongoInstance = MongoCalendar.getInstance()
        ds = mongoInstance.find(cls.coll_name, pipeline, True)
        for d in ds:
            # disabling this error as it is an abstract function
            yield cls(d)  #  pylint: disable=no-value-for-parameter

    def getId(self):
        """Returns the mongo id  of this element.
        Returns:
            bson.objectid.ObjectId
        """
        return self._id

    def getParent(self):
        """Returns the mongo id  of this element parent.
        Returns:
            bson.objectid.ObjectId
        """
        if self.parent is None:
            try:
                self.parent = self._getParent()  # pylint: disable=assignment-from-none
            except TypeError:
                return None
        return self.parent

    def _getParent(self):
        """
        To be overriden
        Return the mongo ObjectId _id of the first parent of this object. 
        Returns:
            Returns the parent's ObjectId _id".
        Returns:
            None
        """
        return None

    def delete(self):
        """
        To be overriden
        Delete the object represented by this model in database.
        """
        # pass

    def addInDb(self):
        """
        To be overriden
        Add this model to pollenisator database.
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise 
        """
        # pass

    def update(self, _pipeline_set=None):
        """
        To be overriden
        Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.
        """
        # pass

    def getTags(self):
        """Returns the tag list assigned to this element.
        Returns:
            list of string
        """
        return self.tags


    def getTagsGroups(self):
        """Returns groups of tags that may not be applied at the same time
        Returns:
            List of list of strings
        """
        tags = Settings.getTags()
        return [tags, ["hidden"]]

    def addTag(self, newTag, overrideGroupe=True):
        """Add the given tag to this object.
        Args:
            newTag: a new tag as a string to be added to this model tags
            overrideGroupe: Default to True. If newTag is in a group with a tag already assigned to this object, it will replace this old tag.
        """
        tags = self.getTags()
        if newTag not in tags:
            for group in self.getTagsGroups():
                if newTag in group:
                    i = 0
                    len_tags = len(tags)
                    while i < len_tags:
                        if tags[i] in group:
                            if overrideGroupe:
                                tags.remove(tags[i])
                                i -= 1
                            else:
                                continue
                        len_tags = len(tags)
                        i += 1
            tags.append(newTag)
            self.tags = tags
            self.update()

    def delTag(self, tagToDelete):
        """Delete the given tag in this object.
        Args:
            tagToDelete: a tag as a string to be deleted from this model tags
        """
        tags = self.getTags()
        mongoInstance = MongoCalendar.getInstance()
        if tagToDelete in tags:
            del tags[tags.index(tagToDelete)]
            notify = tagToDelete != "hidden"
            mongoInstance.update(self.__class__.coll_name, {"_id": ObjectId(self._id)}, {
                "$set": {"tags": tags}}, False, notify)

    def setTags(self, tags):
        """Change all tags for the given new ones  and update database
        Args:
            tags: a list of tag string
        """
        self.tags = tags
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.update(self.__class__.coll_name, {"_id": ObjectId(self._id)}, {
            "$set": {"tags": tags}})

    def getDetailedString(self):
        """To be inherited and overriden
        Returns a detailed string describing this element. Calls __str__ of children by default.
        Returns:
            string
        """
        return str(self)

    def updateInfos(self, newInfos):
        """Change all infos stores in self.infos with the given new ones and update database.
        Args:
            newInfos: A new dictionnary of custom information
        """
        if "" in newInfos:
            del newInfos[""]
        self.infos.update(newInfos)
        self.update()
