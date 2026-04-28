# Prompt Skill Orchestrator

Codex skill for turning a complex user prompt into a small, ordered set of required skills, plugins, and app tools.

Use it when a prompt asks Codex to:

- find required skills before doing the work
- combine explicit skills such as `caveman` and `joplin-llm-wiki`
- decide which plugin or app connector should handle part of a task
- run work in a clear sequence: discover, read context, implement, validate, persist, publish
- save durable outcomes into a Joplin-based LLM Wiki

## What It Does

The skill teaches Codex to parse a prompt into deliverables, target systems, constraints, and explicit skill mentions. It then selects the smallest useful set of skills and sequences them so work happens in the right order.

For example:

1. Create or edit files first.
2. Validate the result.
3. Ingest durable knowledge into Joplin LLM Wiki if requested.
4. Publish to GitHub only after local validation and secret scanning.

## Contents

- `SKILL.md` - runtime instructions loaded by Codex when the skill triggers.
- `references/selection-rubric.md` - rubric for deciding which skills are required, optional, or irrelevant.
- `scripts/list_available_skills.py` - local helper that scans Codex skill directories and prints matching skill metadata as JSON.
- `agents/openai.yaml` - UI metadata for Codex skill listings.

## Install

Copy or clone this folder into your Codex skills directory:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
git clone https://github.com/Nehoko/prompt-skill-orchestrator.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/prompt-skill-orchestrator"
```

Restart Codex if needed so it reloads local skills.

## Usage

Invoke it explicitly:

```text
Use $prompt-skill-orchestrator to find the required skills for this prompt, execute the task, validate the result, and ingest durable notes into Joplin LLM Wiki.
```

Example prompt:

```text
Use $prompt-skill-orchestrator with $caveman:caveman and $joplin-curl:joplin-llm-wiki. Create a new skill, find any extra skills needed, validate it, ingest the result into Joplin LLM Wiki, and publish it to GitHub.
```

## Skill Discovery Helper

List all discovered skills:

```bash
python3 scripts/list_available_skills.py
```

Filter by keyword:

```bash
python3 scripts/list_available_skills.py --query joplin
python3 scripts/list_available_skills.py --query github
```

Add an extra skill root:

```bash
python3 scripts/list_available_skills.py --root /path/to/skills --query calendar
```

The script reads `SKILL.md` frontmatter and returns JSON objects with `name`, `description`, and `path`.

## Environment Variables And Secrets

This repository should not contain private tokens, local API config, `.env` files, or machine-specific values.

Use environment variables for sensitive or local setup values:

- `CODEX_HOME` - optional Codex home directory override.
- `JOPLIN_TOKEN` - Joplin API token, if your local workflow needs one.
- `JOPLIN_PORT` - Joplin clipper port, if your local workflow needs one.
- `GITHUB_TOKEN` - GitHub token for non-interactive GitHub CLI/API workflows.

Before publishing changes, scan tracked files for secrets and replace setup-specific values with environment variable names.

## Validate

Run the Codex skill validator from your local `skill-creator` skill:

```bash
python3 "$CODEX_HOME/skills/.system/skill-creator/scripts/quick_validate.py" .
```

If `PyYAML` is missing, install it into your active Python environment or provide it through `PYTHONPATH`.

Smoke test the helper:

```bash
python3 scripts/list_available_skills.py --query caveman
```

## License

No license file is included yet. Treat usage rights as unspecified until a license is added.
