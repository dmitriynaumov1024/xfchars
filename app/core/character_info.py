class CharacterInfo:
    """
    Character info
    """
    code: int
    display: str
    name: str

    def get_hex (self)-> str:
        """
        Get plain hex representation like 00FF
        """
        if self.code <= 0xffff:
            return f"{self.code:04x}"
        elif self.code <= 0xffffff:
            return f"{self.code:06x}"
        else:
            return f"{self.code:08x}"

    def get_ucode (self)-> str:
        """
        Get unicode code like '\\u00FF'
        """
        return f"\\u{self.get_hex()}"

    def get_htmlcode (self)-> str:
        """
        Get html code like '&#12345;'
        """
        return f"&#{self.code};"

    def set_values (self, *, code: int = None, display: str = None, name: str = None):
        self.code = code
        self.display = display
        self.name = name
        return self

    def from_dict(self, kw: dict):
        return self.set_values(**kw)
