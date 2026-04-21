#!/usr/bin/env bash
set -euo pipefail

# meta-audit local data collector
# Outputs deterministic JSON metrics for Phase 1 (local data collection).
# Claude uses this output as scoring input — no ad-hoc counting.

CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"
SKILLS_DIR="$CLAUDE_DIR/skills"
AGENTS_DIR="$CLAUDE_DIR/agents"
RULES_DIR="$CLAUDE_DIR/rules"
SETTINGS_FILE="$CLAUDE_DIR/settings.json"
PLUGINS_FILE="$CLAUDE_DIR/plugins/installed_plugins.json"

count_dir_entries() {
  local dir="$1"
  if [ -d "$dir" ]; then
    find "$dir" -maxdepth 1 -mindepth 1 -type d -o -type l 2>/dev/null | wc -l | tr -d ' '
  else
    echo "0"
  fi
}

count_files() {
  local dir="$1" pattern="$2"
  if [ -d "$dir" ]; then
    find "$dir" -maxdepth 1 -name "$pattern" 2>/dev/null | wc -l | tr -d ' '
  else
    echo "0"
  fi
}

# Skills count (directories/symlinks in ~/.claude/skills/)
skill_count=$(count_dir_entries "$SKILLS_DIR")

# Agent count (markdown files in ~/.claude/agents/)
agent_count=$(count_files "$AGENTS_DIR" "*.md")

# Rules count (markdown files in ~/.claude/rules/)
rules_count=$(count_files "$RULES_DIR" "*.md")

# Hook count and event types from settings.json
hook_count=0
hook_event_types=0
if [ -f "$SETTINGS_FILE" ]; then
  hook_count=$(python3 -c "
import json, sys
try:
    s = json.load(open('$SETTINGS_FILE'))
    hooks = s.get('hooks', {})
    total = sum(len(v) if isinstance(v, list) else 0 for v in hooks.values())
    print(total)
except: print(0)
" 2>/dev/null || echo "0")
  hook_event_types=$(python3 -c "
import json, sys
try:
    s = json.load(open('$SETTINGS_FILE'))
    hooks = s.get('hooks', {})
    types = [k for k, v in hooks.items() if isinstance(v, list) and len(v) > 0]
    print(len(types))
except: print(0)
" 2>/dev/null || echo "0")
fi

# Project-level hooks (search common project dirs)
project_hooks="false"
for d in . "$HOME/code" "$HOME/projects"; do
  if find "$d" -maxdepth 3 -path "*/.claude/settings.json" -exec grep -l '"hooks"' {} \; 2>/dev/null | head -1 | grep -q .; then
    project_hooks="true"
    break
  fi
done

# Plugin count
plugin_count=0
if [ -f "$PLUGINS_FILE" ]; then
  plugin_count=$(python3 -c "
import json
try:
    d = json.load(open('$PLUGINS_FILE'))
    print(len(d) if isinstance(d, list) else len(d.keys()))
except: print(0)
" 2>/dev/null || echo "0")
fi
# Also count from settings.json plugins array
if [ -f "$SETTINGS_FILE" ]; then
  settings_plugins=$(python3 -c "
import json
try:
    s = json.load(open('$SETTINGS_FILE'))
    print(len(s.get('plugins', [])))
except: print(0)
" 2>/dev/null || echo "0")
  if [ "$settings_plugins" -gt "$plugin_count" ] 2>/dev/null; then
    plugin_count=$settings_plugins
  fi
fi

# Cron/headless detection
has_cron="false"
if crontab -l 2>/dev/null | grep -q "claude\|claude-code\|skills"; then
  has_cron="true"
fi

# GitHub Actions detection (check recent repos)
has_ci="false"
if [ -f ".github/workflows/"*.yml ] 2>/dev/null || [ -f ".github/workflows/"*.yaml ] 2>/dev/null; then
  has_ci="true"
fi

# Reflection pipeline detection
has_reflection="false"
if [ -d "$CLAUDE_DIR/audit-history" ] || grep -rq "reflection\|self-improve\|meta-learning" "$SKILLS_DIR" 2>/dev/null; then
  has_reflection="true"
fi

# 30-day commit velocity
commit_velocity=$(git log --oneline --since="30 days ago" 2>/dev/null | wc -l | tr -d ' ' || echo "0")

# CLAUDE.md existence and size
claudemd_lines=0
if [ -f "CLAUDE.md" ]; then
  claudemd_lines=$(wc -l < "CLAUDE.md" | tr -d ' ')
fi

# Output as JSON
cat <<EOJSON
{
  "collected_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "skills": {
    "count": $skill_count
  },
  "agents": {
    "count": $agent_count
  },
  "rules": {
    "count": $rules_count
  },
  "hooks": {
    "total_entries": $hook_count,
    "event_types_used": $hook_event_types,
    "has_project_level": $project_hooks
  },
  "plugins": {
    "count": $plugin_count
  },
  "headless": {
    "has_cron": $has_cron,
    "has_ci": $has_ci
  },
  "meta_learning": {
    "has_reflection": $has_reflection
  },
  "activity": {
    "commit_velocity_30d": $commit_velocity,
    "claudemd_lines": $claudemd_lines
  }
}
EOJSON
