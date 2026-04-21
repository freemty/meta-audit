# CC Navigator Skill

```
  ___ ___   _  _          _           _
 / __/ __| | \| |__ ___ _(_)__ _ __ _| |_ ___ _ _
| (_| (__  | .` / _` \ V / / _` / _` |  _/ _ \ '_|
 \___\___| |_|\_\__,_|\_/|_\__, \__,_|\__\___/_|
                            |___/
```

> **Claude Code Skill** | Installable via `npx skills add`

Your Claude Code workflow navigator -- recommends the right skill, agent, or tool for any task based on 11 curated sources. Part of [yuanbo-skills](https://github.com/freemty/yuanbo-skills).

## Install

```bash
npx skills add freemty/cc-navigator
```

<details>
<summary>Alternative install methods</summary>

**Manual (curl)**

```bash
mkdir -p ~/.claude/skills/cc-navigator
curl -sL https://raw.githubusercontent.com/freemty/cc-navigator/main/skills/cc-navigator/SKILL.md \
  -o ~/.claude/skills/cc-navigator/SKILL.md
```

**Git clone (as plugin)**

```bash
git clone https://github.com/freemty/cc-navigator.git ~/.claude/plugins/cc-navigator
```

Then add to your `~/.claude/settings.json`:
```json
{
  "plugins": ["~/.claude/plugins/cc-navigator"]
}
```

</details>

## What it does

- **Navigates your workflow** -- classifies your task and recommends the right skill, in the right order
- **Synthesizes best practices** from 11 authoritative CC-specific sources
- **Points to ecosystem tools** for web access, SWE workflows, and information presentation

## When it triggers

- "How should I approach this?"
- Starting a new task, feature, or debug session
- Unsure which skill or agent to use next
- Need to find the right tool for web access, testing, or presentation

## What's inside

| Section | Content |
|---------|---------|
| Decision Framework | Task classification table + workflow decision tree |
| Synthesized Principles | 8 cross-source principles for daily practice (11 sources) |
| Ecosystem Quick Reference | Web access, SWE workflow, and presentation tools |
| References | Full article archives + ecosystem detail guides |

## Sources

1. [Superpowers](https://github.com/obra/superpowers) -- TDD, task atomization, subagent-driven development
2. [AReaL / Starcat](https://github.com/inclusionAI/AReaL) -- 32-day zero-handwritten distributed RL
3. [CC Official: How It Works](https://code.claude.com/docs/how-claude-code-works) -- Agentic loop, context management
4. [CC Official: Hooks Guide](https://code.claude.com/docs/hooks-guide) -- 4 hook types, 19 lifecycle events
5. [Boris Cherny: CC Tips](https://x.com/bcherny/status/2017742741636321619) -- CC creator's 10 tips from the team
6. [Tw93: CC Architecture](https://x.com/HiTw93/status/2032091246588518683) -- Six-layer architecture, context governance
7. [Thariq: How We Use Skills](https://x.com/trq212/status/2033949937936085378) -- 9 skill categories, writing best practices
8. [Thariq: Seeing like an Agent](https://x.com/trq212/status/2027463795355095314) -- Tool design philosophy
9. [Harness Design](https://www.anthropic.com/engineering/harness-design-long-running-apps) -- GAN-inspired multi-agent for long tasks
10. [Anthropic Skills](https://github.com/anthropics/skills) -- Official skill spec, progressive disclosure, eval-driven skill development
11. [jiahao-shao1](https://github.com/jiahao-shao1) -- Research workflow skills, remote-cluster-agent, 5-tier web-fetcher

## License

MIT
