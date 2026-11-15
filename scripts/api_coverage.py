#!/usr/bin/env python3
# coding: utf-8
"""
Maintain docs/API_COVERAGE.md: which Backlog API endpoints python-backlog implements.

The list of endpoints is docs/api_endpoints.json. It is maintained by hand, or by an AI agent that reads
the official API reference (see .claude/skills/api-change/SKILL.md): this script never downloads or parses
the documentation site, so it does not break when the site changes.
Implemented endpoints are found by statically analyzing backlog/*.py: every call to invoke_method()
with a literal HTTP method and a resolvable URI counts.

Usage:
    python scripts/api_coverage.py generate   # rewrite docs/API_COVERAGE.md
    python scripts/api_coverage.py check      # exit 1 if docs/API_COVERAGE.md is out of date (used in CI)

Only the standard library is used.
"""

import ast
import collections
import difflib
import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINTS_JSON = os.path.join(ROOT, "docs", "api_endpoints.json")
COVERAGE_MD = os.path.join(ROOT, "docs", "API_COVERAGE.md")

GROUP_NAMES = {
    "space": "Space", "users": "Users", "statuses": "Statuses", "priorities": "Priorities",
    "resolutions": "Resolutions", "projects": "Projects", "issues": "Issues", "documents": "Documents",
    "wikis": "Wiki", "notifications": "Notifications", "watchings": "Watching", "stars": "Stars",
    "teams": "Teams", "rateLimit": "Rate limit",
}


# ---------------------------------------------------------------------------------------------
# Static analysis of backlog/*.py
# ---------------------------------------------------------------------------------------------

def normalize(path):
    """
    "/api/v2/issues/:issueIdOrKey/comments" and "issues/{issue_id_or_key}/comments" -> "issues/*/comments"
    """
    path = re.sub(r"^/api/v2/", "", path)
    path = re.sub(r"\{[^}]*\}|:[A-Za-z]+", "*", path)
    return path.strip("/")


def _string_value(node, env, helpers):
    """
    Best-effort evaluation of an expression that builds a URI. Placeholders become "{x}".
    """
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.JoinedStr):
        return "".join(v.value if isinstance(v, ast.Constant) else "{x}" for v in node.values)
    if isinstance(node, ast.Name):
        return env.get(node.id)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left, right = _string_value(node.left, env, helpers), _string_value(node.right, env, helpers)
        return left + right if left is not None and right is not None else None
    if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
        if node.func.attr == "format" and isinstance(node.func.value, ast.Constant):
            return node.func.value.value
        # self._something_uri(...) helpers that return a URI template
        return helpers.get(node.func.attr)
    return None


def _assignments(func, helpers):
    env = {}
    for node in ast.walk(func):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            value = _string_value(node.value, env, helpers)
            if value is not None:
                env[node.targets[0].id] = value
    return env


def _uri_helpers(functions):
    """
    Methods that return a single URI template, e.g. Issue._comment_uri(): {name: template}.
    """
    helpers = {}
    for func in functions:
        returns = [n.value for n in ast.walk(func) if isinstance(n, ast.Return) and n.value is not None]
        if len(returns) == 1:
            value = _string_value(returns[0], _assignments(func, {}), {})
            if value and "/" in value:
                helpers[func.name] = value
    return helpers


def _invoke_method_calls(func, helpers):
    """
    Yield (METHOD, uri) for each invoke_method() call in the function whose arguments can be resolved.
    """
    env = _assignments(func, helpers)
    for node in ast.walk(func):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "invoke_method" and len(node.args) >= 2):
            method = _string_value(node.args[0], env, helpers)
            uri = _string_value(node.args[1], env, helpers)
            if method and uri:
                yield method.upper(), uri


def implemented_endpoints(package_dir=None):
    """
    Return {(METHOD, normalized path): ["Class.method", ...]} for the methods in backlog/*.py.
    """
    package_dir = package_dir or os.path.join(ROOT, "backlog")
    found = collections.defaultdict(list)
    for filename in sorted(glob.glob(os.path.join(package_dir, "*.py"))):
        with open(filename, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename)
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            functions = [n for n in cls.body if isinstance(n, ast.FunctionDef)]
            helpers = _uri_helpers(functions)
            for func in functions:
                name = "{}.{}".format(cls.name, func.name)
                for method, uri in _invoke_method_calls(func, helpers):
                    key = (method, normalize(uri))
                    if name not in found[key]:
                        found[key].append(name)
    return dict(found)


# ---------------------------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------------------------

def _group(path):
    if path.startswith("/api/v2/projects/") and "/git/" in path:
        return "Git"
    segment = path.split("/")[3]
    return GROUP_NAMES.get(segment, segment[:1].upper() + segment[1:])


