"""Check GSD phase progress and optionally launch a command in the project."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

PHASE = r"[0-9]+(?:\.[0-9]+)*"


def phase_id(value):
    if not isinstance(value, str) or not re.fullmatch(PHASE, value):
        raise ValueError("invalid phase identity")
    return ".".join(str(int(part)) for part in value.split("."))


def check(root):
    planning = root / ".planning"
    state = (planning / "STATE.md").read_text(encoding="utf-8-sig")
    roadmap = (planning / "ROADMAP.md").read_text(encoding="utf-8-sig")
    progress = re.findall(r"^Progress:[ \t]*([0-9]+)/([0-9]+)(?=\s|$)", state, re.M)
    rows = re.findall(rf"^[ \t]*- \[([ xX])\][ \t]+\*\*Phase[ \t]+({PHASE}):",
                      roadmap, re.M)
    phases = {phase_id(value): mark.lower() == "x" for mark, value in rows}
    if len(progress) != 1 or not rows or len(rows) != len(phases):
        raise ValueError("unsupported progress format or duplicate roadmap phase")
    completed = {value for value, done in phases.items() if done}
    reported = tuple(map(int, progress[0]))
    actual = (len(completed), len(phases))
    if reported != actual:
        return 2, f"CONFLICT: STATE.md {reported} != ROADMAP.md {actual}"

    ledger = planning / "p2-completed.json"
    if completed or ledger.exists():
        values = json.loads(ledger.read_text(encoding="utf-8-sig"))
        if not isinstance(values, list):
            raise ValueError("completed phase ledger must be a JSON list")
        identities = {phase_id(value) for value in values}
        if len(identities) != len(values):
            raise ValueError("duplicate completed phase identity")
        if identities != completed:
            return 2, f"CONFLICT: recorded {sorted(identities)} != roadmap {sorted(completed)}"

    return 0, f"CONSISTENT: {actual[0]}/{actual[1]}"


def main(argv):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    separator = argv.index("--") if "--" in argv else len(argv)
    args = parser.parse_args(argv[:separator])
    command = argv[separator + 1:]
    if separator < len(argv) and not command:
        parser.error("expected a command after --")
    root = args.project.resolve()
    try:
        status, message = check(root)
    except (OSError, ValueError) as error:
        status, message = 3, f"UNKNOWN: {error}"
    print(message, file=sys.stderr if status else sys.stdout, flush=True)
    if status or not command:
        return status
    try:
        return subprocess.run(command, cwd=root).returncode
    except OSError as error:
        print(f"LAUNCH FAILED: {error}", file=sys.stderr)
        return 4


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
