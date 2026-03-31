#!/usr/bin/env python3
"""
Thin runner: forwards AppleScript to macOS `osascript`.
Prefer --file or stdin for multiline scripts; use -e only for short one-liners.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run AppleScript via osascript (stdin, file, or -e).",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-e",
        "--execute",
        metavar="LINE",
        help="Single-line AppleScript (multiline: use --file or stdin).",
    )
    group.add_argument(
        "-f",
        "--file",
        metavar="PATH",
        type=Path,
        help="Path to a .applescript / .scpt / plain text script file.",
    )
    parser.add_argument(
        "-a",
        "--args",
        nargs="*",
        metavar="ARG",
        help="Arguments to pass to the AppleScript.",
    )
    args = parser.parse_args()

    if args.execute is not None:
        cmd = ["osascript", "-e", args.execute]
        if args.args:
            cmd.extend(args.args)
        return subprocess.run(cmd, check=False).returncode

    if args.file is not None:
        path = args.file.expanduser().resolve()
        if not path.is_file():
            print(f"run_applescript: file not found: {path}", file=sys.stderr)
            return 2
        cmd = ["osascript", str(path)]
        if args.args:
            cmd.extend(args.args)
        return subprocess.run(cmd, check=False).returncode

    if sys.stdin.isatty():
        parser.print_help()
        print(
            "\nProvide a script via stdin (pipe/heredoc), or use -f / -e.",
            file=sys.stderr,
        )
        return 2

    script = sys.stdin.read()
    if not script.strip():
        print("run_applescript: empty stdin", file=sys.stderr)
        return 2

    proc = subprocess.run(
        ["osascript"],
        input=script.encode("utf-8"),
        check=False,
    )
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())