#!/usr/bin/env python3
"""MAID bounded autonomous coding queue. Does not execute issue-authored code."""
import base64
import fnmatch
import json
import os
import pathlib
import re
import subprocess
import sys

OWNER = "karanzing1992"
REPO = "karanzing1992/airo"
TRIGGER = "/maid-autonomous-run"
POLICY = "docs/maid/AUTONOMOUS_ISSUE_POLICY.json"

def command(*args):
    p = subprocess.run(args, text=True, capture_output=True, check=True, timeout=30)
    return p.stdout.strip()

def authorize(event, kind, actor):
    if kind == "schedule":
        return True
    if kind == "workflow_dispatch":
        return actor == OWNER
    if kind != "issue_comment":
        return False
    issue, comment, sender = event.get("issue") or {}, event.get("comment") or {}, event.get("sender") or {}
    return bool(
        event.get("action") == "created" and actor == OWNER
        and sender.get("login") == OWNER
        and (comment.get("user") or {}).get("login") == OWNER
        and comment.get("body", "").strip() == TRIGGER
        and issue.get("number") in (1, 2)
        and not issue.get("pull_request")
    )

def task_policy(number):
    policy = json.loads(pathlib.Path(POLICY).read_text(encoding="utf-8"))
    for task in policy["tasks"]:
        if task["issue"] == number:
            return task
    raise ValueError("Task is not in the explicitly authorized queue")

def select(issues, prs, policy, *, master_has_upstream):
    # No overlapping AI-written review PRs, no duplicate retries.
    if any(p.get("state", "OPEN").upper() == "OPEN" and
           (p.get("title", "").startswith("MAID AUTO:") or p.get("headRefName", "").startswith("autopilot/maid-auto-"))
           for p in prs):
        return None
    by_number = {i["number"]: i for i in issues if i.get("number")}
    for task in policy["tasks"]:
        num = task["issue"]
        issue = by_number.get(num)
        if not issue or issue.get("state") != "OPEN":
            continue
        if issue.get("author", {}).get("login") != OWNER:
            continue
        if "maid:blocked" in issue.get("labels", []):
            continue
        if any(p.get("title", "").startswith("MAID AUTO: I%02d" % num) for p in prs):
            continue  # Never regenerate duplicates after successful PR.
        if num == 1:
            if master_has_upstream:
                continue
            if not any(p.get("number") == 14 and p.get("state") == "OPEN" for p in prs):
                continue
        elif not master_has_upstream:
            continue  # M0 upstream not merged. No premature implementation.
        elif any(by_number.get(dep, {}).get("state") != "CLOSED" for dep in task.get("dependsOn", [])):
            continue
        return task
    return None

def changed_paths(root="."):
    result = command("git", "status", "--porcelain", "-uall")
    paths = []
    for line in result.splitlines():
        if not line.strip(): continue
        path = line[3:]
        if " -> " in path:
            raise ValueError("renames are prohibited in automation")
        paths.append(path)
    return paths

def validate(task, root="."):
    paths = changed_paths(root)
    if not paths:
        raise ValueError("Agent produced no code change")
    if len(paths) > task["maxFiles"]:
        raise ValueError("Too many changed paths: %s" % paths)
    total = 0
    for name in paths:
        if not any(fnmatch.fnmatchcase(name, pat) for pat in task["allowedPaths"]):
            raise ValueError("Out-of-scope path: %s" % name)
        p = pathlib.Path(root) / name
        if not p.is_file() or p.is_symlink():
            raise ValueError("Deleted files or symlinks prohibited: %s" % name)
        total += p.stat().st_size
    if total > task["maxBytes"]:
        raise ValueError("Max changed file bytes exceeded")
    if task["issue"] == 1:
        scripts = json.loads(pathlib.Path(root, "package.json").read_text())["scripts"]
        if scripts.get("lint") != "expo lint" or "jest" not in scripts.get("test", ""):
            raise ValueError("Lint/test script weakened or replaced")
    return paths

def append_output(**values):
    path = os.getenv("GITHUB_OUTPUT")
    if path:
        with open(path, "a", encoding="utf-8") as f:
            for key, val in values.items(): f.write(f"{key}={val}\n")

def main():
    subcommand = sys.argv[1]
    if subcommand == "admit":
        event = json.loads(pathlib.Path(os.environ["GITHUB_EVENT_PATH"]).read_text())
        ok = authorize(event, os.environ["GITHUB_EVENT_NAME"], os.getenv("GITHUB_ACTOR", ""))
        append_output(authorized=str(ok).lower())
        print("MAID_AUTONOMY_ADMIT", ok)
    elif subcommand == "select":
        policy = json.loads(pathlib.Path(POLICY).read_text())
        issues_raw = json.loads(command("gh", "issue", "list", "-R", REPO, "--state", "all", "--limit", "100",
                                     "--json", "number,state,author,labels"))
        issues = [{"number": v["number"], "state": v["state"], "author": v["author"],
                   "labels": [p["name"] for p in v["labels"]]} for v in issues_raw]
        prs = json.loads(command("gh", "pr", "list", "-R", REPO, "--state", "all", "--limit", "100",
                                "--json", "number,state,title,headRefName"))
        upstream = command("gh", "api", "repos/"+REPO+"/contents/package.json", "--jq", ".path") == "package.json" \
                   if os.getenv("MAID_BASELINE_HINT") == "yes" else False
        # Master baseline detection via GH API status; no git branch guess.
        if not upstream:
            p = subprocess.run(["gh","api","repos/"+REPO+"/contents/package.json"],capture_output=True,text=True)
            upstream = p.returncode == 0
        task = select(issues, prs, policy, master_has_upstream=upstream)
        if task:
            blob = base64.b64encode(json.dumps(task, separators=(",", ":")).encode()).decode()
            append_output(selected="true", task=blob, issue=str(task["issue"]))
            print("SELECTED_ISSUE", task["issue"], "BASE", task["base"], "MASTER_UPSTREAM", upstream)
        else:
            append_output(selected="false", task="", issue="")
            print("NO_ELIGIBLE_ISSUE: review PRs/dependencies or blocked tasks")
    elif subcommand == "validate":
        task = json.loads(pathlib.Path(sys.argv[2]).read_text())
        print("MAID_ALLOWED_DIFF", json.dumps(validate(task)))
    else:
        raise SystemExit("Unknown subcommand")

if __name__ == "__main__":
    main()
