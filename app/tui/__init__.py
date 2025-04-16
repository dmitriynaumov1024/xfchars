import sys
import os
from ..core import *
from ..utils import *
from .info import *

class TuiWorker:
    def print_result (self, result: CharacterSearchResult):
        request = result.request
        result_limit = min(request.result_limit, len(result.result))
        print(f"looked for {request.query}")
        print(f"match at least {request.match_min}")
        print(f"found {len(result.result)} items, showing {result_limit}")
        for i in range(0, result_limit):
            item = result.result[i]
            print(f"  {item.display} {item.name}")
            print(f"  unicode: {item.get_ucode()}, html: {item.get_htmlcode()}")
        print()
        return 0

    def command_short_help (self):
        print(APP_SHORT_HELP)
        return 2

    def command_help (self):
        print(APP_HELP)
        return 0

    def command_version (self):
        print(f"{APP_NAME} {APP_VERSION}")
        return 0

    def command_find (self, args):
        if len(args) < 1:
            return self.command_short_help()
        kwargs = argparse(
            ["--query", *args],
            query = parse_str,
            match_min = parse_int,
            match_at_least = parse_int,
            char_limit = parse_int,
            include = parse_list,
            exclude = parse_list,
            result_limit = parse_int
        )
        request = CharacterSearchRequest().set_values(**kwargs)
        result = CharacterSearcher.search(request)
        self.print_result(result)
        return 0

    def command_gui (self, args):
        # to do implement gui worker
        return 0

    def command (self, command, args_list):
        command = command.lower().strip()
        if command.startswith("--"):
            command = command[2:]
        if command == "find":
            return self.command_find(args_list)
        elif command == "gui":
            return self.command_gui(args_list)
        elif command == "version":
            return self.command_version()
        elif command == "help":
            return self.command_help()
        else:
            return self.command_short_help()

    def main (self):
        if len(sys.argv) < 2:
            return self.command_short_help()
        return self.command(sys.argv[1], sys.argv[2:])
