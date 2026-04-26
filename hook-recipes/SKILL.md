---
name: hook-recipes
description: >
  Use when meta-audit identifies missing hook coverage, or the user wants to add
  hooks but doesn't know what to write. Provides battle-tested hook templates for
  PostToolUse type-checking, PreToolUse guards, and project-level scaffolds.
  Triggers: "add a hook", "what hooks should I have", "fix my hook coverage",
  after meta-audit shows hook gaps.
---

# Hook Recipes

Curated hook templates for Claude Code. Each recipe is a tested `settings.json` entry ready to apply via `/update-config`.

## When to Use

- meta-audit flagged missing PostToolUse / project-level hooks
- You want to add a hook but don't know the matcher/command pattern
- Setting up a new project and want standard guardrails

## When NOT to Use

- Writing a custom domain-specific hook from scratch (just edit settings.json directly)
- Debugging an existing hook that's misfiring

## Workflow

1. **Diagnose** — Check which hooks are missing. If meta-audit was just run, use its output. Otherwise run `bash collect.sh` from the meta-audit directory and check `hooks.event_types_used` and `hooks.has_project_level`.

2. **Select** — Read `recipes.json` (in this skill's directory) to list available recipes. Present the user a table:
   ```
   | # | Recipe | Event | Matcher | What it does |
   ```
   Let the user pick by number or name.

3. **Adapt** — Before applying, check the user's stack:
   - TypeScript project? → use `tsc` recipe, not `pyright`
   - Python project? → use `pyright` or `ruff` recipe
   - Monorepo? → adjust paths in command
   - Already has similar hook? → warn about duplication

4. **Apply** — Use `/update-config` to write the hook entry into the correct settings file:
   - **Global hooks** → `~/.claude/settings.json`
   - **Project hooks** → `.claude/settings.json` in the project root
   Tell the user which file will be modified and get confirmation.

5. **Verify** — Re-run `bash collect.sh` and confirm the expected field changed (e.g., `hooks.total_entries` +1, `hooks.event_types_used` +1).

## Recipe Format (in recipes.json)

Each recipe has:
- `id` — unique identifier
- `name` — human-readable name
- `event` — hook event type (PreToolUse / PostToolUse / Stop / Notification)
- `matcher` — tool matcher pattern
- `command` — shell command to execute
- `description` — what it catches and why
- `stack` — which tech stacks this applies to (e.g., ["typescript"], ["python"], ["any"])
- `level_impact` — which meta-audit field it moves (for verification)

## Constraints

- **Never auto-apply** — always show the user what will be written and to which file
- **One recipe at a time** — apply, verify, then next. Don't batch-write multiple hooks
- **Respect existing hooks** — check for duplicates before adding
- **Shell script hooks go in `~/.claude/hooks/`** — for non-trivial commands, create a script file rather than inlining a long command string
