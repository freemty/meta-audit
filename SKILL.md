---
name: meta-audit
description: Use when explicitly auditing an agent workflow, repository automation maturity, repeated friction, or context-engineering debt. Triggers on /meta-audit, "audit my setup", "how automated am I", "what should I build next", "automation maturity check".
---

# Meta Audit

Audit observed behavior and executable interfaces, not aspirational docs.

## Modes

- `workflow`: repeated manual sequences, failure recovery, missing feedback.
- `automation`: maturity, coverage, and high-leverage automation candidates.
- `context`: duplicated instructions, overlong skill entrypoints, reminder
  hooks, host-specific assumptions, and rules that belong in tools/tests.

For context mode, run:

```bash
python3 scripts/context_audit.py --check <repo-root>
```

Then inspect the highest-signal findings. Classify each instruction as:
model judgment, typed interface, on-demand reference, verifier/rubric, durable
state, or hard safety/provenance boundary.

Return top friction, evidence, proposed owner/layer, expected benefit, and a
behavioral validation case. Do not recommend a new skill or hook when a smaller
script, schema, test, or deletion solves the problem.
