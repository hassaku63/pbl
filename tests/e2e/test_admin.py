# coding: utf-8
"""
Tier A: space administrator operations. These never run in CI: run them locally with
scripts/e2e_local.py, which asks for confirmation and writes a report without response data.

User round trip (User.add/update/delete, deprecated since 0.18.0 because they are no longer in the official
API documentation and are reported not to work on the new plans; this test records whether they still work):
runs only when BACKLOG_E2E_USER_EMAIL is set. Backlog may send a registration mail to that
address, so use an address you own. The user is created with the viewer role and deleted again.
"""

import os
import secrets
import unittest

from tests.e2e import assertions as check
from tests.e2e.support import RUN_ID, client, is_previous_run, requires_local_admin, resource_name

USER_EMAIL = os.environ.get("BACKLOG_E2E_USER_EMAIL")
VIEWER = 4


@requires_local_admin
@unittest.skipUnless(USER_EMAIL, "BACKLOG_E2E_USER_EMAIL is not set")
class TestUserAdmin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.api = client()
        # Delete users left over by earlier local runs.
        for user in cls.api.user.list():
            if is_previous_run(user.get("name")):
                cls.api.user.delete(user["id"])

    def test_user_round_trip(self):
        name = resource_name("user")
        user = self.api.user.add(
            userId="pble2e{}".format(RUN_ID),
            password=secrets.token_urlsafe(24),
            name=name,
            mailAddress=USER_EMAIL,
            roleType=VIEWER,
        )
        try:
            check.field_equals(user, "name", name, what="user.add()")
            check.field_type(user, "id", int, what="user.add()")
            renamed = resource_name("user-renamed")
            check.field_equals(self.api.user.update(user["id"], name=renamed), "name", renamed, what="user.update()")
            check.field_equals(self.api.user.get(user["id"]), "name", renamed, what="user.get()")
        finally:
            self.api.user.delete(user["id"])
