#!/usr/bin/env python3
# coding: utf-8
"""
Maintain docs/API_COVERAGE.md: which Backlog API endpoints python-backlog implements.

The list of endpoints comes from a snapshot of the official API documentation (docs/api_endpoints.json).
Implemented endpoints are found by statically analyzing backlog/*.py: every call to invoke_method()
with a literal HTTP method and a resolvable URI counts.

Usage:
    python scripts/api_coverage.py generate   # rewrite docs/API_COVERAGE.md
    python scripts/api_coverage.py check      # exit 1 if docs/API_COVERAGE.md is out of date (used in CI)
    python scripts/api_coverage.py refresh    # re-download the endpoint list from the official docs (network)

Only the standard library is used.
"""

import ast
import collections
import datetime
import difflib
import glob
import html
import json
import os
import re
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENDPOINTS_JSON = os.path.join(ROOT, "docs", "api_endpoints.json")
COVERAGE_MD = os.path.join(ROOT, "docs", "API_COVERAGE.md")
DOCS_BASE = "https://developer.nulab.com"
DOCS_INDEX = DOCS_BASE + "/docs/backlog/"

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
        "Which [Backlog API v2]({}) endpoints python-backlog implements.".format(DOCS_INDEX),
        "",
        "The endpoint list is a snapshot of the official API reference taken on {} "
        "(`docs/api_endpoints.json`, refresh it with `python scripts/api_coverage.py refresh`). "
        "**{} of {} endpoints ({:.0%}) have a dedicated method.** Any other endpoint can still be called with "
        "`BacklogAPI.invoke_method()`.".format(snapshot["checked"], covered, len(endpoints), covered / len(endpoints)),
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
        lines += ["", "## " + name, "", "| Method | Path | API | python-backlog |", "|---|---|---|---|"]
        for e in items:
            names = methods(e)
            cell = ", ".join("`{}()`".format(n) for n in names) if names else "—"
            lines.append("| {} | `{}` | [{}]({}/docs/backlog/api/2/{}/) | {} |".format(
                e["method"], e["path"].replace("/api/v2/", "", 1), e["title"], DOCS_BASE, e["slug"], cell))
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------------------------
# Refreshing the snapshot from the official documentation
# ---------------------------------------------------------------------------------------------

def _fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "python-backlog-api-coverage"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def _page_text(page):
    page = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", page, flags=re.S)
    return [x.strip() for x in html.unescape(re.sub(r"<[^>]+>", "\n", page)).split("\n") if x.strip()]


def refresh():
    index = _fetch(DOCS_INDEX)
    slugs = sorted(set(re.findall(r'href="/docs/backlog/api/2/([a-z0-9-]+)/?"', index)))
    if not slugs:
        raise SystemExit("No API pages found in {}; the page layout may have changed".format(DOCS_INDEX))
    endpoints = []
    for slug in slugs:
        page = _fetch("{}/docs/backlog/api/2/{}/".format(DOCS_BASE, slug))
        lines = _page_text(page)
        method = next((lines[i + 1] for i, x in enumerate(lines[:-1]) if x == "Method"), "")
        path = next((lines[i + 1] for i, x in enumerate(lines[:-1]) if x == "URL"), "")
        match = re.search(r"<title>(.*?)</title>", page, re.S)
        title = html.unescape(match.group(1)).split("|")[0].strip() if match else slug
        if not method or not path.startswith("/api/v2/"):
            raise SystemExit("Could not parse method/URL of {}".format(slug))
        endpoints.append({"method": method, "path": path, "title": title, "slug": slug})
        time.sleep(0.2)
    endpoints.sort(key=lambda e: (e["path"], e["method"]))
    snapshot = {"source": DOCS_INDEX, "checked": datetime.date.today().isoformat(), "endpoints": endpoints}
    with open(ENDPOINTS_JSON, "w", encoding="utf-8") as f:
        f.write(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n")
    print("Saved {} endpoints to {}".format(len(endpoints), os.path.relpath(ENDPOINTS_JSON, ROOT)))


# ---------------------------------------------------------------------------------------------

def _load_snapshot():
    with open(ENDPOINTS_JSON, encoding="utf-8") as f:
        return json.load(f)


def main(argv):
    command = argv[1] if len(argv) > 1 else "check"
    if command == "refresh":
        refresh()
        command = "generate"
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
