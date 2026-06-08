Purpose

This file gives Copilot sessions repository-specific instructions so suggestions and code edits align with the project's structure and assessment requirements.

Build / test / lint (what exists and how to run)

- CI workflow (.github/workflows/github-actions.yml) runs:
  - pip install -r requirements.txt
  - bash ./run.sh
- Locally (recommended):
  - python -m venv venv
  - venv\Scripts\activate
  - pip install -r requirements.txt
  - bash run.sh
- Tests: no test framework or tests were found. If pytest is added, run a single test with:
  - python -m pytest path/to/module.py::test_name
- Lint: no linter config found. If adding flake8/ruff/black, use their standard CLI (e.g., ruff check ., black --check .).

High-level architecture (big picture)

- This repository appears to be an assessment/submission template rather than a deployed application. Key artifacts:
  - decision_log.md — assessment decision log the candidate must author
  - prompt_chat_history.md — transcript + share-link record for AI assistant usage
  - litellm_config.yaml / settings.json / .env — local LLM and environment configuration (API keys and endpoints)
  - .github/workflows/github-actions.yml — CI that expects requirements.txt and run.sh
- There is not a recognizable src/ or package layout (no tests or library modules detected). Some users created a Python virtualenv inside the repo (venv) — treat as local-only.

Key conventions and repo-specific notes

- Assessment files are canonical: decision_log.md and prompt_chat_history.md must be filled by the candidate according to their instructions. Do not auto-edit these files except for formatting or redaction of secrets (never add content on behalf of the candidate).
- Secrets: API keys and tokens are present in local config files in this copy. Do NOT commit real secrets to the repository or paste them into PRs. Prefer using environment variables or GitHub Secrets. When suggesting edits, remind users to move secrets to secure storage.
- CI expectations: The workflow expects a requirements.txt and a run.sh at repo root. If absent, create those artifacts intentionally; do not assume their content.
- Virtualenv: A local venv exists in some copies. Copilot should not suggest committing venv contents or editing files inside venv. Add or keep a top-level .gitignore entry for venv/.
- Test and lint patterns: None exist now. When adding tests, prefer a tests/ directory and use pytest conventions. For single-test execution use pytest path::test_name.

AI assistant / other tool configs

- No dedicated AI-assistant rule files were found (CLAUDE.md, AGENTS.md, .cursorrules, .windsurfrules, CONVENTIONS.md, etc.). If you add assistant-specific rules, place them at repo root or in .github and reference them in this file.

If you edit repository structure

- Keep assessment artifacts (decision_log.md, prompt_chat_history.md) intact and do not rewrite the candidate's answers.
- If adding a setup or CI artifact (requirements.txt, run.sh), document its purpose in this file and ensure it does not contain secrets.

Questions after this change

Would you like this file adjusted (more detail about preferred linters, a recommended test runner, or adding a simple example requirements.txt/run.sh)?
