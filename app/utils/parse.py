from typing import List

def parse_bool (s: str)-> bool:
    return s.strip().lower() == "true"

def parse_int (s: str)-> int:
    try:
        if s.startswith("0x"):
            return int(s, 16)
        else:
            return int(s)
    except:
        return 0

def parse_str (s: str)-> str:
    return s

def parse_list (s: str)-> List[str]:
    try:
        return list(map(str.strip, s.split(",")))
    except:
        return []


