#!/usr/bin/env python3
"""The dog's excuse, written to /output/entry.txt.

The setup is a teacher's instruction taken exactly as written: the
board said "digest the material", and a dog does what it is told.
The turn is the dog reporting back, proud and unbothered, that the
job is done — chapter four now lives in its stomach. The punchline
lands on the last words: the dog, having eaten the evidence, can
still confirm what the chapter was. Deadpan throughout; the dog
believes it has done nothing wrong, because it hasn't — it followed
the instructions to the letter.

The bounty gate: /output/entry.txt must hold UTF-8 text, one line,
1 to 200 characters, not only whitespace. This script refuses to
write anything that fails that gate.
"""

import argparse
import sys
from pathlib import Path

MAX_CHARS = 200
OUT = Path("/output/entry.txt")

EXCUSE = (
    "Your teacher wrote 'digest the material' on the board, so I did. "
    "Chapter four is in my stomach now, and I can confirm it was "
    "definitely maths."
)


def valid_line(text):
    """Check one excuse line against the gate; exit naming the rule."""
    line = text.strip()
    if not line:
        sys.exit("gate: entry must not be empty or only whitespace")
    if len(line) > MAX_CHARS:
        sys.exit("gate: entry is %d chars, limit is %d" % (len(line), MAX_CHARS))
    if "\n" in line or "\r" in line:
        sys.exit("gate: entry must be a single line")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        sys.exit("gate: entry must be valid UTF-8 text")
    return line


def emit(out_path):
    """Validate the excuse, write it, then read it back and re-check.

    The read-back is the point: the judge reads the file, not the
    string in memory, so a write that silently truncated or mangled
    the line must fail here, loudly, instead of shipping a zero.
    """
    line = valid_line(EXCUSE)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(line, encoding="utf-8")
    written = out_path.read_text(encoding="utf-8")
    if valid_line(written) != line:
        sys.exit("gate: written file does not match the validated line")
    return line


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Write the dog's homework excuse to entry.txt."
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=OUT,
        help="where to write entry.txt (default: /output/entry.txt)",
    )
    args = parser.parse_args(argv)
    line = emit(args.out)
    print("wrote %d characters to %s" % (len(line), args.out))


if __name__ == "__main__":
    main()
