# meta-audit

Know your automation maturity level -- and what to build next.

An Agent Skill that audits workflow maturity and context-engineering debt, then
maps observed friction to the smallest effective interface, reference, test, or
automation change.

## When to Use

- Monthly automation audit or after completing a major milestone
- You feel a productivity bottleneck but can't pinpoint where
- You want a data-driven answer to "what should I build next?"
- Skills, instruction files, or hooks have grown and may now conflict

## Features

- **L0-L5 maturity model** -- five-axis assessment across skills, hooks, headless, multi-agent, and meta-learning
- **5-axis radar** -- quantified scores with ecosystem comparison (coverage ratio, not guesswork)
- **External benchmarking** -- GitHub API queries against top repos (superpowers, gstack, anthropics/skills, etc.)
- **Friction-to-action mapping** -- extracts friction root causes from session data and maps them to concrete improvements
- **Deterministic data collection** -- `collect.sh` outputs JSON metrics, no LLM counting
- **`--quick` / `--verbose` modes** -- flexible depth control
- **Hook Recipes** -- curated hook templates that close audit gaps in one step (see below)
- **Context audit** -- detects overlong entrypoints, host-specific portable
  bodies, imperative density, and injected hook surface

## Usage

```
/meta-audit              # full audit (with external benchmarks)
/meta-audit --quick      # skip external benchmarks, local data only
/meta-audit --verbose    # output full friction detail + raw benchmark data
python3 scripts/context_audit.py --check /path/to/repo
python3 scripts/context_audit.py --json /path/to/repo
```

## Output Example

```markdown
# Meta Audit — 2026-04-20

## Level: L3 Hooked (previous L2, +1)

## Radar
| Axis            | Score | Ecosystem P50 | Gap             |
|-----------------|-------|---------------|-----------------|
| Skill Breadth   | 83    | 15            | +68 (top 1%)    |
| Hook Depth      | 6/19  | 3/19          | +3              |
| Headless        | 1     | 0             | +1              |
| Multi-agent     | 6     | 2             | +4              |
| Meta-learning   | yes   | no            | --              |

## Top-3 Friction → Top-3 Action
1. buggy_code (94x) → PostToolUse pyright/ruff hook
2. wrong_approach (78x) → PreToolUse constraint guards
3. tool_failure (23x) → Environment preflight skill

## Compared to Last Audit
- Added: 4 hooks, reflection pipeline
- Improved: Hook depth 0→7
- Regressed: --
```

## Hook Recipes (sub-skill)

When an audit flags missing hook coverage, use `/hook-recipes` to apply tested templates instead of writing hooks from scratch.

10 built-in recipes covering:

| Category | Recipes | Audit Gap Closed |
|----------|---------|-----------------|
| PostToolUse type-check | tsc, pyright | `event_types_used` 3→4 |
| PostToolUse lint | ruff, eslint | `total_entries` +1 |
| PostToolUse format | prettier, ruff format | `total_entries` +1 |
| PreToolUse guard | large-file, test-before-commit | `total_entries` +1 |
| Project-level template | python-guard, ml-experiment-guard | `has_project_level` → true |

Each recipe includes matcher, command, stack compatibility, and the exact `collect.sh` field it moves -- so you can verify the fix immediately.

## Install

### Via skills.sh (recommended)

```bash
npx skills add freemty/meta-audit
```

Works with Claude Code, Cursor, Codex, Windsurf, and [15+ other agents](https://skills.sh).

### Manual

```bash
git clone https://github.com/freemty/meta-audit.git ~/.claude/skills/meta-audit
```

## License

MIT
