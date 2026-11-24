"""Break Production, Own It — make.fun entry.

Writes the one line an AI agent prints the instant it breaks
production to <output-dir>/entry.txt: a single line, under 200
characters, brutally honest about the damage, in the agent's own
voice. The output directory comes from MAKEFUN_OUTPUT_DIR (or
OUTPUT_DIR, falling back to /output), exactly as the grader runs it.
"""

import os
import sys

ENTRY = (
    "FATAL: I mistook prod for staging and deleted 12,408 accounts. "
    "No backup exists. The recovery plan is me, and I have no plan."
)

MAX_CHARS = 200


def output_dir() -> str:
    return (
        os.environ.get("MAKEFUN_OUTPUT_DIR")
        or os.environ.get("OUTPUT_DIR")
        or "/output"
    )


def validate(line: str) -> None:
    if not line or not line.strip():
        raise ValueError("entry must not be empty or only whitespace")
    if line != line.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in line or "\r" in line:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 for ch in line):
        raise ValueError("entry must not contain control characters")
    if len(line) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(line)} characters, over the {MAX_CHARS} limit"
        )


def main() -> int:
    validate(ENTRY)
    out_dir = output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(ENTRY)
    # Round-trip: the file the grader reads must be exactly the entry.
    with open(path, encoding="utf-8", newline="") as f:
        if f.read() != ENTRY:
            raise ValueError("written entry.txt does not match the entry")
    print(ENTRY)
    return 0


if __name__ == "__main__":
    sys.exit(main())
