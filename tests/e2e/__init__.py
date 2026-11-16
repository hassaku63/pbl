# coding: utf-8
"""
End-to-end tests against a real Backlog space.

They are skipped unless the following environment variables are set (see .github/workflows/e2e.yml):

- BACKLOG_E2E_SPACE: space key
- BACKLOG_E2E_API_KEY: API key
- BACKLOG_E2E_DOMAIN: "backlog.jp" (default), "backlog.com" or "backlogtool.com"
- BACKLOG_E2E_PROJECT_KEY: key of a project dedicated to these tests
- BACKLOG_E2E_WRITE: set to "1" to also run tests that create and delete data in that project
- BACKLOG_E2E_INTERVAL: minimum seconds between requests (default 1.0), to stay well below rate limits
- BACKLOG_E2E_ADMIN: set to "1" by scripts/e2e_local.py to run tier A tests (refused in CI)
- BACKLOG_E2E_USER_EMAIL: tier A only. Address used for the test user (it may receive a registration mail)

Guidelines: tests/e2e/README.md. Setup of the space and the GitHub environment: CONTRIBUTING.md.
"""
