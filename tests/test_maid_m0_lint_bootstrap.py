import importlib.util
import json
import pathlib
import tempfile
import unittest
root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("m0",root/"scripts/maid_m0_lint_bootstrap.py")
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
class M0LintTests(unittest.TestCase):
    def setUp(self):
        self.task=json.loads((root/"docs/maid/AUTONOMOUS_ISSUE_POLICY.json").read_text())["tasks"][0]
        self.source={"scripts":{"lint":"expo lint","test":"jest --ci"},"dependencies":{"expo":"^57.0.0","react":"19.2.3"},"devDependencies":{"typescript":"~6.0.3"}}
    def test_pins_compatible_deps_and_preserves_scripts(self):
        with tempfile.TemporaryDirectory() as temp:
            p=pathlib.Path(temp);(p/"package.json").write_text(json.dumps(self.source))
            txt,config=m.prepare(p,self.task)
            pkg=json.loads(txt)
            self.assertEqual(pkg["scripts"],self.source["scripts"])
            self.assertEqual(pkg["dependencies"],self.source["dependencies"])
            self.assertEqual(pkg["devDependencies"]["typescript"],"~6.0.3")
            self.assertEqual(pkg["devDependencies"]["eslint-config-expo"],"57.0.2")
            self.assertEqual(pkg["devDependencies"]["eslint"],m.ESLINT_VERSION)
            self.assertIn('eslint-config-expo/flat',config)
    def test_refuses_existing_config(self):
        with tempfile.TemporaryDirectory() as temp:
            p=pathlib.Path(temp);(p/"package.json").write_text(json.dumps(self.source))
            (p/"eslint.config.js").write_text("original")
            with self.assertRaises(ValueError):m.prepare(p,self.task)
    def test_refuses_wrong_sdk(self):
        with tempfile.TemporaryDirectory() as temp:
            p=pathlib.Path(temp);x=dict(self.source,dependencies={"expo":"^56.0.0"})
            (p/"package.json").write_text(json.dumps(x))
            with self.assertRaises(ValueError):m.prepare(p,self.task)
    def test_refuses_other_issue(self):
        with tempfile.TemporaryDirectory() as temp:
            p=pathlib.Path(temp);(p/"package.json").write_text(json.dumps(self.source))
            with self.assertRaises(ValueError):m.prepare(p,{"issue":13})
if __name__=="__main__":unittest.main()
