#!/usr/bin/env python3
"""Security controls for the free MAID OpenCode GitHub Actions pilot."""
import argparse
import json
import pathlib
import subprocess
import sys

OWNER = "karanzing1992"
ISSUE_NUMBER = 16
COMMAND = "/maid-oss"
ALLOWED_FILE = "docs/maid/AUTOPILOT_PILOT_RESULT.md"


def owner_authorized(event):
    issue = event.get("issue") or {}
    comment = event.get("comment") or {}
    return (
        event.get("action") == "created"
        and (event.get("sender") or {}).get("login") == OWNER
        and (comment.get("user") or {}).get("login") == OWNER
        and comment.get("body", "").strip() == COMMAND
        and issue.get("number") == ISSUE_NUMBER
        and not issue.get("pull_request")
    )


def validate_changes(repo="."):
    root = pathlib.Path(repo).resolve()
    allowed = root / ALLOWED_FILE
    if not allowed.is_file() or not allowed.read_text(encoding="utf-8").strip():
        raise ValueError("MAID pilot file was not created or is empty")
    result = subprocess.run(
        ["git", "status", "--porcelain", "-uall"],
        cwd=root, check=True, capture_output=True, text=True,
    )
    changed = [line[3:] for line in result.stdout.splitlines() if line.strip()]
    if changed != [ALLOWED_FILE]:
        raise ValueError("Disallowed changes; expected only %r, got %r" % (ALLOWED_FILE, changed))
    if allowed.stat().st_size > 16384:
        raise ValueError("Pilot file unexpectedly large")
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--event", type=pathlib.Path)
    parser.add_argument("--validate-diff", action="store_true")
    args = parser.parse_args()
    if args.event:
        data = json.loads(args.event.read_text(encoding="utf-8"))
        if not owner_authorized(data):
            raise SystemExit("DENIED: unauthorized or malformed MAID pilot event")
        print("AUTHORIZED_OWNER_PILOT: issue 16, exact command")
    if args.validate_diff:
        print("ALLOWED_DIFF:", validate_changes())


if __name__ == "__main__":
    main()
