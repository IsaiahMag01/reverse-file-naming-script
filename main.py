#!/usr/bin/env python3
"""
Reverse the numeric prefixes of files in a folder.

Example: with 50 files, "1. Title.mp4" becomes "50. Title.mp4",
"50. Other.mp4" becomes "1. Other.mp4", and so on.

Usage:
    python reverse_numbering.py "C:\\path\\to\\folder"            # dry run (preview only)
    python reverse_numbering.py "C:\\path\\to\\folder" --apply    # actually rename
"""
import re
import sys
import uuid
from pathlib import Path

PATTERN = re.compile(r"^(\d+)\.\s*(.*)$", re.DOTALL)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    folder = Path(sys.argv[1])
    apply = "--apply" in sys.argv

    items = []  # (path, number, rest_of_name, width)
    for p in folder.iterdir():
        if not p.is_file():
            continue
        m = PATTERN.match(p.name)
        if m:
            items.append((p, int(m.group(1)), m.group(2), len(m.group(1))))

    if not items:
        print("No files with a leading 'N. ' number found.")
        return

    lo = min(i[1] for i in items)
    hi = max(i[1] for i in items)
    print(f"Found {len(items)} numbered files (range {lo}-{hi}).\n")

    plan = []
    for p, n, rest, width in sorted(items, key=lambda i: i[1]):
        new_n = hi + lo - n
        # keep zero-padding if the originals used it (e.g. 01, 02)
        num = str(new_n).zfill(width) if width > 1 and p.name[0] == "0" else str(new_n)
        new_name = f"{num}. {rest}"
        plan.append((p, p.with_name(new_name)))
        print(f"{p.name}\n   -> {new_name}")

    if not apply:
        print("\nDry run only. Re-run with --apply to rename.")
        return

    # Two-phase rename so no file ever overwrites another mid-process
    temps = []
    for src, dst in plan:
        tmp = src.with_name(f"__tmp_{uuid.uuid4().hex}{src.suffix}")
        src.rename(tmp)
        temps.append((tmp, dst))
    for tmp, dst in temps:
        tmp.rename(dst)

    print(f"\nDone. Renamed {len(plan)} files.")


if __name__ == "__main__":
    main()