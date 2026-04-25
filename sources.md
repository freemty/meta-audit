# Meta Audit -- Benchmark Sources

Data sources for Phase 2 external benchmarking. Queried via `gh api`, cached for 7 days at `~/.claude/audit-cache/benchmark.json`.

## Core Sources (queried in default mode)

| Source | What to Query | Signal | Query Method |
|--------|--------------|--------|-------------|
| `obra/superpowers-marketplace` | Plugin list + skill count per plugin | Benchmark for P99 power user skills/workflows | `gh api repos/obra/superpowers-marketplace/git/trees/main?recursive=1` |
| `anthropics/skills` | Directory structure + spec version | Official skill standard + reference skill count | `gh api repos/anthropics/skills/git/trees/main?recursive=1` |
| `anthropics/claude-plugins-official` | Plugin count in marketplace directory | Official ecosystem scale | `gh api repos/anthropics/claude-plugins-official/contents/plugins` |
| Local `~/.claude/plugins/installed_plugins.json` | Installed plugin count + versions | User's own plugin coverage | Read file directly |
| `affaan-m/everything-claude-code` | skills/ directory + stars | Community best practices collection scale | `gh api repos/affaan-m/everything-claude-code` |
| `garrytan/gstack` | Skill count + agent count + stars + has_headless + has_multi_agent | Largest power user framework (47 skills, headless browser, multi-host) | `gh api repos/garrytan/gstack/git/trees/main?recursive=1` |

## Supplementary Sources (added in --verbose mode)

| Source | What to Query | Signal |
|--------|--------------|--------|
| `ComposioHQ/awesome-claude-skills` | Star count + README skill list | Community growth rate / popularity |
| Showcase configs (ChrisWiles, etc.) | hooks/skills in settings.json | Typical power user configuration benchmarks |
| `openai/codex` | Feature list + stars | Competitor capability alignment |
| `nicepkg/claude-code-skill` | Total indexed skill count | Ecosystem breadth (long tail) |
| `forrestchang/andrej-karpathy-skills` | Star count + skill structure + CLAUDE.md guidelines | Community behavioral guidelines plugin benchmark, Karpathy coding principles coverage |
| `jiahao-shao1/sjh-skills` | skill count + workflow-stage coverage | Peer researcher skill collection (replica) — same-scale comparator to yuanbo-skills |

## Research Harness Benchmarks

衡量的不是 skill 覆盖率，而是 research session 生命周期 / harness 成熟度。详见 `docs/plugins/evolve-bench.md`。

| Source | What to Query | Signal |
|--------|--------------|--------|
| `Sisyphe-lee/evolve_bench` | harness/ protocols + research/ spec + .claude/skills/ (report/review/direction/orchestrate) | Reference harness for AI-driven research projects — two-stage closure, file-is-state, programmatic validators |

## Extracted Fields

Each source is normalized after extraction to:

```json
{
  "source": "obra/superpowers-marketplace",
  "stars": 160000,
  "skill_count": 42,
  "hook_count": 6,
  "plugin_count": 8,
  "has_headless": true,
  "has_multi_agent": true,
  "fetched_at": "2026-04-20T12:00:00Z"
}
```

## Benchmark Calculation

Core sources are split into two categories, never mixed:
- **Framework sources** (superpowers, anthropics/skills, everything-claude-code, gstack) -- represent "the ceiling if you fully adopt that framework"
- **User sources** (local installed_plugins) -- represent "the user's actual coverage"

Benchmark metrics:
- **Ecosystem ceiling**: maximum across framework sources (represents a single framework's full capability)
- **User coverage**: user source / ecosystem ceiling x 100%
- **Ecosystem mean**: framework sources with highest and lowest removed, then averaged (only meaningful with 3+ sources)

"P99" is not used -- sample size (3-5 sources) is too small for percentile statistics to be meaningful.

## Cache Strategy

- Path: `~/.claude/audit-cache/benchmark.json`
- TTL: 7 days (`fetched_at` + 7d < now → expired, refetch)
- GFW/rate-limit fallback: use expired cache, annotate in report as "benchmark data from {date} cache"
- First run without cache: must query at least one core source, otherwise mark Phase 2 as "unavailable"

## Authentication

- Prefer `gh api` (uses `gh auth` token automatically)
- Without `gh`: unauthenticated REST API, 60 req/h limit, sufficient (core sources need ~5 requests)
- If all fail: skip Phase 2, annotate the reason
