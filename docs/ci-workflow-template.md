# CI Workflow Template

The Zapier GitHub MCP integration doesn't have `workflow` scope, so this CI yaml
couldn't be pushed directly to `.github/workflows/ci.yml`. Move it manually:

```bash
mkdir -p .github/workflows
mv docs/ci-workflow-template.yml .github/workflows/ci.yml
git add .github/workflows/ci.yml
git commit -m "ci: enable GitHub Actions"
git push
```

## Contents (paste into `.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [main, dev]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.production.txt
      - name: Run tests
        run: pytest tests/ -v
        env:
          META_VERIFY_TOKEN: RecruitinSecureToken2026!
```

This workflow runs pytest on every push to main/dev and on PRs to main.
