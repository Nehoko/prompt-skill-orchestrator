---
name: prompt-skill-orchestrator
description: "Select and sequence Codex skills, plugins, and app tools from a user prompt, especially when a task asks to combine caveman compression with Joplin LLM Wiki ingestion or to discover required skills before execution. Use when prompts mention finding required skills, routing work to skills, orchestrating multiple skills, ingesting outcomes into Joplin LLM Wiki, or keeping responses token-compact while coordinating tool-backed work."
---

# Prompt Skill Orchestrator

Route a prompt into the smallest useful set of Codex skills and tools, then run task work with compressed communication and durable Joplin wiki capture when requested.

## Workflow

1. Parse the prompt into deliverables, required systems, constraints, and explicit skill mentions.
2. Run `scripts/list_available_skills.py` when local skill inventory is needed. Use its JSON output to identify candidate skills by name, path, and description.
3. Select only skills needed to complete the task. Prefer explicit user mentions first, then high-confidence description matches, then app/plugin tools implied by the task.
4. Read each selected `SKILL.md` only as needed. If a selected skill points to references or scripts, load only the relevant files.
5. Sequence skills by dependency:
   - creation or editing skills before publishing or ingestion
   - Joplin LLM Wiki schema/config checks before Joplin writes
   - GitHub/repository steps after local files validate
6. Use caveman style for user-facing progress and summaries when requested, but write code, commits, PR bodies, and wiki notes in normal clear prose unless the target schema asks for compressed text.
7. Persist durable results into Joplin LLM Wiki when requested: raw source first if useful, synthesized wiki page next, index/log last.
8. Verify local artifacts with the relevant validator or smoke test before publishing.

## Skill Selection

Use `references/selection-rubric.md` for ambiguous prompts or when many candidate skills match.

Selection rules:

- Explicit `$skill` mentions are authoritative unless impossible.
- Prefer one specialist skill over several broad skills.
- Add companion skills only when their workflow is directly needed.
- Do not load a skill just because it is adjacent to the task.
- If a plugin/app is named, prefer that plugin's skill or MCP/app tools over generic shell work.
- For GitHub work, inspect connector capability first; use `gh` only for missing repository operations.

## Joplin Ingestion

When ingesting this orchestration result into Joplin LLM Wiki:

- Verify Joplin helper config and ping first.
- Inspect notebooks and read `LLM Wiki/Ops/Schema` if it exists.
- Store raw prompt/source material under `Raw Sources` when it has future value.
- Store distilled process knowledge under `Wiki`.
- Update `index` and append a dated `log` entry.
- Use tags sparingly for `skill`, `codex`, `workflow`, or project-specific retrieval.

## GitHub Publishing

When asked to create a repository:

- Initialize a local git repository in the skill folder if needed.
- Commit only files belonging to the skill.
- Scan tracked files for secrets, tokens, private hostnames, absolute user paths, and local config before publishing.
- Redact sensitive values. Replace setup-specific values with environment variable names such as `JOPLIN_TOKEN`, `JOPLIN_PORT`, `GITHUB_TOKEN`, or project-specific equivalents.
- Do not commit `.env`, local config files, API tokens, personal access tokens, or generated request payloads containing sensitive data.
- Prefer GitHub connector tools for existing repositories.
- If repository creation is not available through the connector, use `gh repo create` with user approval when required by sandbox/network policy.

## Output

Report:

- chosen skills and why
- files created or changed
- validation commands and results
- Joplin note titles/ids changed
- GitHub repository URL or blocker
