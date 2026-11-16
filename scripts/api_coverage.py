#!/usr/bin/env python3
# coding: utf-8
"""
Maintain docs/API_COVERAGE.md: which Backlog API endpoints python-backlog implements.

The list of endpoints is docs/api_endpoints.json. It is maintained by hand, or by an AI agent that reads
the official API reference (see .claude/skills/api-change/SKILL.md): this script never downloads or parses
the documentation site, so it does not break when the site changes.
Implemented endpoints are found by statically analyzing backlog/*.py: every call to invoke_method()
with a literal HTTP method and a resolvable URI counts.

The "removed" list in docs/api_endpoints.json records endpoints that Backlog removed. "check" fails when a
method that is not deprecated calls one of them. A method is deprecated when its docstring contains
".. deprecated::" or it emits a DeprecationWarning (directly or through a helper whose name contains "deprecat"
or "warn").

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


def _is_deprecated(func):
    """
    Whether a method is marked as deprecated: ".. deprecated::" in its docstring, a warnings.warn() call
    with DeprecationWarning, or a call to a helper whose name mentions deprecation or warnings.
    """
    if ".. deprecated::" in (ast.get_docstring(func) or ""):
        return True
    for node in ast.walk(func):
        if not isinstance(node, ast.Call):
            continue
        name = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
        if name == "warn" and any(isinstance(a, ast.Name) and a.id == "DeprecationWarning" for a in ast.walk(node)):
            return True
        if name != "warn" and ("deprecat" in name.lower() or name.lower().startswith("_warn")):
            return True
    return False


def deprecated_methods(package_dir=None):
    """
    Return the set of "Class.method" names in backlog/*.py that are marked as deprecated.
    """
    package_dir = package_dir or os.path.join(ROOT, "backlog")
    found = set()
    for filename in sorted(glob.glob(os.path.join(package_dir, "*.py"))):
        with open(filename, encoding="utf-8") as f:
            tree = ast.parse(f.read(), filename)
        for cls in (n for n in tree.body if isinstance(n, ast.ClassDef)):
            for func in (n for n in cls.body if isinstance(n, ast.FunctionDef)):
                if _is_deprecated(func):
                    found.add("{}.{}".format(cls.name, func.name))
    return found


def removed_endpoint_violations(snapshot, implemented, deprecated):
    """
    Return ["METHOD path: Class.method", ...] for methods that call a removed endpoint and are not deprecated.
    """
    problems = []
    for e in snapshot.get("removed", []):
        for name in implemented.get((e["method"].upper(), normalize(e["path"])), []):
            if name not in deprecated:
                problems.append("{} {}: {}".format(e["method"], e["path"], name))
    return problems


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


def _removed_when(e):
    if not e.get("removed_in"):
        return "Removed from the reference (confirmed {})".format(e["confirmed_on"])
    when = "{} ({})".format(e["removed_in"], e["removed_on"]) if e.get("removed_on") else e["removed_in"]
    return "[{}]({})".format(when, e["changelog"]) if e.get("changelog") else when


def _render_removed(removed, implemented, deprecated):
    if not removed:
        return []
    lines = [
        "",
        "## Removed endpoints",
        "",
        "Endpoints that Backlog removed from the API. Methods that still call them are deprecated "
        "(`scripts/api_coverage.py check` fails otherwise).",
        "",
        "| Method | Path | API | Removed | Replacement | python-backlog |",
        "|---|---|---|---|---|---|",
    ]
    for e in sorted(removed, key=lambda e: (e["path"], e["method"])):
        when = _removed_when(e)
        title = "[{}]({})".format(e["title"], e["announcement"]) if e.get("announcement") else e["title"]
        names = implemented.get((e["method"].upper(), normalize(e["path"])), [])
        cell = ", ".join("`{}()`{}".format(n, " (deprecated)" if n in deprecated else "") for n in names) if names else "—"
        replacement = "`{}`".format(e["replacement"].replace("/api/v2/", "", 1)) if e.get("replacement") else "—"
        lines.append("| {} | `{}` | {} | {} | {} | {} |".format(
            e["method"], e["path"].replace("/api/v2/", "", 1), title, when, replacement, cell))
    notes = [e for e in removed if e.get("note")]
    if notes:
        lines.append("")
        for note in sorted({e["note"] for e in notes}):
            titles = ", ".join(e["title"] for e in notes if e["note"] == note)
            lines.append("- {}: {}".format(titles, note))
    return lines


def render(snapshot, implemented, deprecated=frozenset()):
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
    removed = {(e["method"].upper(), normalize(e["path"])) for e in snapshot.get("removed", [])}
    undocumented = sorted((k, v) for k, v in implemented.items() if k not in documented and k not in removed)
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
    lines += _render_removed(snapshot.get("removed", []), implemented, deprecated)
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------------------------

_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_REQUIRED = ("method", "path", "title", "url", "last_accessed")


def _validate_removed_formats(i, e):
    problems = []
    for k in ("removed_on", "confirmed_on"):
        if e.get(k) and not _DATE.match(e[k]):
            problems.append("removed[{}]: {} must be a YYYY-MM-DD date".format(i, k))
    for k in ("announcement", "changelog"):
        if e.get(k) and not e[k].startswith("https://"):
            problems.append("removed[{}]: {} must be an https URL".format(i, k))
    return problems


def _validate_removed(removed, seen):
    """
    Validate the "removed" entries; seen holds the (method, path) keys of the current endpoints.
    """
    problems = []
    for i, e in enumerate(removed):
        missing = [k for k in ("method", "path", "title", "confirmed_on") if not e.get(k)]
        if missing:
            problems.append("removed[{}] is missing {}".format(i, ", ".join(missing)))
            continue
        if not e.get("removed_in") and not e.get("note"):
            problems.append("removed[{}]: give removed_in (changelog version) or a note".format(i))
        if e["method"] not in ("GET", "POST", "PUT", "PATCH", "DELETE"):
            problems.append("removed[{}]: invalid method {!r}".format(i, e["method"]))
        if not e["path"].startswith("/api/v2/"):
            problems.append("removed[{}]: path must start with /api/v2/".format(i))
        problems += _validate_removed_formats(i, e)
        key = (e["method"], normalize(e["path"]))
        if key in seen:
            problems.append("removed[{}]: {} {} is also listed as a current endpoint or twice".format(i, e["method"], e["path"]))
        seen.add(key)
    return problems


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
    problems += _validate_removed(snapshot.get("removed", []), seen)
    if problems:
        raise SystemExit("docs/api_endpoints.json is invalid:\n  " + "\n  ".join(problems))
    return snapshot


def main(argv):
    command = argv[1] if len(argv) > 1 else "check"
    snapshot, implemented, deprecated = _load_snapshot(), implemented_endpoints(), deprecated_methods()
    expected = render(snapshot, implemented, deprecated)
    violations = removed_endpoint_violations(snapshot, implemented, deprecated)
    for violation in violations:
        print("::error::{} calls an endpoint that Backlog removed. Deprecate the method "
              "(see .claude/skills/api-change/SKILL.md) or stop calling the endpoint.".format(violation))
    if command == "generate":
        with open(COVERAGE_MD, "w", encoding="utf-8") as f:
            f.write(expected)
        print("Wrote {}".format(os.path.relpath(COVERAGE_MD, ROOT)))
        return 1 if violations else 0
    if command == "check":
        if violations:
            return 1
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
