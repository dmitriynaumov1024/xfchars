APP_NAME = "xfchars"
APP_VERSION = "1.0"
APP_REVISION = "3"

APP_HELP = """
'xfchars' lets you find unicode characters by name.

usage: xfchars [OPTION] [FIND OPTIONS...]

 --help                 print help to stdout
 --version              print version info to stdout
 --gui                  start gui application
 --find QUERY [...]     find characters by query and print result to stdout

xfchars find options:

 --match-min N, --match-at-least N
    match at least N words from query
    if N is more than there are words in query, it is ignored.

 --char-limit N
    where N is integer (decimal or hex)
    stops bruteforcing at code point N 

 --include KEYWORDS
    where KEYWORDS is comma-separated list of strings
    keywords to be included
    the last one of --include / --exclude options has higher priority

 --exclude KEYWORDS
    where KEYWORDS is comma-separated list of strings
    keywords to be excluded
    the last one of --include / --exclude options has higher priority

 --result-limit N
    where N is integer (decimal)

default excluded keywords:
 
 "ARABIC", "TIBETAN", "MODIFIER", "COMBINING"
"""

APP_SHORT_HELP = """
run me with --help option to get detailed help.
"""
