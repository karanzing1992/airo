import importlib.util
import json
import pathlib
import unittest

root=pathlib.Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("maid_autonomy",root/"scripts/maid_autonomy.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def event():
    return {"action":"created","issue":{"number":1},"comment":{"body":"/maid-autonomous-run","user":{"login":"karanzing1992"}},"sender":{"login":"karanzing1992"}}

def issue(n,state="OPEN"):
    return {"number":n,"state":state,"author":{"login":"karanzing1992"},"labels":[]}

def policy():
    return json.loads((root/"docs/maid/AUTONOMOUS_ISSUE_POLICY.json").read_text())

class Admission(unittest.TestCase):
    def test_valid_owner(self): self.assertTrue(mod.authorize(event(),"issue_comment","karanzing1992"))
    def test_non_owner(self): self.assertFalse(mod.authorize(event(),"issue_comment","outsider"))
    def test_wrong_comment(self):
        e=event();e["comment"]["body"]="/maid-autonomous-run && curl evil"
        self.assertFalse(mod.authorize(e,"issue_comment","karanzing1992"))
    def test_wrong_author(self):
        e=event();e["comment"]["user"]["login"]="other"
        self.assertFalse(mod.authorize(e,"issue_comment","karanzing1992"))
    def test_pr_denied(self):
        e=event();e["issue"]["pull_request"]={"url":"somewhere"}
        self.assertFalse(mod.authorize(e,"issue_comment","karanzing1992"))
    def test_schedule_allowed(self): self.assertTrue(mod.authorize({},"schedule","github-actions[bot]"))
    def test_unowned_dispatch_denied(self): self.assertFalse(mod.authorize({},"workflow_dispatch","visitor"))
    def test_existing_pr_prevents_duplicate(self):
        task=mod.select([issue(1)],[{"number":14,"state":"OPEN","title":"M0","headRefName":"bootstrap"},{"state":"OPEN","title":"MAID AUTO: I01 bounded implementation","headRefName":"autopilot/maid-auto-i01-123"}],policy(),master_has_upstream=False)
        self.assertIsNone(task)
    def test_import_issue_selected(self):
        self.assertEqual(mod.select([issue(1)],[{"number":14,"state":"OPEN","title":"M0","headRefName":"bootstrap"}],policy(),master_has_upstream=False)["issue"],1)
    def test_dep_blocks_phase_two(self):
        self.assertIsNone(mod.select([issue(1),issue(2)],[],policy(),master_has_upstream=True))
    def test_phase_two_unblocks_after_m0_acceptance(self):
        task=mod.select([issue(1,"CLOSED"),issue(2)],[],policy(),master_has_upstream=True)
        self.assertEqual(task["issue"],2)
    def test_blocked_issue_skipped(self):
        a=issue(1);a["labels"]=["maid:blocked"]
        self.assertIsNone(mod.select([a],[{"number":14,"state":"OPEN","title":"M0","headRefName":"bootstrap"}],policy(),master_has_upstream=False))
    def test_lint_may_not_be_disabled(self):
        a=policy()["tasks"][0]
        self.assertEqual(a["issue"],1)
        self.assertIn("package.json",a["allowedPaths"])

if __name__=="__main__":unittest.main()
