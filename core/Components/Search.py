"""DEPRECATED Hold functions to interact with the search bar. NOW LOCATED IN Filter.py"""

from core.Components.mongo import MongoCalendar
from core.Models.Ip import Ip
from core.Models.Port import Port
from core.Models.Scope import Scope
from core.Models.Tool import Tool
from core.Models.Defect import Defect
from core.Views.IpView import IpView
from core.Views.PortView import PortView
from core.Views.ScopeView import ScopeView
from core.Views.ToolView import ToolView
from core.Views.DefectView import DefectView
import re


class Operator:
    def __init__(self, op, arg, exact_match=True):
        self.op = op
        self.arg = arg
        try:
            regex = '^'+self.arg+'$' if exact_match else self.arg
            self.reg = re.compile(regex, re.IGNORECASE | re.MULTILINE)
        except re.error as e:
            raise e

    def getMongo(self):
        key = self.op
        val = {}
        val["$regex"] = self.reg
        return key, val


class ParseError(Exception):
    """To raise parsing error"""


class Search:
    exact_match = True
    classes = {
        "port": {"collection": "ports", "view": PortView, "model": Port, "keywords": ["port", "proto", "service", "product", "ip", "scope", "notes", "tags", "infos."]},
        "ip": {"collection": "ips", "view": IpView, "model": Ip, "keywords": ["ip", "scope", "notes", "tags", "infos."]},
        "scope": {"collection": "scopes", "view": ScopeView, "model": Scope, "keywords": ["wave", "scope", "notes", "tags"]},
        "tool": {"collection": "tools", "view": ToolView, "model": Tool, "keywords": ["name", "dated", "datef", "lvl", "port", "proto", "ip", "scope", "notes", "tags"]},
        "defect": {"collection": "defects", "view": DefectView, "model": Defect, "keywords": ["title", "ease", "impact", "risk", "port", "proto", "ip", "scope", "notes", "tags"]},
    }

    @classmethod
    def help(cls):
        # pylint: disable=anomalous-backslash-in-string
        return """Search examples in match: (python regex)
every ports                       || class:port
every 443 ports                || class:port port:^443$
ports ending with 443      || class:port port:443$
all 80 or 443 ports            || class:port port:^80$|^443$
every port excepted 443  || port:(?!^443$) class:port
ports excepted 80|443     || port:(?!^443$|^80$) class:port
all defects                        || class:defect
every defect with Foo      || class:defect title:foo
all domains                      || class:ip ip:[A-Za-z]
every ip starting as 1.2    || ip:^1\.2 class:ip
every finished tool         || class:tool datef:^(?!None).+
every tool not done         || class:tool datef:None
search an ip infos for ABC info value || class:ip ip.infos.ABC:value
----------------------------------------------------
Search examples in exact match: (python regex)
every ports                       || class:port
every 443 ports                || class:port port:443
ports ending with 443      || class:port port:.*443
all 80 or 443 ports            || class:port port|80|443
every port excepted 443  || port:(?!443).* class:port
ports excepted 80|443     || port:(?!443|80).* class:port
all defects                        || class:defect
every defect with Foo      || class:defect title:.*foo.*
all domains                      || class:ip ip:.*[A-Za-z].*
every ip starting as 1.2    || ip:1\.2\..* class:ip"""
    @classmethod
    def getKeywordsSuggestion(cls, coll, start, terms):
        liste = [keyword for keyword in cls.classes[coll]["keywords"]
                 if keyword.startswith(start) and keyword not in terms]
        if coll in ["ip", "port"] and start.startswith("infos."):
            mongoInstance = MongoCalendar.getInstance()
            infosInDb = mongoInstance.find(
                Search.classes[coll]["collection"], {"infos": {"$ne": {}}})
            keys = set()
            for infoInDb in infosInDb:
                for k in infoInDb["infos"].keys():
                    keys.add("infos."+k)
            liste = list(keys)
            liste.sort()

        return liste

    @classmethod
    def getSuggestions(cls, searchValue, entry):
        initialValue = str(searchValue.get())
        pos = entry.index('insert')
        wordPos = initialValue.find(" ", pos)
        wordBeforePos = initialValue.find(" ", 0, pos)
        nextValuePos = initialValue.find(":", pos)
        editingTheKw = wordPos <= nextValuePos
        toComplete = initialValue[:wordPos] if wordPos != -1 else initialValue
        words = toComplete.split()
        # EMPTY SEARCH BAR, return class choice
        if len(words) == 0:
            ret = list(map(lambda x: "class:"+x, cls.classes.keys()))
            return ret
        ret = []
        # get word to complete, if a space just has been placed, we have a new word
        if toComplete[wordPos] == " ":
            word = ""
        else:
            word = words[-1].strip()
        posValue = word.find(':')  # Search a key:value delimiter
        try:
            # Check if a class has been found
            coll, terms = cls.parse(toComplete, True)
        except ParseError:
            return ret
        # No class found, suggests class
        if coll == "":
            try:
                value = word[posValue+1:]
                if value != "".strip() and not editingTheKw and posValue != -1:
                    classes = [classe for classe in cls.classes.keys()
                               if classe.startswith(value)]
                else:
                    classes = cls.classes.keys()
            except IndexError:
                classes = cls.classes.keys()
            ret = list(map(lambda x: "class:"+x, classes))
            return ret
        # No : found, suggests keyword
        if posValue == -1:
            ret = list(map(lambda x: initialValue[:wordBeforePos]+" "+x, cls.getKeywordsSuggestion(
                coll, word, list(map(lambda x: x.op, terms)))))
        return ret

    def __init__(self, query="", exactMatch=True):
        try:
            self.query = query
            self.coll = ""
            Search.exact_match = exactMatch
            self.terms = []
            if self.query != "":
                self.coll, self.terms = Search.parse(query)
        except ParseError as e:
            raise e

    def getViews(self, appTw, viewFrame, mainApp):
        mongoLine = {}
        mongoInstance = MongoCalendar.getInstance()
        for term in self.terms:
            key, val = term.getMongo()
            mongoLine[key] = val
        found_res = mongoInstance.find(
            Search.classes[self.coll]["collection"], mongoLine)
        print("Searchinging in "+str(self.coll)+" mogoline:"+str(mongoLine))
        ret = []
        for found in found_res:
            view_cls = Search.classes[self.coll]["view"]
            model_cls = Search.classes[self.coll]["model"]
            ret.append(view_cls(appTw, viewFrame, mainApp, model_cls(found)))
        return ret

    def getIds(self):
        ret = []
        mongoInstance = MongoCalendar.getInstance()
        if self.coll == '':
            return ret
        mongoLine = {}
        for term in self.terms:
            key, val = term.getMongo()
            mongoLine[key] = val
        found_res = mongoInstance.find(
            Search.classes[self.coll]["collection"], mongoLine)
        for found in found_res:
            ret.append(str(found["_id"]))
        return ret

    @classmethod
    def parse(cls, query, ignoreException=False):
        ret = []
        vals = query.split(" ")
        coll = ""
        for val in vals:
            kv = val.split(":")
            if len(kv) != 2 and not ignoreException:
                raise ParseError("Incorrect search term: '" +
                                 str(val)+"'. Parameter name or value missing.")
            operator = kv[0].strip()
            if len(kv) == 2:
                args = kv[1].strip()
            else:
                args = ""
            if operator == "class":
                if args in Search.classes.keys():
                    coll = args
                elif not ignoreException:
                    raise ParseError(
                        "invalid class. Valid classes are "+(', '.join(Search.classes.keys())))
            else:
                try:
                    op = Operator(operator, args, Search.exact_match)
                except:
                    raise ParseError(
                        "Argument "+str(operator)+":"+str(args) + " is not a valid python regex.")
                ret.append(op)
        if coll == "" and not ignoreException:
            raise ParseError("Term class required class:<value>")
        return coll, ret
