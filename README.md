# meta-audit

Know your automation maturity level -- and what to build next.

A [Claude Code](https://claude.ai/claude-code) skill that audits your AI coding tool setup against an L0-L5 maturity model, benchmarks you against the ecosystem's top power users, and outputs a focused action plan to close the biggest gaps.

## When to Use

- Monthly automation audit or after completing a major milestone
- You feel a productivity bottleneck but can't pinpoint where
- You want a data-driven answer to "what should I build next?"

## Features

- **L0-L5 maturity model** -- five-axis assessment across skills, hooks, headless, multi-agent, and meta-learning
- **5-axis radar** -- quantified scores with ecosystem comparison (coverage ratio, not guesswork)
- **External benchmarking** -- GitHub API queries against top repos (superpowers, gstack, anthropics/skills, etc.)
- **Friction-to-action mapping** -- extracts friction root causes from session data and maps them to concrete improvements
- **Deterministic data collection** -- `collect.sh` outputs JSON metrics, no LLM counting
- **`--quick` / `--verbose` modes** -- flexible depth control

## Usage

```
/meta-audit              # full audit (with external benchmarks)
/meta-audit --quick      # skip external benchmarks, local data only
/meta-audit --verbose    # output full friction detail + raw benchmark data
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
