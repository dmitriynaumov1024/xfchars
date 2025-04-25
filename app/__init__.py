import sys
from .core import CharacterSearcher, CharacterSearchRequest
from .tui import TuiWorker

def main():
    return TuiWorker().main()
