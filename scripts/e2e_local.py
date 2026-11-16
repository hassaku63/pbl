#!/usr/bin/env python3
# coding: utf-8
"""
Run the tier A end-to-end tests (space administrator operations) locally and write a report.

Tier A tests are never run in CI: they need administrator rights, may handle personal data and
may have side effects outside Backlog (e.g. a registration mail). This script:

1. refuses to run in CI,
2. lists what the tests will create and delete, and asks for confirmation,
3. runs the tests with BACKLOG_E2E_ADMIN=1,
4. writes a Markdown report with the result of each test and the endpoints it called
   (HTTP method and path with IDs replaced). The report never contains request or response data,
   so it can be pasted into an issue or pull request.

Usage:
    BACKLOG_E2E_SPACE=... BACKLOG_E2E_API_KEY=... [BACKLOG_E2E_USER_EMAIL=...] \\
        python scripts/e2e_local.py [--yes] [--report e2e-report.md] [--all]

    --all   also run the tier R tests (and tier W ones when BACKLOG_E2E_WRITE=1)
"""

import argparse
import datetime
import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLAN = """\
Tier A tests about to run against space "{space}":

- User round trip (tests.e2e.test_admin.TestUserAdmin): {user_plan}

Resources are named with the "pbl-e2e-" prefix. Leftover users of earlier runs with that prefix are deleted.
"""


def in_ci(environ=None):
    environ = os.environ if environ is None else environ
    return bool(environ.get("GITHUB_ACTIONS") or environ.get("CI"))


def normalize_path(uri, project_key=None):
    """
    "users/12345" -> "users/:id", "issues/TEST-12/comments" -> "issues/:issueKey/comments".
    The report shows only these normalized paths.
    """
    parts = []
    for segment in uri.split("?")[0].strip("/").split("/"):
        if re.fullmatch(r"\d+", segment):
            segment = ":id"
        elif project_key and segment == project_key:
            segment = ":projectKey"
        elif re.fullmatch(r"[A-Z][A-Z0-9_]*-\d+", segment):
            segment = ":issueKey"
        parts.append(segment)
    return "/".join(parts)


class RecordingResult(unittest.TextTestResult):
    """
    Records the outcome of each test and the endpoints it called. Failure details are kept only for
    AssertionError, whose messages come from tests/e2e/assertions.py and contain no response values.
    """

    calls = None  # list shared with the request recorder

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.records = []
        self._start = 0

    def startTest(self, test):
        self._start = len(self.calls)
        super().startTest(test)

    def _record(self, test, outcome, detail=""):
        endpoints = sorted(set(self.calls[self._start:]))
        self.records.append((test.id(), outcome, detail, endpoints))

    def addSuccess(self, test):
        super().addSuccess(test)
        self._record(test, "passed")

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self._record(test, "failed", str(err[1]))

    def addError(self, test, err):
        super().addError(test, err)
        self._record(test, "error", err[0].__name__)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self._record(test, "skipped", reason)


def render_report(records, started, tiers):
    counts = {}
    for _, outcome, _, _ in records:
        counts[outcome] = counts.get(outcome, 0) + 1
    lines = [
        "# python-backlog E2E report",
        "",
        "- Run at: {} (UTC)".format(started.strftime("%Y-%m-%d %H:%M")),
        "- Tiers: {}".format(", ".join(tiers)),
        "- Result: {}".format(", ".join("{} {}".format(n, k) for k, n in sorted(counts.items())) or "no tests"),
        "",
        "This report contains no request or response data; paths have IDs replaced.",
        "",
        "| Test | Result | Detail | Endpoints |",
        "|---|---|---|---|",
    ]
    for test_id, outcome, detail, endpoints in records:
        cell = "<br>".join("`{} {}`".format(m, p) for m, p in endpoints) or "—"
        lines.append("| `{}` | {} | {} | {} |".format(
            test_id.replace("tests.e2e.", ""), outcome, detail.replace("|", "\\|").replace("\n", " "), cell))
    return "\n".join(lines) + "\n"


def install_recorder(calls, project_key):
    from tests.e2e import support

    original_send = support.ThrottledBacklogAPI._send
    original_raw = support.ThrottledBacklogAPI.raw_request

    def _send(self, method, uri, *args, **kwargs):
        calls.append((method.upper(), normalize_path(uri, project_key)))
        return original_send(self, method, uri, *args, **kwargs)

    def raw_request(self, method, uri):
        calls.append((method.upper(), normalize_path(uri, project_key)))
        return original_raw(self, method, uri)

    support.ThrottledBacklogAPI._send = _send
    support.ThrottledBacklogAPI.raw_request = raw_request


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--yes", action="store_true", help="do not ask for confirmation")
    parser.add_argument("--report", default="e2e-report.md", help="report file (default: e2e-report.md)")
    parser.add_argument("--all", action="store_true", help="also run the tier R/W tests")
    args = parser.parse_args(argv)

    if in_ci():
        print("Refusing to run: tier A tests never run in CI (GITHUB_ACTIONS or CI is set).", file=sys.stderr)
        return 2
    space = os.environ.get("BACKLOG_E2E_SPACE")
    if not space or not os.environ.get("BACKLOG_E2E_API_KEY"):
        print("Set BACKLOG_E2E_SPACE and BACKLOG_E2E_API_KEY (the key of a space administrator).", file=sys.stderr)
        return 2

    user_plan = (
        "creates a viewer user with the address in BACKLOG_E2E_USER_EMAIL (Backlog may send it a registration "
        "mail), renames it and deletes it."
        if os.environ.get("BACKLOG_E2E_USER_EMAIL") else "skipped (BACKLOG_E2E_USER_EMAIL is not set)."
    )
    print(PLAN.format(space=space, user_plan=user_plan))
    if args.all:
        print("Tier R tests{} also run.\n".format(
            " and tier W tests" if os.environ.get("BACKLOG_E2E_WRITE") == "1" else ""))
    if not args.yes and input("Continue? [y/N] ").strip().lower() not in ("y", "yes"):
        print("Aborted.")
        return 1

    os.environ["BACKLOG_E2E_ADMIN"] = "1"
    sys.path.insert(0, ROOT)
    calls = []
    install_recorder(calls, os.environ.get("BACKLOG_E2E_PROJECT_KEY"))

    loader = unittest.TestLoader()
    if args.all:
        suite = loader.discover(os.path.join(ROOT, "tests", "e2e"), top_level_dir=ROOT)
    else:
        suite = loader.loadTestsFromName("tests.e2e.test_admin")
    RecordingResult.calls = calls
    started = datetime.datetime.now(datetime.timezone.utc)
    result = unittest.TextTestRunner(resultclass=RecordingResult, verbosity=2).run(suite)

    tiers = ["A"] + (["R"] + (["W"] if os.environ.get("BACKLOG_E2E_WRITE") == "1" else []) if args.all else [])
    with open(args.report, "w", encoding="utf-8") as f:
        f.write(render_report(result.records, started, tiers))
    print("\nWrote {}".format(args.report))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
