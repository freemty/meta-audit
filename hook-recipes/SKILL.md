---
name: hook-recipes
description: Use when a deterministic safety or feedback boundary genuinely requires a host lifecycle hook. Triggers on "add a hook", "what hooks should I have", "fix my hook coverage", or after meta-audit shows hook gaps.
---

# Hook Recipes

Use a hook only when the event boundary itself matters. Prefer a tool schema,
script, test, CI check, or model judgment for everything else.

1. Define the exact event, matcher, deterministic signal, and desired effect.
2. Check for an existing equivalent and for a lower-context implementation.
3. Read `recipes.json` and select the closest compatible recipe.
4. Adapt paths and host payload shape, show the exact mutation, and obtain
   approval.
5. Trigger the real host event and verify both matching and non-matching cases.

Good hooks enforce destructive-action boundaries or run cheap deterministic
feedback. Avoid catalogs, cross-sell reminders, generic planning prompts, and
frequent natural-language nudges.
