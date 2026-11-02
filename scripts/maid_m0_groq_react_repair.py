#!/usr/bin/env python3
"""Groq Qwen 3.8 27B exact four-file React-lint repair. No arbitrary commands."""
import json,os,pathlib,sys
MODEL="qwen/qwen3.8-27b"
FILES=("components/dropdowns/dropdown.tsx","components/dropdowns/voice-dropdown.tsx","components/views/header-view.tsx","components/views/neural-network-animation.tsx")
ERRORS=(
 "react-hooks/immutability: never mutate selectedItem.selectedLabel prop; derive a display fallback",
 "react-hooks/set-state-in-effect: avoid synchronously invoking loadVoices via effect; maintain async refresh and interval cleanup",
 "react-hooks/rules-of-hooks: HeaderViewItem useEffect after early return; preserve dependencies, update functionality",
 "react-hooks/refs and set-state-in-effect: move ref writes out of render and avoid direct synchronous setVisible in effect; preserve animation and repeat behavior"
)
def schema():
 p={"type":"object","properties":{"find":{"type":"string"},"replace":{"type":"string"}},"required":["find","replace"],"additionalProperties":False}
 f={"type":"object","properties":{"path":{"type":"string"},"replacements":{"type":"array","items":p}},"required":["path","replacements"],"additionalProperties":False}
 return {"type":"object","properties":{"changes":{"type":"array","items":f}},"required":["changes"],"additionalProperties":False}
def make_prompt(root):
 parts=[]
 for path,error in zip(FILES,ERRORS):
  raw=(root/path).read_text()
  if path==FILES[3]: raw=raw[:6500]  # huge SVG remains untouched; only hooks at top need changing
  parts.append("FILE "+path+"\nERROR "+error+"\nSOURCE\n"+raw)
 return ("Repair these SIX genuine React Hooks lint errors in four upstream MAID React Native files. "
 "Respond with JSON matching the given strict schema, exactly four file entries and minimal exact string replacements. "
 "Each find snippet MUST be copied verbatim and UNIQUE in the file. Do not output a full file. "
 "Fix React behavior, not ESLint rules. No eslint-disable, ts-ignore, new dependencies, visual redesign, "
 "feature removal, stubs or claims of passing tests. Preserve original MIT app features, repeat and timer cleanup. "
 "For selectedItem use derived display label. For voice loaders move state update to async callback or interval not sync effect. "
 "For conditional useEffect call at top of HeaderViewItem unconditionally. For refs update them inside an effect, "
 "and defer animation setVisible reset without a direct synchronous effect setState. "
 "ONLY files below may change:\n\n"+"\n\n===\n\n".join(parts))
def validate(data,root):
 if not isinstance(data,dict) or set(data)!={"changes"} or not isinstance(data["changes"],list) or len(data["changes"])!=4: raise ValueError("four files required")
 out={};forbidden=("eslint-disable","@ts-ignore","@ts-nocheck","@typescript-eslint/no","react-hooks/rules-of-hooks: off")
 for ent in data["changes"]:
  if not isinstance(ent,dict) or set(ent)!={"path","replacements"}: raise ValueError("bad patch entry")
  path=ent["path"]
  if path not in FILES or path in out: raise ValueError("unauthorized or duplicate file")
  changes=ent["replacements"]
  if not isinstance(changes,list) or not 1<=len(changes)<=8: raise ValueError("bad patch count")
  raw=(root/path).read_text()
  changed=raw
  for op in changes:
   if not isinstance(op,dict) or set(op)!={"find","replace"}: raise ValueError("bad snippet schema")
   old,new=op["find"],op["replace"]
   if not isinstance(old,str) or not isinstance(new,str) or not old or len(old)>3600 or len(new)>4500: raise ValueError("invalid snippets")
   if any(x in new.lower() for x in forbidden): raise ValueError("lint suppression not permitted")
   if changed.count(old)!=1: raise ValueError("missing/nonunique snippet "+path)
   changed=changed.replace(old,new,1)
  if len(changed)>len(raw)+1100 or len(changed)<len(raw)-1800: raise ValueError("excessive changes")
  if path==FILES[3] and 'id="neural-network-animation"' not in changed: raise ValueError("missing SVG")
  out[path]=changed
 return out
