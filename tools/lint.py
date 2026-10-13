#!/usr/bin/env python3
"""Compatibility entry point; use kc.py check for new workflows."""
import sys
from kc import main

if __name__ == "__main__":
    # Preserve an optional global root argument before inserting the subcommand.
    args = sys.argv[1:]
    if "--root" in args:
        position = args.index("--root")
        root_args = args[position:position + 2]
        del args[position:position + 2]
    else:
        root_args = []
    sys.exit(main(root_args + ["check"] + args))
