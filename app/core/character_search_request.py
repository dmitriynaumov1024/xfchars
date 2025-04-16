class CharacterSearchRequest:
    """
    Character search request
    """
    query: str
    match_min: int
    char_limit: int
    result_limit: int
    include: dict

    __includes_sample__ = ({
        "ARABIC": False,
        "TIBETAN": False,
        "MODIFIER": False,
        "COMBINING": False
    })

    __char_limits__ = ([
        0xff,
        0xffff,
        0x1fffff
    ])

    def get_includes ()-> dict:
        """
        Get a sample map of include/exclude options to be used in search.
        """
        return dict(__class__.__includes_sample__)

    def get_char_limits ()-> list:
        """
        Get list of char limit options
        """
        return __class__.__char_limits__

    def __init__ (self):
        self.query = ""
        self.match_min = 1
        self.char_limit = 0xffff
        self.result_limit = 10
        self.include = self.__class__.get_includes()

    def set_values (self, *, 
                    query: str = None, 
                    match_min: int = None, 
                    match_at_least: int = None,
                    char_limit: int = None, 
                    result_limit: int = None, 
                    include: dict|list = None,
                    exclude: dict|list = None):
        char_limits = self.__class__.__char_limits__
        if query is not None:
            self.query = query.upper().strip()
        if match_min is not None:
            self.match_min = max(1, match_min)
        if match_at_least is not None:
            self.match_min = max(1, match_at_least)
        if char_limit is not None:
            self.char_limit = max(char_limits[0], min(char_limits[-1], char_limit))
        if result_limit is not None:
            self.result_limit = max(1, result_limit)
        if type(include) is dict:
            for key, val in include.items():
                self.include[key] = val
        if type(include) is list:
            for key in include:
                self.include[key] = True
        if type(exclude) is dict:
            for key, val in exclude.items():
                self.include[key] = not val
        if type(exclude) is list:
            for key in exclude:
                self.include[key] = False
        return self

    def from_dict (self, kw: dict):
        return self.set_values(**kw)
