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
"""