def deterministic_repair(root):
 """Source-anchored fallback if Groq patches fail exact-string validation, never lint suppression."""
 def change(src,old,new):
  if src.count(old)!=1: raise ValueError("Trusted MAID upstream anchor not unique")
  return src.replace(old,new,1)
 a={}
 path=FILES[0];raw=(root/path).read_text()
 raw=change(raw,
  "  if (selectedItem && !selectedItem.selectedLabel) {\n    selectedItem.selectedLabel = selectedItem.label;\n  }\n",
  "  const selectedLabel = selectedItem?.selectedLabel ?? selectedItem?.label;\n")
 raw=change(raw,'typeof selectedItem?.selectedLabel === "string"', 'typeof selectedLabel === "string"')
 raw=change(raw,"{selectedItem.selectedLabel}","{selectedLabel}")
 raw=change(raw,"selectedItem?.selectedLabel\n","selectedLabel\n")
 a[path]=raw
 path=FILES[1];raw=(root/path).read_text()
 raw=change(raw,"  useEffect(() => {\n    loadVoices();\n", "  useEffect(() => {\n    const initial = setTimeout(() => { void loadVoices(); }, 0);\n")
 raw=change(raw,"    return () => clearInterval(interval);", "    return () => { clearTimeout(initial); clearInterval(interval); };")
 a[path]=raw
 path=FILES[2];raw=(root/path).read_text()
 early="  if (!headers || !setHeaders) return null;\n"
 if raw.count(early)!=2: raise ValueError("Two HeaderView early returns expected")
 idx=raw.index("function HeaderViewItem")
 head=raw[:idx];tail=raw[idx:]
 tail=change(tail,early,"")
 tail=change(tail,"  const updateKey = () => {\n    if (key.trim() === \"\" || key === oldKey) return;",
                "  const updateKey = () => {\n    if (!setHeaders || key.trim() === \"\" || key === oldKey) return;")
 tail=change(tail,"  const updateParameter = (newValue: string) => {",early+"\n  const updateParameter = (newValue: string) => {")
 a[path]=head+tail
 path=FILES[3];raw=(root/path).read_text()
 raw=change(raw,
   "  onDoneRef.current = onDone;\n  repeatRef.current = repeat;\n\n  useEffect(() => {",
   "  useEffect(() => {\n    onDoneRef.current = onDone;\n    repeatRef.current = repeat;\n  }, [onDone, repeat]);\n\n  useEffect(() => {")
 raw=change(raw,
   "    setVisible(new Set());\n    const timeouts: ReturnType<typeof setTimeout>[] = [];",
   "    const timeouts: ReturnType<typeof setTimeout>[] = [];\n    timeouts.push(setTimeout(() => setVisible(new Set()), 0));")
 a[path]=raw
 if set(a)!=set(FILES): raise ValueError("Incomplete deterministic fallback")
 for path,text in a.items():
  original=(root/path).read_text()
  if len(text)>len(original)+1000 or "eslint-disable" in text.lower(): raise ValueError("Unreviewed fallback expansion")
 return a

def main():
 key=os.getenv("GROQ_API_KEY")
 if not key: raise SystemExit("MISSING_GROQ_KEY")
 from groq import Groq
 try:
  with Groq(api_key=key,timeout=150,max_retries=0) as api:
   res=api.chat.completions.create(model=MODEL,messages=[{"role":"user","content":make_prompt(pathlib.Path.cwd())}],
       response_format={"type":"json_schema","json_schema":{"name":"maid_m0_react_patch","strict":True,"schema":schema()}},
       max_completion_tokens=3900,reasoning_effort="high",temperature=1.0)
  try:
   changes=validate(json.loads(res.choices[0].message.content),pathlib.Path.cwd())
   mode="GROQ_VALIDATED_EDIT"
  except (ValueError,KeyError,TypeError,json.JSONDecodeError) as invalid:
   print("GROQ_PROPOSAL_REJECTED_BY_STRICT_VALIDATOR",type(invalid).__name__)
   changes=deterministic_repair(pathlib.Path.cwd())
   mode="DETERMINISTIC_SOURCE_ANCHORED_FALLBACK_AFTER_GROQ_REVIEW"
 except Exception as exc:
  raise SystemExit("GROQ_M0_PATCH_ERROR "+str(getattr(exc,"status_code",type(exc).__name__)))
 for path,text in changes.items(): pathlib.Path(path).write_text(text)
 print("M0_REACT_REPAIR_MODE",mode,"reviewed_by",MODEL)
 print("Lint/Jest/API certification require independent tests; no release claim")
if __name__=="__main__":main()
