import sys
from .core import CharacterSearcher, CharacterSearchRequest
from .tui import TuiWorker

def test_cli_1():
    request = CharacterSearchRequest().set_values(
        query = "Down Arrow",
        match_min = 2,
        char_limit = 0x10ffff,
        result_limit = 20
    )

    result = CharacterSearcher.search(request)

    print(f"looked for {result.request.query}")
    print(f"found {len(result.result)} items")
    for i in range(0, min(result.request.result_limit, len(result.result))):
        item = result.result[i]
        print(f"- {item.display} {item.name}")
        print(f"  unicode: {item.get_ucode()}, html: {item.get_htmlcode()}")
    return

def main():
    return TuiWorker().main()
