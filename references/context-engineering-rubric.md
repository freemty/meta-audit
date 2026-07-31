# Context Engineering Rubric

Use this rubric for findings produced by `context_audit.py`.

| Finding | Preferred owner |
| --- | --- |
| Contextual style or naming choice | Model judgment plus surrounding files |
| Deterministic file/state mutation | Typed script or tool |
| Large domain/style knowledge | On-demand reference |
| Subjective quality boundary | Rubric and verifier |
| Stable project fact or gotcha | Lightweight AGENTS.md/CLAUDE.md or project memory |
| Destructive action, provenance, external side effect | Explicit hard boundary |

Flag:

- the same imperative in multiple layers;
- skill descriptions that summarize workflows instead of triggers;
- frequently injected catalogs or reminders;
- host/model/tool names in portable bodies;
- host-specific tool permission fields in shared skill frontmatter;
- entrypoints above 500 words without a documented reason;
- examples that duplicate a typed interface;
- source and installed-cache versions that identify different content as the
  same release.

Simplification is accepted only after representative behavior tests pass on
each supported host/model class.
