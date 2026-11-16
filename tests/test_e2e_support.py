# coding: utf-8
"""
Offline tests for the end-to-end test support code, and enforcement of tests/e2e/README.md.
"""

import datetime
import glob
import os
import re
import subprocess
import sys
import unittest

from tests.e2e import assertions as check
from tests.e2e import mask
from tests.e2e.support import PREFIX, is_leftover, resource_name

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET = "taro.yamada@example.com"


class TestAssertions(unittest.TestCase):
    def _message(self, func, *args, **kwargs):
        with self.assertRaises(AssertionError) as cm:
            func(*args, **kwargs)
        return str(cm.exception)

    def test_messages_never_contain_values(self):
        user = {"id": 1, "name": "Taro Yamada", "mailAddress": SECRET}
        messages = [
            self._message(check.has_keys, user, "id", "lang", what="user"),
            self._message(check.field_equals, user, "mailAddress", "other@example.com", what="user"),
            self._message(check.field_type, user, "mailAddress", int, what="user"),
            self._message(check.is_list, user, what="users"),
            self._message(check.is_list, [user], what="users", min_length=2),
            self._message(check.is_list, [user], what="users", item_keys=("lang",)),
            self._message(check.contains_id, [user], 2, what="users"),
            self._message(check.is_count, user, what="count"),
        ]
        for message in messages:
            with self.subTest(message=message):
                self.assertNotIn(SECRET, message)
                self.assertNotIn("Taro", message)

    def test_messages_name_the_problem(self):
        self.assertIn("lang", self._message(check.has_keys, {"id": 1}, "id", "lang"))
        self.assertIn("'summary'", self._message(check.field_equals, {"summary": "a"}, "summary", "b"))
        self.assertIn("expected 1", self._message(check.is_count, {"count": 0}, expected=1))

    def test_passing_checks(self):
        check.has_keys({"id": 1, "issueKey": "A-1"}, "id", "issueKey")
        check.field_equals({"summary": "s"}, "summary", "s")
        check.field_type({"id": 1}, "id", int)
        check.is_list([{"id": 1}], min_length=1, item_keys=("id",))
        check.is_count({"count": 3}, expected=3)
        check.contains_id([{"id": 1}, {"id": 2}], 2)
        check.is_true(True, "never shown")


class TestNamingAndLeftovers(unittest.TestCase):
    def test_resource_name(self):
        self.assertTrue(resource_name("issue").startswith(PREFIX))
        self.assertTrue(resource_name("issue").endswith("-issue"))

    def test_is_leftover(self):
        now = datetime.datetime(2026, 11, 16, 12, 0, tzinfo=datetime.timezone.utc)
        self.assertTrue(is_leftover(PREFIX + "1-issue", "2026-11-16T10:00:00Z", now=now))
        self.assertFalse(is_leftover(PREFIX + "1-issue", "2026-11-16T11:30:00Z", now=now))  # may belong to a running test
        self.assertFalse(is_leftover("user issue", "2026-11-01T00:00:00Z", now=now))
        self.assertFalse(is_leftover(None, "2026-11-01T00:00:00Z", now=now))


class TestMask(unittest.TestCase):
    def test_personal_values(self):
        user = {"id": 1, "userId": "taro", "name": "Taro Yamada", "mailAddress": SECRET, "roleType": 1,
                "nulabAccount": {"nulabId": "abc", "name": "Taro", "uniqueId": "u-1"}}
        self.assertEqual(sorted(["taro", "Taro Yamada", SECRET, "abc", "Taro", "u-1"]), mask.personal_values(user))


class TestTierAGuard(unittest.TestCase):
    def test_admin_tier_refuses_to_load_in_ci(self):
        env = dict(os.environ, BACKLOG_E2E_ADMIN="1", GITHUB_ACTIONS="true")
        result = subprocess.run([sys.executable, "-c", "import tests.e2e.support"], cwd=ROOT, env=env,
                                capture_output=True, text=True)
        self.assertNotEqual(0, result.returncode)
        self.assertIn("must not be set in CI", result.stderr)


class TestGuidelinesAreFollowed(unittest.TestCase):
    """
    tests/e2e/README.md rule 2 and 3: no self.assert* and no print() in end-to-end test modules.
    """

    def test_no_unittest_assertions_or_print(self):
        forbidden = re.compile(r"\bself\.assert\w*\(|(?<![\w.])print\(")
        for path in sorted(glob.glob(os.path.join(ROOT, "tests", "e2e", "test_*.py"))):
            with open(path, encoding="utf-8") as f:
                for number, line in enumerate(f, 1):
                    with self.subTest(file=os.path.basename(path), line=number):
                        self.assertIsNone(forbidden.search(line), "use tests/e2e/assertions.py instead")


if __name__ == "__main__":
    unittest.main()
