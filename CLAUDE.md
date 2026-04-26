# meta-audit

AI automation maturity audit plugin for Claude Code.

## Structure

- `SKILL.md` — Skill definition: L0-L5 model, 5-axis radar, pipeline, action template
- `sources.md` — External benchmark data sources and stats methodology
- `collect.sh` — Deterministic local data collector (outputs JSON)
- `test-collect.sh` — Smoke test for collect.sh
- `hook-recipes/SKILL.md` — Sub-skill: curated hook templates for closing audit gaps
- `hook-recipes/recipes.json` — Structured hook template data (10 recipes, PostToolUse/PreToolUse/project-level)
- `.claude-plugin/plugin.json` — Plugin manifest (skills: meta-audit, hook-recipes)

## Key Design Decisions

- `disable-auto-invoke: true` — this skill has side effects (writes audit-history/audit-cache), must be explicitly triggered
- Scoring uses `collect.sh` output, not LLM counting — deterministic and reproducible
- Benchmarks use coverage ratio (user / ecosystem max), not percentiles — sample size too small for P99
- L3+ maturity requires outcome evidence (friction reduction), not just config counts
- hook-recipes is a sub-skill that closes the "audit → action" gap — meta-audit identifies missing hooks, hook-recipes provides tested templates to apply them
- Recipes are data-driven (recipes.json), not hardcoded in SKILL.md — easy to add new recipes without editing skill logic
- cc-navigator was moved to yuanbo-skills (separate repo) — this plugin is audit-only
