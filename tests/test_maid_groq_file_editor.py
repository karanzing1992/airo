import importlib.util
import json
import pathlib
import tempfile
import unittest

root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("groq_writer",root/"scripts/maid_groq_file_editor.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class StructuredWriterTests(unittest.TestCase):
    def setUp(self):
        self.task=json.loads((root/"docs/maid/AUTONOMOUS_ISSUE_POLICY.json").read_text())["tasks"][0]
    def test_traversal_denied(self):
        for path in ("../steal","/etc/passwd",".git/config","foo/../../package.json","package.json/../README.md"):
            self.assertFalse(m.valid_path(path,self.task["allowedPaths"]))
    def test_approved_files(self):
        self.assertTrue(m.valid_path("package.json",self.task["allowedPaths"]))
        self.assertTrue(m.valid_path("eslint.config.mjs",self.task["allowedPaths"]))
        self.assertFalse(m.valid_path("src/secret.ts",self.task["allowedPaths"]))
    def test_schema_is_strict(self):
        p=m.api_payload(self.task,[])
        fmt=p["response_format"]["json_schema"]
        self.assertTrue(fmt["strict"])
        self.assertEqual(p["model"],"qwen/qwen3.8-27b")
        self.assertEqual(fmt["schema"]["additionalProperties"],False)
    def test_reject_dependency_regression(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=pathlib.Path(tmp)
            src={"scripts":{"lint":"expo lint","test":"jest --ci"},"dependencies":{"react":"19"},"devDependencies":{"typescript":"6"}}
            (r/"package.json").write_text(json.dumps(src))
            bad=dict(src)
            bad["scripts"]={"lint":"echo ok","test":"jest --ci"}
            with self.assertRaises(ValueError):
                m.validated_files({"files":[{"path":"package.json","content":json.dumps(bad)}]},self.task,r)
    def test_reject_missing_eslint_dependency(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=pathlib.Path(tmp)
            src={"scripts":{"lint":"expo lint","test":"jest --ci"},"dependencies":{},"devDependencies":{}}
            (r/"package.json").write_text(json.dumps(src))
            with self.assertRaises(ValueError):
                m.validated_files({"files":[{"path":"package.json","content":json.dumps(src)}]},self.task,r)
    def test_allow_valid_dev_dependencies(self):
        with tempfile.TemporaryDirectory() as tmp:
            r=pathlib.Path(tmp)
            src={"scripts":{"lint":"expo lint","test":"jest --ci"},"dependencies":{},"devDependencies":{}}
            (r/"package.json").write_text(json.dumps(src))
            new=dict(src,devDependencies={"eslint":"^9.0.0","eslint-config-expo":"~11.0.0"})
            writes=m.validated_files({"files":[{"path":"package.json","content":json.dumps(new)}]},self.task,r)
            self.assertEqual(len(writes),1)
if __name__=="__main__":unittest.main()
