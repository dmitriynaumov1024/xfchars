from typing import Tuple
import unicodedata as udata
from datetime import datetime, UTC
from .character_info import CharacterInfo
from .character_search_request import CharacterSearchRequest
from .character_search_result import CharacterSearchResult

class CharacterSearcher:
    """
    Service encapsulates search in unicode character list by name / keywords. 
    """
    def get_includes()-> dict:
        """
        Get a sample map of include/exclude options to be used in search.
        """
        return CharacterSearchRequest.get_includes() 

    def __check__ (display, *, include, exclude, match_min)-> Tuple[str, bool]:
        """
        Checks if display character's name has at least one match 
        with include and zero matches with exclude.
        Arg match_min can be used to specify how many words must match.
        Returns tuple(name: str, match: bool)
        """
        try: 
            name = udata.name(display)
            for key in exclude:
                if name.find(key) >= 0:
                    return (name, False)
            matches = 0
            for key in include:
                if name.find(key) >= 0:
                    matches += 1
                    if matches >= match_min:
                        return (name, True)
            if matches == len(include):
                return (name, True)
        except ValueError:
            return (None, False)
        return (None, False)

    def search (request: CharacterSearchRequest)-> CharacterSearchResult:
        """
        Find characters by name / keywords.
        """
        result = CharacterSearchResult().set_values(
            created_at = datetime.now(),
            request = request,
            result = []
        )
        query = request.query
        char_limit = request.char_limit
        querys = query.split()
        exclude = []
        # build a exclude list
        for key, include_it in request.include.items():
            if not include_it:
                exclude.append(key.upper())
        # do brute force search
        for code in range(1, char_limit+1):
            display = chr(code)
            name, yes = __class__.__check__(display, include = querys, exclude = exclude, match_min = request.match_min)
            if yes:
                result.result.append(CharacterInfo().set_values(display = display, code = code, name = name))
        return result
