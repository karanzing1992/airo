#!/usr/bin/env python3
"""One-call Groq structured-output code editor with deterministic path policy."""
import fnmatch
import json
import os
import pathlib
import sys

MODEL = "openai/gpt-oss-120b"
BASE_URL = "https://api.groq.com/openai/v1/chat/completions"

def valid_path(name, patterns):
    if not isinstance(name, str) or not name or len(name) > 256:
        return False
    p=pathlib.PurePosixPath(name)
    return not p.is_absolute() and ".." not in p.parts and name==str(p) and not name.startswith(".git") and any(
        fnmatch.fnmatchcase(name,pat) for pat in patterns
    )

def source_context(task, root):
    # Only owner-approved source files. No git config, environment, keys or user data.
    samples=[]
    if task["issue"] == 1:
        candidates=["package.json", "eslint.config.js", "eslint.config.mjs", ".eslintrc.js"]
    else:
        candidates=["docs/maid/PRODUCT_SCOPE_V1.md","docs/maid/WEB_MOBILE_PARITY.md","docs/maid/INTEGRATIONS_AND_MODELS.md","packages/protocol/package.json"]
    for name in candidates:
        p=root/name
        if p.is_file() and not p.is_symlink():
            raw=p.read_text(encoding="utf-8")
            samples.append({"path":name, "content":raw[:20000]})
    return samples

def api_payload(task, context):
    schema={"type":"object","properties":{
        "files":{"type":"array","items":{"type":"object","properties":{
            "path":{"type":"string"},"content":{"type":"string"}
        },"required":["path","content"],"additionalProperties":False}}
    },"required":["files"],"additionalProperties":False}
    instruction=(
        "Return ONLY strict JSON matching supplied schema. You are the MAID autonomous software engineer. "
        "Create concrete source files, not advice, code fences or pseudo-task descriptions. "
        "Only trusted owner workflow metadata is supplied, not untrusted issue text. "
        "Change files ONLY from these approved paths: "+", ".join(task["allowedPaths"])+". "
        "Every file object contains its complete desired UTF-8 contents. "
        "Do not remove existing scripts, dependencies or application features. "
        "For issue 1 preserve every existing package.json key and its existing script entries, "
        "add correct compatible ESLint development dependencies and config, do not generate yarn.lock "
        "(CI will update it). No credentials, production deployment, real host operations or claims of test pass. "
        "Avoid code comments that claim the features are deployed. Task: "+task["prompt"]
    )
    return {"model":MODEL,
       "messages":[{"role":"user","content":instruction+"\n\nTrusted source context:\n"+json.dumps(context,ensure_ascii=False)}],
       "response_format":{"type":"json_schema","json_schema":{"name":"maid_approved_file_changes","strict":True,"schema":schema}},
       "reasoning_effort":"medium","max_completion_tokens":8192,"temperature":0.2,"stream":False}

def validated_files(result,task,root):
    if not isinstance(result,dict) or not isinstance(result.get("files"),list):
        raise ValueError("Response did not contain a JSON files list")
    entries=result["files"]
    if not entries or len(entries)>task["maxFiles"]:
        raise ValueError("Empty or oversized edit list")
    seen=set()
    size=0
    writes=[]
    for ent in entries:
        if not isinstance(ent,dict) or set(ent)!={"path","content"}:
            raise ValueError("Invalid file object")
        path,text=ent["path"],ent["content"]
        if not valid_path(path,task["allowedPaths"]) or path in seen or not isinstance(text,str):
            raise ValueError("Out-of-policy, duplicate or invalid file edit")
        seen.add(path)
        size+=len(text.encode())
        p=(root/path)
        # Resolve all ancestors and prevent symlink escapes before writing.
        if not p.resolve().is_relative_to(root.resolve()) or p.is_symlink():
            raise ValueError("Symlink or repository traversal")
        if p.exists() and not p.is_file():
            raise ValueError("Non-file destination")
        writes.append((p,text))
    if size>task["maxBytes"]:
        raise ValueError("Cumulative edits exceed byte limit")
    if task["issue"]==1:
        old=json.loads((root/"package.json").read_text())
        new_entry=next((text for path,text in writes if path==root/"package.json"),None)
        if new_entry is not None:
            new=json.loads(new_entry)
            if old.get("scripts")!=new.get("scripts") or old.get("dependencies")!=new.get("dependencies"):
                raise ValueError("Upstream scripts or production dependencies changed")
            for key,version in old.get("devDependencies",{}).items():
                if new.get("devDependencies",{}).get(key)!=version:
                    raise ValueError("Upstream existing dev dependency changed: "+key)
            if "eslint" not in new.get("devDependencies",{}) or "eslint-config-expo" not in new.get("devDependencies",{}):
                raise ValueError("ESLint dependencies missing")
    return writes

def main():
    task=json.loads(pathlib.Path(sys.argv[1]).read_text())
    root=pathlib.Path.cwd()
    token=os.environ.get("GROQ_API_KEY")
    if not token: raise SystemExit("GROQ_API_KEY absent: fail closed")
    try:
        from groq import Groq
    except ImportError:
        raise SystemExit("GROQ_OFFICIAL_SDK_MISSING")
    payload=api_payload(task,source_context(task,root))
    try:
        with Groq(api_key=token,timeout=130,max_retries=0) as client:
            response=client.chat.completions.create(**payload)
            content=response.choices[0].message.content
    except Exception as exc:
        # No provider response body or sensitive request data is ever logged.
        raise SystemExit("GROQ_SDK_ERROR "+str(getattr(exc,"status_code",type(exc).__name__)))
    try:
        response=json.loads(content)
        writes=validated_files(response,task,root)
    except Exception as exc:
        raise SystemExit("GROQ_INVALID_FILE_EDIT "+str(exc)[:180])
    for path,text in writes:
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(text,encoding="utf-8")
    print("GROQ_STRUCTURED_FILES_WRITTEN",json.dumps([str(p.relative_to(root)) for p,_ in writes]))
    print("MODEL",MODEL,"source-only; test and release status unknown")

if __name__=="__main__":
    main()
