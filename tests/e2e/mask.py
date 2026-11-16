# coding: utf-8
"""
Print GitHub Actions ::add-mask:: commands for the personal data of the API key's user
(name, mail address, user ID, Nulab account), so that they are masked in the rest of the job's log.

Run it in CI before the tests:  python -m tests.e2e.mask
It never prints any value except inside ::add-mask:: commands, which GitHub does not display.
"""

import sys

from tests.e2e.support import CONFIGURED, client


def personal_values(user):
    values = [user.get("name"), user.get("mailAddress"), user.get("userId")]
    account = user.get("nulabAccount") or {}
    values += [account.get("name"), account.get("uniqueId"), account.get("nulabId")]
    return sorted({str(v) for v in values if v})


def main():
    if not CONFIGURED:
        print("mask: e2e is not configured; nothing to mask")
        return 0
    try:
        user = client().user.get_myself()
    except Exception as e:  # noqa: BLE001 - report the error type only, never the response
        print("::error::mask: could not read users/myself ({})".format(type(e).__name__))
        return 1
    for value in personal_values(user):
        print("::add-mask::{}".format(value))
    print("mask: masked the personal data of the API key's user")
    return 0


if __name__ == "__main__":
    sys.exit(main())
