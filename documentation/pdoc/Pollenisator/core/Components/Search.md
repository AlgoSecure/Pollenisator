Module Pollenisator.core.Components.Search
==========================================
DEPRECATED Hold functions to interact with the search bar. NOW LOCATED IN Filter.py

Classes
-------

`Operator(op, arg, exact_match=True)`
:   

    ### Methods

    `getMongo(self)`
    :

`ParseError(...)`
:   To raise parsing error

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`Search(query='', exactMatch=True)`
:   

    ### Class variables

    `classes`
    :

    `exact_match`
    :

    ### Static methods

    `getKeywordsSuggestion(coll, start, terms)`
    :

    `getSuggestions(searchValue, entry)`
    :

    `help()`
    :

    `parse(query, ignoreException=False)`
    :

    ### Methods

    `getIds(self)`
    :

    `getViews(self, appTw, viewFrame, mainApp)`
    :