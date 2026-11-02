#!/usr/bin/env python3
"""Reproducible upstream MAID SDK 57 ESLint bootstrap, not a lint bypass."""
import json
import pathlib
import sys

ESLINT_VERSION = "^9.39.1"
EXPO_CONFIG_VERSION = "57.0.2"
CONFIG = """const { defineConfig } = require('eslint/config');
const expoConfig = require('eslint-config-expo/flat');

module.exports = defineConfig([
  expoConfig,
]);
"""

def prepare(root,task):
    if task["issue"] != 1:
        raise ValueError("Only M0 lint issue #1 can use deterministic bootstrap")
    path=root/"package.json"
    original=json.loads(path.read_text(encoding="utf-8"))
    if original.get("scripts",{}).get("lint")!="expo lint" or "jest" not in original.get("scripts",{}).get("test",""):
        raise ValueError("Unexpected baseline scripts")
    if not str(original.get("dependencies",{}).get("expo","")).startswith("^57."):
        raise ValueError("SDK mismatch: expected pinned Expo 57")
    if (root/"eslint.config.js").exists() or (root/"eslint.config.mjs").exists():
        raise ValueError("Existing ESLint config must be reviewed, not overwritten")
    out=json.loads(json.dumps(original))
    dev=out.setdefault("devDependencies",{})
    for name,version in (("eslint",ESLINT_VERSION),("eslint-config-expo",EXPO_CONFIG_VERSION)):
        if name in dev and dev[name] != version:
            raise ValueError("Conflicting existing ESLint dependency: "+name)
        dev[name]=version
    if out["scripts"]!=original["scripts"] or out["dependencies"]!=original["dependencies"]:
        raise ValueError("Runtime or lint scripts changed")
    return json.dumps(out,indent=2,ensure_ascii=False)+"\n",CONFIG

def main():
    root=pathlib.Path.cwd()
    task=json.loads(pathlib.Path(sys.argv[1]).read_text())
    package,config=prepare(root,task)
    (root/"package.json").write_text(package,encoding="utf-8")
    (root/"eslint.config.js").write_text(config,encoding="utf-8")
    print("M0_PINNED_ESLINT_BOOTSTRAP: expo57/57.0.2, eslint9, no runtime code changes")
    print("Tests and official lint must still pass; no certification from file generation alone")

if __name__=="__main__":main()
