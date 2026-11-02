import unittest
from scripts.maid_oss_guard import owner_authorized


def valid():
    return {
        "action": "created",
        "sender": {"login": "karanzing1992"},
        "comment": {"user": {"login": "karanzing1992"}, "body": "/maid-oss"},
        "issue": {"number": 16},
    }


class AuthorizationGateTests(unittest.TestCase):
    def test_owner_pilot_accepted(self):
        self.assertTrue(owner_authorized(valid()))

    def test_other_actor_denied(self):
        x = valid()
        x["sender"]["login"] = "outsider"
        self.assertFalse(owner_authorized(x))

    def test_other_comment_author_denied(self):
        x = valid()
        x["comment"]["user"]["login"] = "outsider"
        self.assertFalse(owner_authorized(x))

    def test_other_issue_denied(self):
        x = valid()
        x["issue"]["number"] = 2
        self.assertFalse(owner_authorized(x))

    def test_pull_request_comment_denied(self):
        x = valid()
        x["issue"]["pull_request"] = {"url": "ignored"}
        self.assertFalse(owner_authorized(x))

    def test_extra_command_denied(self):
        x = valid()
        x["comment"]["body"] = "/maid-oss && do-extra"
        self.assertFalse(owner_authorized(x))

    def test_wrong_action_denied(self):
        x = valid()
        x["action"] = "edited"
        self.assertFalse(owner_authorized(x))


if __name__ == "__main__":
    unittest.main()
