# meta-audit

AI automation maturity audit plugin for Claude Code.

## Structure

- `meta-audit/SKILL.md` — Skill definition: L0-L5 model, 5-axis radar, pipeline, action template
- `meta-audit/sources.md` — External benchmark data sources and stats methodology
- `meta-audit/collect.sh` — Deterministic local data collector (outputs JSON)
- `meta-audit/test-collect.sh` — Smoke test for collect.sh
- `.claude-plugin/plugin.json` — Plugin manifest (single skill: meta-audit)

## Key Design Decisions

- `disable-auto-invoke: true` — this skill has side effects (writes audit-history/audit-cache), must be explicitly triggered
- Scoring uses `collect.sh` output, not LLM counting — deterministic and reproducible
- Benchmarks use coverage ratio (user / ecosystem max), not percentiles — sample size too small for P99
- L3+ maturity requires outcome evidence (friction reduction), not just config counts
- cc-navigator was moved to yuanbo-skills (separate repo) — this plugin is audit-only
