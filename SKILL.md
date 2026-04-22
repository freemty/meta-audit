---
name: meta-audit
disable-auto-invoke: true
description: >
  Use when the user explicitly requests an automation maturity audit via /meta-audit.
  Assesses AI coding tool automation maturity, identifies gaps vs ecosystem benchmarks,
  and recommends what skills/hooks/workflows to build next.
  Triggers: /meta-audit, "audit my setup", "how automated am I",
  "what should I build next", "automation maturity check".
---

# Meta Audit

Data-driven automation maturity assessment: benchmark against the ecosystem, produce evidence-backed positioning + concrete action items.

## When to Use

- Monthly recurring audit / after completing a major milestone
- Want to know "what should I build next?"
- Feeling an efficiency bottleneck but unsure where it is

## When NOT to Use

- Day-to-day code review / single session retrospective / pure project progress check

## Pipeline

1. **Data Collection** -- Run `bash collect.sh` (in this skill's directory) to get deterministic JSON output. Includes skill/hook/plugin/agent counts, headless detection, 30-day commit velocity. Do not count manually or guess.
2. **External Benchmarks** -- Use `gh api` to query core sources (superpowers-marketplace, anthropics/skills, everything-claude-code, etc.) and extract skill/hook/plugin counts. Cache for 7 days. See `sources.md` for details. If unavailable, skip and annotate.
3. **Analysis & Positioning** -- L0-L5 scoring + 5-axis radar + friction root cause mapping
4. **Report Output** -- Concise Markdown report + archive to `~/.claude/audit-history/{YYYY-MM-DD}.md`

## Maturity Model (L0-L5)

Quantity is a necessary condition, not a sufficient one. L3+ determination must combine outcome metrics (friction reduction, commit velocity increase, reduced manual intervention). Stacking configuration counts alone does not warrant a level upgrade.

| Level | Definition | Criteria |
|-------|-----------|----------|
| L0 Vanilla | Only uses CLAUDE.md | skills=0, hooks=0 |
| L1 Configured | Has rules + a few skills | skills<15, hooks<=1 |
| L2 Skilled | Many skills, manually triggered | skills>=15, hooks<3 |
| L3 Hooked | Skills + hooks + agents, observable friction reduction | hooks>=3, project-level hooks, wrong_approach friction decreased vs L2 |
| L4 Orchestrated | Headless/cron + multi-agent, low manual intervention rate | Has persistent cron or GitHub Actions, human intervention <30% of sessions |
| L5 Autonomous | Self-healing + meta-learning, continuous improvement | Has reflection pipeline, monthly friction trend declining |

## Radar Axes (5 axes)

1. **Skill Breadth** -- skill count / ecosystem max
2. **Hook Depth** -- hook entries / available event types (4 types x 19 lifecycle events)
3. **Headless Degree** -- cron + CI/CD automation
4. **Multi-agent** -- agent definition count + parallel dispatch
5. **Meta-learning** -- existence of reflection/self-improvement loop

## Friction-to-Action Mapping

| Friction Type | Recommended Improvement |
|--------------|------------------------|
| wrong_approach high | PreToolUse guard hooks / CLAUDE.md constraints |
| buggy_code high | PostToolUse type-check hooks |
| tool_failure high | Environment preflight skills |

## Report Structure

```
# Meta Audit -- {date}
## Level: L{N} (vs previous L{M})
## Radar: 5-axis table (score / ecosystem P50 / gap)
## Top-3 Friction → Top-3 Action
## Compared to Last Audit (added / improved / regressed)
```

## Execution Constraints

- **Do not auto-execute improvements** -- output recommendations only, execution requires human confirmation
- **Batch-parse facets** -- use Python for processing, do not Read files one by one
- **Parallelize external queries** -- spawn GitHub API calls with parallel Agents (use `gh api` or unauthenticated REST, mind the 60 req/h limit)
- **`--verbose`** -- output full friction detail + raw benchmark data
- **`--quick`** -- skip external benchmarks, use local data only

## Action Template

Each Top-3 action item must include:
1. **What** -- one-sentence description of the specific change
2. **How** -- directly executable command or skill invocation
3. **Verify** -- how to confirm completion (re-run `collect.sh` and compare which field changed)

Example:
```
Action 1: Add PostToolUse type-check hook
  What: Add a pyright check to hooks.PostToolUse in ~/.claude/settings.json
  How: /update-config
  Verify: collect.sh → hooks.total_entries +1, hooks.event_types_used includes PostToolUse
```

## Common Mistakes

| Mistake | Correct Approach |
|---------|-----------------|
| Compare against "typical user" with no data source | Cite specific repo + star count |
| Equate skill count with maturity | L2→L3 requires hooks + friction reduction, not just more skills |
| Too many recommendations (10+ action items) | Cap at Top-3; focus enables execution |
| Benchmark data outdated | 7-day TTL cache; refetch when expired |
| Action items without execution path | Every action must have a command/skill + verification method |
