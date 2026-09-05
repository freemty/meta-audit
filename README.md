# meta-audit

Version 1.1.0. Audit observed workflow friction and context debt, then propose
the smallest effective change. Counts are inventory, not productivity scores.

## Use

Claude Code plugin: `/meta-audit:meta-audit`. Codex plugin:
`$meta-audit:meta-audit` or the host skill selector. Natural-language discovery
depends on the host. Install through the yuanbo-skills marketplace on Codex;
do not also register global copies of the plugin's skills.

```bash
python3 scripts/context_audit.py --check /path/to/repository
python3 scripts/context_audit.py --json /path/to/repository
```

The audit shares discovery with the marketplace validator and installer, including
bundled selfOS entries and separately counted workspace skills. It follows
referenced instructions and distinguishes hard link/policy errors from review
signals. Long style rubrics can be valid.

`collect.sh` remains an optional Claude-config snapshot adapter. Its counts do
not establish active Codex registration or completed model behavior.
`sources.md` explains evidence-bounded external comparisons.

## Hook recipes

Six read-only type/lint/format feedback templates in `hook-recipes/recipes.json`
need a tested host adapter and an already installed project executable. Generic
test-before-commit, 800-line guards and forced dry-run templates were removed.
An audit is read-only; installing a hook requires the corresponding user intent.

MIT.
