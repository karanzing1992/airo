import importlib.util,json,pathlib,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("maidm0",ROOT/"scripts/maid_m0_groq_react_repair.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class M0SafetyTests(unittest.TestCase):
 def test_fixed_scope(self):
  self.assertEqual(len(m.FILES),4)
  self.assertEqual(m.MODEL,'qwen/qwen3.8-27b')
  self.assertEqual(m.schema()["additionalProperties"],False)
 def setup(self,root):
  for path in m.FILES:
   p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_text('const original = 1;\nid="neural-network-animation"')
 def test_valid_minimal_snippet(self):
  with tempfile.TemporaryDirectory() as t:
   r=pathlib.Path(t);self.setup(r)
   d={"changes":[{"path":p,"replacements":[{"find":"const original = 1;","replace":"const original = 2;"}]} for p in m.FILES]}
   self.assertEqual(len(m.validate(d,r)),4)
 def test_reject_lint_suppressions(self):
  with tempfile.TemporaryDirectory() as t:
   r=pathlib.Path(t);self.setup(r)
   d={"changes":[{"path":p,"replacements":[{"find":"const original = 1;","replace":"/* eslint-disable */"}]} for p in m.FILES]}
   with self.assertRaises(ValueError):m.validate(d,r)
 def test_reject_traversal(self):
  with tempfile.TemporaryDirectory() as t:
   r=pathlib.Path(t);self.setup(r)
   d={"changes":[{"path":p,"replacements":[{"find":"const original = 1;","replace":"const original = 2;"}]} for p in m.FILES]}
   d["changes"][0]["path"]="../secrets"
   with self.assertRaises(ValueError):m.validate(d,r)
 def test_reject_nonunique_matches(self):
  with tempfile.TemporaryDirectory() as t:
   r=pathlib.Path(t);self.setup(r)
   (r/m.FILES[0]).write_text("a a")
   d={"changes":[{"path":p,"replacements":[{"find":"const original = 1;","replace":"const original = 2;"}]} for p in m.FILES]}
   d["changes"][0]["replacements"]=[{"find":"a","replace":"b"}]
   with self.assertRaises(ValueError):m.validate(d,r)

 def test_fallback_preserves_original_behavior_signatures(self):
  with tempfile.TemporaryDirectory() as t:
   r=pathlib.Path(t)
   x=[
    '  if (selectedItem && !selectedItem.selectedLabel) {\n    selectedItem.selectedLabel = selectedItem.label;\n  }\n typeof selectedItem?.selectedLabel === "string"\n {selectedItem.selectedLabel}\n selectedItem?.selectedLabel\n',
    '  useEffect(() => {\n    loadVoices();\n    return () => clearInterval(interval);',
    'function HeaderViewItem() {\n  if (!headers || !setHeaders) return null;\n  const updateKey = () => {\n    if (key.trim() === "" || key === oldKey) return;\n  const updateParameter = (newValue: string) => {',
    '  onDoneRef.current = onDone;\n  repeatRef.current = repeat;\n\n  useEffect(() => {\n    setVisible(new Set());\n    const timeouts: ReturnType<typeof setTimeout>[] = [];'
   ]
   for path,raw in zip(m.FILES,x):
    p=r/path;p.parent.mkdir(parents=True,exist_ok=True)
    if path==m.FILES[2]: raw= '  if (!headers || !setHeaders) return null;\n'+raw
    p.write_text(raw)
   d=m.deterministic_repair(r)
   self.assertEqual(len(d),4)
   self.assertNotIn("selectedItem.selectedLabel =",d[m.FILES[0]])
   self.assertIn("setTimeout(() => setVisible(new Set()), 0)",d[m.FILES[3]])
if __name__=="__main__":unittest.main()
