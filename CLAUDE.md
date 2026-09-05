# meta-audit

Portable workflow/context audit with optional deterministic adapters.

- `scripts/skill_inventory.py` owns public/workspace discovery and frontmatter
  parsing; the outer marketplace validator, audit and installer reuse it.
- `scripts/context_audit.py` follows executable reference links. Hard contract
  failures block; length, personal paths and instruction density are review signals.
- `collect.sh` is a legacy Claude-config adapter, not proof of runtime behavior.
- `hook-recipes/recipes.json` contains six read-only adapter templates, not
  installed hooks or safety gates.
- Read-only audit does not authorize edits, installation, commits or publication.
  Test changed script behavior with temporary fixtures; report live gaps honestly.
