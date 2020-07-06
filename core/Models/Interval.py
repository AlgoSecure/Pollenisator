"""Interval Model. Useful to limit in a time frame some tools"""

from core.Models.Element import Element
from core.Models.Tool import Tool
from core.Components.mongo import MongoCalendar
import core.Components.Utils as Utils
from bson.objectid import ObjectId
from datetime import datetime


class Interval(Element):
    """
    Represents an interval object that defines an time interval where a wave can be executed.

    Attributes:
        coll_name: collection name in pollenisator database
    """
    coll_name = "intervals"

    def __init__(self, valuesFromDb=None):
        """Constructor
        Args:
            valueFromDb: a dict holding values to load into the object. A mongo fetched interval is optimal.
                        possible keys with default values are : _id (None), parent (None), tags([]), infos({}),
                        wave(""), dated("None"), datef("None")
        """
        if valuesFromDb is None:
            valuesFromDb = {}
        super().__init__(valuesFromDb.get("_id", None), valuesFromDb.get("parent", None),  valuesFromDb.get(
            "tags", []), valuesFromDb.get("infos", {}))
        self.initialize(valuesFromDb.get("wave", ""), valuesFromDb.get("dated", "None"),
                        valuesFromDb.get("datef", "None"), valuesFromDb.get("infos", {}))

    def initialize(self, wave, dated="None", datef="None", infos=None):
        """Set values of interval
        Args:
            wave: the parent wave name
            dated: a starting date and tiem for this interval in format : '%d/%m/%Y %H:%M:%S'. or the string "None"
            datef: an ending date and tiem for this interval in format : '%d/%m/%Y %H:%M:%S'. or the string "None"
            infos: a dictionnary with key values as additional information. Default to None
        Returns:
            this object
        """
        self.wave = wave
        self.dated = dated
        self.datef = datef
        self.infos = infos if infos is not None else {}
        return self

    def delete(self):
        """
        Delete the Interval represented by this model in database.
        """
        mongoInstance = MongoCalendar.getInstance()
        mongoInstance.delete(
            "intervals", {"_id": self._id})
        parent_wave = mongoInstance.find("waves", {"wave": self.wave}, False)
        self._id = None
        if parent_wave is None:
            return
        mongoInstance.notify(mongoInstance.calendarName,
                             "waves", parent_wave["_id"], "update", "")
        other_intervals = Interval.fetchObjects({"wave": self.wave})
        no_interval_in_time = True
        for other_interval in other_intervals:
            if Utils.fitNowTime(other_interval.dated, other_interval.datef):
                no_interval_in_time = False
                break
        if no_interval_in_time:
            tools = Tool.fetchObjects({"wave": self.wave})
            for tool in tools:
                tool.setOutOfTime()

    def setToolsInTime(self):
        """Get all OOT (Out of Time) tools in this wave and checks if this Interval makes them in time. 
        If it is the case, set them in time.
        """
        if Utils.fitNowTime(self.dated, self.datef):
            tools = Tool.fetchObjects({"wave": self.wave, "status": "OOT"})
            for tool in tools:
                tool.setInTime()

    def addInDb(self):
        """
        Add this interval in database.

        Returns: a tuple with :
                * bool for success
                * mongo ObjectId : already existing object if duplicate, create object id otherwise 
        """
        base = {"wave": self.wave, "dated": self.dated, "datef": self.datef}
        parent = self.getParent()
        mongoInstance = MongoCalendar.getInstance()
        res = mongoInstance.insert(
            "intervals", base, parent)
        self.setToolsInTime()
        self._id = res.inserted_id
        return True, res.inserted_id

    def update(self, pipeline_set=None):
        """Update this object in database.
        Args:
            pipeline_set: (Opt.) A dictionnary with custom values. If None (default) use model attributes.
        """
        self.setToolsInTime()
        mongoInstance = MongoCalendar.getInstance()
        if pipeline_set is None:
            mongoInstance.update("intervals", {"_id": ObjectId(self._id)}, {
                "$set": {"dated": self.dated, "datef": self.datef}})
        else:
            mongoInstance.update("intervals", {"_id": ObjectId(self._id)}, {
                "$set": pipeline_set})

    def _getParent(self):
        """
        Return the mongo ObjectId _id of the first parent of this object. For an interval it is the wave.

        Returns:
            Returns the parent wave's ObjectId _id".
        """
        mongoInstance = MongoCalendar.getInstance()
        return mongoInstance.find("waves", {"wave": self.wave}, False)["_id"]

    def __str__(self):
        """
        Get a string representation of a command group.

        Returns:
            Returns the string "Interval".
        """
        return "Interval"

    @classmethod
    def _translateDateString(cls, datestring):
        """Returns the datetime object when given a str wih format '%d/%m/%Y %H:%M:%S'
        Args:
            a string formated as datetime format : '%d/%m/%Y %H:%M:%S'
        """
        ret = None
        if(type(datestring) == str or type(datestring) == str):
            if datestring != "None":
                ret = datetime.strptime(
                    datestring, '%d/%m/%Y %H:%M:%S')
        return ret

    def getEndingDate(self):
        """Returns the ending date and time of this interval
        Returns:
            a datetime object.
        """
        return Interval._translateDateString(self.datef)

    def getDbKey(self):
        """Return a dict from model to use as unique composed key.
        Returns:
            A dict (1 key :"wave")
        """
        return {"wave": self.wave}
