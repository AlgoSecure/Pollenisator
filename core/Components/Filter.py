"""Module using Lark parser to parse filter query and return according results"""
from lark import Lark, Transformer, exceptions
import re

class Term:
    """A search term, meaning "key.name" == (value) """
    def __init__(self, val):
        """Constructor"""
        self.val = val

class TreeToCondition(Transformer):
    """Inherits lark.Transformer
    A Lark Transformer to process the parse-tree returned by lark
    Attributes:
        null: value will be converted to python None
        true: value will be converted to python True
        false: value will be converted to python False
        eq: value will be converted to string "=="
        neq: value will be converted to string "!="
        gt: value will be converted to string ">"
        ge: value will be converted to string ">="
        le: value will be converted to string "<="
        lt: value will be converted to string "<"
        regex: value will be converted to string "||regex||"
        inside: value will be converted to string "in"
        notin: value will be converted to string "not in"
        andcond: value will be converted to string "and"
        orcond: value will be converted to string "or"
        notcond: value will be converted to string "not"
    """
    null = lambda self, _: None
    true = lambda self, _: True
    false = lambda self, _: False
    eq = lambda self, _: "=="
    neq = lambda self, _: "!="
    gt = lambda self, _: ">"
    ge = lambda self, _: ">="
    le = lambda self, _: "<="
    lt = lambda self, _: "<"
    regex = lambda self, _: "||regex||"
    inside = lambda self, _: "in"
    notin = lambda self, _: "not in"
    andcond = lambda self, _: "and"
    orcond = lambda self, _: "or"
    notcond = lambda self, _: "not"

    def term(self, items):
        """Applied on parse-tree terms objects.
        Args:
            items: the parse-tree term object
        Returns:
            the given item as a list
        """
        return list(items)

    def var(self, s):
        """Applied on parse-tree var objects.
        Args:
            s: the parse-tree var object
        Returns:
            the given item as a Term
        """
        (s,) = s
        return Term(s)

    def string(self, s):
        """Applied on parse-tree string objects.
        Args:
            s: the parse-tree string object
        Returns:
            the given item as a str
        """
        (s,) = s
        return str(s)
    def number(self, n):
        """Applied on parse-tree number objects.
        Args:
            s: the parse-tree number object
        Returns:
            the given item as a str with double quotes around them
        """
        (n,) = n
        return "\""+str(n)+"\""



class ParseError(Exception):
    """Inherits Exception
    Class to raise parsing error"""

class Filter:
    """
    Class to perform Lark parsing and filter database search.
    Attributes:
        exact_match: (DEPRECATED use in, or regex to perform partial match) default to True, can be changed in constructor
        condition_parser: The parsing syntax of Lark is used to search
                        * term: is a (var == value)   
                        * uniopcond: is unary operation (not)
                        * opcond: logical operator on temrs ("and" and "or")       
                        * opregex: the regex operator
                        * STRING: an alphanumeric string with extras characs '.', '[' and ']'
    """
    exact_match = True
    condition_parser = Lark(r"""
    ?term: "("fixedvalue op fixedvalue")"
                | fixedvalue op fixedvalue
                | STRING opregex ESCAPED_STRING
                | uniopcond term
                | "("uniopcond term")"
                | term opcond term
                | "("term opcond term")"
    uniopcond: "not" -> notcond
    opcond: "and" -> andcond | "or" -> orcond
    op: "==" -> eq | "!=" -> neq | ">" -> gt | "<" -> lt 
        | "<=" -> le | ">=" -> ge | "in" -> inside | "not in" -> notin 
    opregex: "regex" -> regex
    STRING: /[A-Za-z0-9\.\[\]]+/
    fixedvalue: SIGNED_NUMBER -> number
         | "true" -> true
         | "false" -> false
         | "null" -> null
         | ESCAPED_STRING -> string
         | STRING -> var

    %import common.ESCAPED_STRING
    %import common.SIGNED_NUMBER
    %import common.WS
    %ignore WS
    """, start='term', parser="lalr", transformer=TreeToCondition())

    @classmethod
    def help(cls):
        """Return a string to help typing request by providing examples
        Returns:
            A string of examples
        """
        # pylint: disable=anomalous-backslash-in-string
        return """
Search examples in match (python condition):
type == "port"
type == "port" and port == 443
type == "port" and port regex "443$"
type == "port" and (port == 80 or port == 443)
type == "port" and port != 443
type == "port" and port != 443 and port != 80
type == "defect"
type == "defect" and "Foo" in title
type == "ip" and ip regex "[A-Za-z]"
type == "ip" and ip regex "^1\.2"
type == "tool" and "done" in status
type == "tool" and "done" not in status
type == "tool" and "ready" in status
type == "ip" and infos.key == "ABC"
"""
    def __init__(self, query="", exactMatch=True):
        """Constructor
        Args:
            query: the query to parse
            exactMatch: not used
        Raises:
            ParseError if Lark raises an UnexpectedToken or an UnexptectedCharacters exception.
        """
        Filter.exact_match = exactMatch
        try:
            self.parsed = Filter.condition_parser.parse(query)
        except exceptions.UnexpectedToken as e:
            raise ParseError(e)
        except exceptions.UnexpectedCharacters as e:
            raise ParseError(e)

    def evaluate(self, parsedcopy, data):
        """Replace parsed items with corresponding formated data and eval the condition using python eval()
        Args:
            parsedcopy: parsed items generated by Lark
            data: data of any object as dictionnary.
        Returns:
            returns result of final eval function
        """
        phrase = ""
        if "||regex||" in parsedcopy:
            val = data.get(parsedcopy[0], None)
            if val is None:
                return False
            return re.search(str(parsedcopy[2])[1:-1], str(val)) is not None
        for children in parsedcopy:
            if isinstance(children, Term):
                if children.val in data.keys():
                    val = data[children.val]
                    if isinstance(val, str):
                        val = "\"\"\""+val.lower()+"\"\"\""
                    else:
                        val = str(val).lower().replace("\"","\\\"")
                    phrase += val+" "
                else:
                    return False
            elif isinstance(children, list):
                res = self.evaluate(children, data)
                phrase += str(res).lower()+" "
            else:
                phrase += children.lower()+" "
        phrase = phrase.replace("false","False")
        phrase = phrase.replace("true","True")
        return eval(phrase)

    def getIds(self, appTw):
        """Return Ids of the models in a PollenisatorTreeview matching the filter
        Args:
            appTw: a PollenisatorTreeview
        Raises:
            ParseError if Lark raises an UnexpectedToken or an UnexptectedCharacters exception.
        Returns:
            A list of Mongo iid which data matched the filter
        """
        found_res = []
        views = appTw.views
        for dbId in views:
            view_object = views[dbId]["view"]
            data = view_object.controller.getData()
            if data is None:
                continue
            keys = list(data.keys())
            it_key = 0
            len_keys = len(keys)
            while it_key < len_keys :
                key = keys[it_key]
                val = data[key]
                if isinstance(val, dict):
                    for subkey, subval in val.items():
                        data[key+"."+str(subkey)] = subval
                        keys.append(key+"."+str(subkey))
                elif isinstance(val, list):
                    for i,subval in enumerate(val):
                        data[key+"["+str(i)+"]"] = subval
                it_key += 1
                len_keys = len(keys)
            dtype = view_object.controller.getType()
            data["type"] = dtype
            result = self.evaluate(self.parsed, data)
            if result:
                found_res.append(dbId)
        return found_res
