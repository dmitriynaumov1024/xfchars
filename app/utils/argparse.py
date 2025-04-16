from typing import List
from .parse import parse_bool 

def itemparse (name, item, hints):
    if name in hints:
        return hints[name](item)
    else:
        return item

def nameparse (word):
    name = word[2:].replace("-", "_").lower()
    return name

def argparse (args: List[str], **hints)-> dict:
    result = dict()
    name = None
    for word in args:
        # if current word starts with "--", it is arg name.
        if word.startswith("--"):
            # if already has name, expect previous was bool
            if name and name in hints and hints[name] == parse_bool:
                result[name] = True
                name = None
            name = nameparse(word)
        # else if we already have arg name, then set value
        elif name:
            result[name] = itemparse(name, word, hints)
            name = None
    # if name was not unset, expect it to be bool
    if name and name in hints and hints[name] == parse_bool:
        result[name] = True
    return result
