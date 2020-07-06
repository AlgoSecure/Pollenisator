"""Controller for model object. Mostly handles conversion between mongo data and python objects"""

from bson.objectid import ObjectId


class ControllerElement:
    """Controller for model object. Mostly handles conversion between mongo data and python objects"""
    def __init__(self, model):
        """Constructor
        Args:
            model: Any instance of classe that inherits core.Models.Element"""
        self.model = model

    def getDbId(self):
        """Returns the mongo database id of the model object
        Returns:
            bson.objectid ObjectId or None if self.model is None
        """
        if self.model is not None:
            return self.model.getId()
        return None

    def getParent(self):
        """Return the parent object database id of the model. E.G a port would returns its parent IP mongo id
        Returns:
            None if model is None
            bson.objectid ObjectId of the parent object
        """
        if self.model is None:
            return None
        return self.model.getParent()

    def doDelete(self):
        """Ask the model to delete itself from database
        """
        self.model.delete()

    def actualize(self):
        """Ask the model to reload its data from database
        """
        if self.model is not None:
            self.model = self.model.__class__.fetchObject(
                {"_id": ObjectId(self.model.getId())})

    def update(self):
        """Update object in database with model data
        """
        self.model.update()

    def updateInfos(self, infos):
        """Update object in database with given dictionnary
        Args:
            infos: a dictionnary with updated values for this object.
        """
        self.model.updateInfos(infos)

    def getModelRepr(self):
        """Returns a string representation of the model
        Returns:
            a string conversion of the model
        """
        try:
            return str(self.model)
        except TypeError:
            return "Error"

    def getTags(self):
        """Returns a list of string secribing tags
        Returns:
            list of string
        """
        if self.model is None:
            return
        return self.model.tags

    def setTags(self, tags):
        """Set the model tags to given tags
        Args:
            tags: a list of string describing tags.
        """
        self.model.setTags(tags)

    def delTag(self, tag):
        """Delete the given tag name in model if it has it
        Args:
            tag: astring describing a tag.
        """
        self.model.delTag(tag)

    def addTag(self, newTag, override=True):
        """Add the given tag name in model if it has it
        Args:
            newTag: a string describing a tag.
            override: if True (default), will force add of the new tag and remove tag of the same tag group.
                      if False, will not add this tag.
        """
        self.model.addTag(newTag, override)

    def getDetailedString(self):
        """Return a string describing the model with more info than getModelRepr. E.G a port goes from "tcp/80" to "IP.IP.IP.IP tcp/80"
        Returns:
            a detailed string conversion of the model
        """
        return self.model.getDetailedString()

    def getType(self):
        """Return a string describing the type of object
        Returns:
            "element" """
        return "element"