Module Pollenisator.core.Models.Element
=======================================
Element parent Model. Common ground for every model

Classes
-------

`Element(_id, parent, tags, infos)`
:   Parent element for all model. This class should only be inherited.
    
    Attributes:
        coll_name:  collection name in pollenisator database
    
    Constructor to be inherited. Child model will all use this constructor.
    
    Args:
        _id: mongo database id
        parent: a parent mongo id object for this model.
        tags: a list of tags applied on this object
        infos: a dicitonnary of custom information

    ### Class variables

    `coll_name`
    :

    ### Static methods

    `fetchObject(pipeline)`
    :   Fetch one element from database and return the CommandGroup object 
        Args:
            pipeline: a Mongo search pipeline (dict)
        Returns:
            Returns the model object or None if nothing matches the pipeline.

    `fetchObjects(pipeline)`
    :   Fetch many commands from database and return a Cursor to iterate over model objects
        Args:
            pipeline: a Mongo search pipeline (dict)
        Returns:
            Returns a cursor to iterate on model objects

    ### Methods

    `addInDb(self)`
    :   To be overriden
        Add this model to pollenisator database.
        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise

    `addTag(self, newTag, overrideGroupe=True)`
    :   Add the given tag to this object.
        Args:
            newTag: a new tag as a string to be added to this model tags
            overrideGroupe: Default to True. If newTag is in a group with a tag already assigned to this object, it will replace this old tag.

    `delTag(self, tagToDelete)`
    :   Delete the given tag in this object.
        Args:
            tagToDelete: a tag as a string to be deleted from this model tags

    `delete(self)`
    :   To be overriden
        Delete the object represented by this model in database.

    `getDetailedString(self)`
    :   To be inherited and overriden
        Returns a detailed string describing this element. Calls __str__ of children by default.
        Returns:
            string

    `getId(self)`
    :   Returns the mongo id  of this element.
        Returns:
            bson.objectid.ObjectId

    `getParent(self)`
    :   Returns the mongo id  of this element parent.
        Returns:
            bson.objectid.ObjectId

    `getTags(self)`
    :   Returns the tag list assigned to this element.
        Returns:
            list of string

    `getTagsGroups(self)`
    :   Returns groups of tags that may not be applied at the same time
        Returns:
            List of list of strings

    `setTags(self, tags)`
    :   Change all tags for the given new ones  and update database
        Args:
            tags: a list of tag string

    `update(self)`
    :   To be overriden
        Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.

    `updateInfos(self, newInfos)`
    :   Change all infos stores in self.infos with the given new ones and update database.
        Args:
            newInfos: A new dictionnary of custom information