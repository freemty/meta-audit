---
name: hook-recipes
description: Use when a deterministic safety or feedback boundary genuinely requires a host lifecycle hook. Triggers on "add a hook", "what hooks should I have", "fix my hook coverage", or after meta-audit shows hook gaps.
---

# Hook Recipes

Use a hook only when the event boundary matters. Prefer an explicit tool, script,
test or CI check when it meets the task with less repeated context.

Define the event, actual payload, deterministic signal, desired effect and scope.
Check for an existing equivalent. Read `recipes.json`: these are six declarative
read-only feedback templates, not installable shell commands or permission gates.
Resolve the project-installed executable; do not let a package runner install
an unrequested tool. Adapt successful-edit signals, file paths and output format
to the actual host. Pass file paths as arguments, not interpolated shell code.

An explicit request to add a scoped hook authorizes that change; do not ask for
the same approval again. Ask only for a consequential missing scope or additional
external operation. A request to audit hooks is read-only.

Test matching, nonmatching, failed and missing-tool cases. Trigger a real host
event when available, distinguishing that from payload fixture tests. Do not
claim a hook enforces permissions unless the host's documented blocking semantics
were tested. Avoid arbitrary file-size limits, generic test reminders, forced
dry runs and suggestions that merely increase a hook-count score.
