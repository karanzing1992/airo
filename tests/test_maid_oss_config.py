import json
import pathlib
import unittest
ROOT = pathlib.Path(__file__).resolve().parents[1]
class GroqConfigTests(unittest.TestCase):
    def test_model_and_permissions(self):
        cfg=json.loads((ROOT/"opencode.json").read_text())
        self.assertEqual(cfg["model"],"groq/openai/gpt-oss-120b")
        self.assertEqual(cfg["permission"]["bash"],"deny")
        self.assertEqual(cfg["permission"]["external_directory"],"deny")
    def test_workflow_credential_and_owner_gate(self):
        txt=(ROOT/".github/workflows/maid-oss-agent.yml").read_text()
        self.assertIn("secrets.GROQ_API_KEY",txt)
        self.assertIn("groq/openai/gpt-oss-120b",txt)
        self.assertNotIn("ollama pull",txt)
        self.assertNotIn("ollama serve",txt)
        self.assertIn("github.event.comment.user.login == 'karanzing1992'",txt)
        self.assertIn("scripts/maid_oss_guard.py --validate-diff",txt)
if __name__ == "__main__": unittest.main()