def render(snapshot, implemented):
    endpoints = snapshot["endpoints"]
    documented = {(e["method"].upper(), normalize(e["path"])) for e in endpoints}
    groups = collections.OrderedDict()
    for e in sorted(endpoints, key=lambda e: (_group(e["path"]), e["path"], e["method"])):
        groups.setdefault(_group(e["path"]), []).append(e)

    def methods(e):
        return implemented.get((e["method"].upper(), normalize(e["path"])), [])

    covered = sum(1 for e in endpoints if methods(e))
    lines = [
        "# Backlog API coverage",
        "",
        "<!-- Generated by scripts/api_coverage.py. Do not edit by hand: run `python scripts/api_coverage.py generate`. -->",
        "",
        "Which [Backlog API v2]({}) endpoints python-backlog implements.".format(snapshot["index"]),
        "",
        "The endpoint list (`docs/api_endpoints.json`) follows the official API reference, whose index was last "
        "checked on {}. **{} of {} endpoints ({:.0%}) have a dedicated method.** Any other endpoint can still be "
        "called with `BacklogAPI.invoke_method()`.".format(snapshot["index_last_accessed"], covered, len(endpoints), covered / len(endpoints)),
        "",
    ]
    undocumented = sorted((k, v) for k, v in implemented.items() if k not in documented)
    if undocumented:
        lines += [
            "Methods that call endpoints which are not in the official API reference "
            "(they may have been removed; see the E2E tests in `tests/e2e/`):",
            "",
        ]
        for (method, path), names in undocumented:
            lines.append("- `{} {}`: {}".format(method, path, ", ".join("`{}()`".format(n) for n in names)))
        lines.append("")
    lines += ["| Group | Implemented |", "|---|---|"]
    for name, items in groups.items():
        lines.append("| [{}](#{}) | {} / {} |".format(
            name, name.lower().replace(" ", "-"), sum(1 for e in items if methods(e)), len(items)))
    for name, items in groups.items():
        lines += ["", "## " + name, "", "| Method | Path | API | Last accessed | python-backlog |", "|---|---|---|---|---|"]
        for e in items:
            names = methods(e)
            cell = ", ".join("`{}()`".format(n) for n in names) if names else "—"
            lines.append("| {} | `{}` | [{}]({}) | {} | {} |".format(
                e["method"], e["path"].replace("/api/v2/", "", 1), e["title"], e["url"], e["last_accessed"], cell))
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------------------------

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_REQUIRED = ("method", "path", "title", "url", "last_accessed")


def _load_snapshot():
    """
    Load docs/api_endpoints.json and validate it, since it is edited by hand.
    """
    with open(ENDPOINTS_JSON, encoding="utf-8") as f:
        snapshot = json.load(f)
    problems = []
    if not _DATE.match(str(snapshot.get("index_last_accessed", ""))):
        problems.append("index_last_accessed must be a YYYY-MM-DD date")
    seen = set()
    for i, e in enumerate(snapshot.get("endpoints", [])):
        missing = [k for k in _REQUIRED if not e.get(k)]
        if missing:
            problems.append("endpoints[{}] is missing {}".format(i, ", ".join(missing)))
            continue
        if e["method"] not in ("GET", "POST", "PUT", "PATCH", "DELETE"):
            problems.append("endpoints[{}]: invalid method {!r}".format(i, e["method"]))
        if not e["path"].startswith("/api/v2/"):
            problems.append("endpoints[{}]: path must start with /api/v2/".format(i))
        if not e["url"].startswith("https://developer.nulab.com/"):
            problems.append("endpoints[{}]: url must point to developer.nulab.com".format(i))
        if not _DATE.match(e["last_accessed"]):
            problems.append("endpoints[{}]: last_accessed must be a YYYY-MM-DD date".format(i))
        key = (e["method"], normalize(e["path"]))
        if key in seen:
            problems.append("endpoints[{}]: duplicate {} {}".format(i, e["method"], e["path"]))
        seen.add(key)
    if problems:
        raise SystemExit("docs/api_endpoints.json is invalid:\n  " + "\n  ".join(problems))
    return snapshot


def main(argv):
    command = argv[1] if len(argv) > 1 else "check"
    expected = render(_load_snapshot(), implemented_endpoints())
    if command == "generate":
        with open(COVERAGE_MD, "w", encoding="utf-8") as f:
            f.write(expected)
        print("Wrote {}".format(os.path.relpath(COVERAGE_MD, ROOT)))
        return 0
    if command == "check":
        actual = ""
        if os.path.exists(COVERAGE_MD):
            with open(COVERAGE_MD, encoding="utf-8") as f:
                actual = f.read()
        if actual == expected:
            print("docs/API_COVERAGE.md is up to date")
            return 0
        sys.stdout.writelines(difflib.unified_diff(
            actual.splitlines(True), expected.splitlines(True), "docs/API_COVERAGE.md (committed)", "docs/API_COVERAGE.md (expected)"))
        print("\n::error::docs/API_COVERAGE.md is out of date. Run: python scripts/api_coverage.py generate")
        return 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
