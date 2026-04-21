---
name: meta-audit
disable-auto-invoke: true
description: >
  Use when the user explicitly requests an automation maturity audit via /meta-audit.
  Assesses AI coding tool automation maturity, identifies gaps vs ecosystem benchmarks,
  and recommends what skills/hooks/workflows to build next.
  Triggers: /meta-audit, "我的自动化水平怎么样", "我在哪个段位", "该优先建什么",
  "audit my setup", "how automated am I".
---

# Meta Audit

从使用数据出发，对标外部生态基准，产出有证据的自动化成熟度定位 + 具体行动项。

## When to Use

- 每月定期审计 / 完成重大里程碑后
- 想知道"下一步该建什么"
- 感觉效率瓶颈但不确定瓶颈在哪

## When NOT to Use

- 日常 code review / 单次 session 回顾 / 纯项目进度检查

## Pipeline

1. **数据采集** — 运行 `bash collect.sh`（本 skill 目录下），获取确定性 JSON 输出。包含 skill/hook/plugin/agent 计数、headless 检测、30天 commit velocity。不要手动计数或猜测。
2. **外部基准** — `gh api` 查核心源 (superpowers-marketplace, anthropics/skills, everything-claude-code 等) 提取 skill/hook/plugin count。缓存 7 天。详见 `sources.md`。不可用则跳过并标注。
3. **分析定位** — L0-L5 打分 + 5轴雷达 + friction 根因映射
4. **输出报告** — Markdown 精简报告 + 存档到 `~/.claude/audit-history/{YYYY-MM-DD}.md`

## 成熟度模型 (L0-L5)

数量是必要条件，不是充分条件。L3+ 的判定必须结合结果指标（friction 下降、commit velocity 提升、手动干预减少），单靠配置数量堆叠不升级。

| Level | 定义 | 判定条件 |
|-------|------|---------|
| L0 Vanilla | 只用 CLAUDE.md | skills=0, hooks=0 |
| L1 Configured | 有 rules + 几个 skills | skills<15, hooks≤1 |
| L2 Skilled | 大量 skills，手动触发 | skills≥15, hooks<3 |
| L3 Hooked | skills + hooks + agents，friction 可观测下降 | hooks≥3, project-level hooks, wrong_approach friction 较 L2 下降 |
| L4 Orchestrated | headless/cron + multi-agent，手动干预率低 | 有持久化 cron 或 GitHub Actions, 人工介入 <30% sessions |
| L5 Autonomous | self-healing + meta-learning，持续改善 | 有 reflection pipeline, 月度 friction 趋势下降 |

## 雷达维度 (5 轴)

1. **Skill 宽度** — skill 数 / 生态 P99
2. **Hook 深度** — hook entries / 可用 event types (4 types × 19 lifecycle events)
3. **Headless 程度** — cron + CI/CD automation
4. **Multi-agent** — agent 定义数 + parallel dispatch
5. **Meta-learning** — reflection/self-improvement loop 存在性

## Friction → Action 映射

| Friction 类型 | 建议改进 |
|--------------|---------|
| wrong_approach 高 | PreToolUse guard hooks / CLAUDE.md constraints |
| buggy_code 高 | PostToolUse type-check hooks |
| tool_failure 高 | 环境 preflight skills |

## 报告结构

```
# Meta Audit — {date}
## 定位: L{N} (vs 前次 L{M})
## 雷达: 5维表 (分数 / 生态P50 / 差距)
## Top-3 Friction → Top-3 Action
## 与上次对比 (新增/改善/退步)
```

## 执行约束

- **不要自动执行改进** — 只输出建议，执行需人确认
- **facets 批量解析** — Python 处理，不要逐文件 Read
- **外部查询并行** — GitHub API 调用用 Agent 并行 spawn（用 `gh api` 或无认证 REST，注意 60 req/h 限制）
- **`--verbose`** — 输出完整 friction detail + benchmark 原始数据
- **`--quick`** — 跳过外部基准，只用本地数据

## Action Template

每个 Top-3 行动项必须包含：
1. **做什么** — 一句话描述具体改变
2. **怎么做** — 可直接执行的命令或 skill invocation（如 `/web-fetcher`、`/cc-navigator`）
3. **验证方式** — 怎么确认做完了（重新跑 `collect.sh` 对比哪个字段变化）

示例：
```
Action 1: 添加 PostToolUse type-check hook
  做: 在 ~/.claude/settings.json 的 hooks.PostToolUse 加 pyright check
  跑: /update-config
  验: collect.sh → hooks.total_entries +1, hooks.event_types_used 含 PostToolUse
```

## Common Mistakes

| 错误 | 正确做法 |
|------|---------|
| 用"典型用户"做对比但无数据来源 | 引用具体 repo + star 数 |
| 把 skill 数量等同于成熟度 | L2→L3 关键是 hooks + friction 下降，不只是 skills |
| 建议太多（10+ 行动项） | 最多 Top-3，focus 才能执行 |
| 对比数据过时 | 7 天 TTL 缓存，过期重新拉取 |
| 行动项没有执行路径 | 每个 action 必须有命令/skill + 验证方式 |
