# Selection Rubric

Use this rubric when a prompt requires skill discovery.

## Inputs

Extract:

- explicit skill mentions (`$skill`, plugin names, app links)
- requested deliverables
- target systems (Joplin, GitHub, Calendar, browser, files, codebase)
- file types and frameworks
- freshness or external-data requirements
- safety constraints and irreversible operations

## Match Levels

- Required: explicitly named or impossible to complete without it.
- Strong: description directly matches deliverable or target system.
- Conditional: needed only after inspection reveals matching files, frameworks, or APIs.
- Skip: merely adjacent, broad, or duplicative.

## Tie Breakers

- Prefer local skill over generic reasoning when it contains tool workflow.
- Prefer app connector over shell when the connector exposes the needed operation.
- Prefer fewer skills when one skill covers the workflow end to end.
- Prefer a create/setup companion skill only for first-time scaffolds.

## Sequence Template

1. Discovery: inventory skills and target project state.
2. Context: read selected skill bodies and required references.
3. Implementation: create/edit artifacts.
4. Validation: run skill validator, tests, or smoke checks.
5. Persistence: update Joplin wiki if requested.
6. Publishing: commit, create repo/PR, or report exact blocker.
