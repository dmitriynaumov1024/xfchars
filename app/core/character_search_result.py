from typing import List
from datetime import datetime, UTC
from .character_info import CharacterInfo
from .character_search_request import CharacterSearchRequest

class CharacterSearchResult:
    """
    Character search result
    """
    created_at: datetime
    request: CharacterSearchRequest
    result: List[CharacterInfo]
    
    def set_values (self, *, 
                    created_at: datetime = None, 
                    request: CharacterSearchRequest = None, 
                    result: List[CharacterInfo] = None):
        if created_at is not None:
            self.created_at = created_at
        if request is not None:
            self.request = request
        if result is not None:
            self.result = result
        return self

    def from_dict (self, kw: dict):
        if "created_at" in kw:
            kw["created_at"] = datetime.fromtimestamp(kw["created_at"])
        if "request" in kw:
            kw["request"] = CharacterSearchRequest().from_dict(kw["request"])
        if "result" in kw:
            kw["result"] = [CharacterInfo().from_dict(item) for item in kw["result"]]
        return self.set_values(**kw)
