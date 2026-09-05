#!/usr/bin/env python3
"""Shared public skill discovery and frontmatter scalars; no third-party runtime."""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import sys


def parse_frontmatter(text):
    lines = text.splitlines()
    if not lines or lines[0].strip() != '---':
        return None
    result, i = {}, 1
    while i < len(lines):
        line = lines[i]
        if line.strip() == '---':
            return result
        match = re.match(r'^([\w-]+):\s*(.*)$', line)
        i += 1
        if not match:
            continue
        key, value = match.groups()
        if re.fullmatch(r'[>|][+-]?', value):
            parts = []
            while i < len(lines) and (not lines[i].strip() or lines[i][0].isspace()):
                parts.append(lines[i].strip())
                i += 1
            result[key] = ('\n' if value.startswith('|') else ' ').join(parts).strip()
        elif value.startswith('"'):
            try:
                result[key] = json.JSONDecoder().raw_decode(value)[0]
            except ValueError:
                return None
        elif value.startswith("'"):
            quoted = re.match(r"^'((?:[^']|'')*)'(?:\s+#.*)?$", value)
            if not quoted:
                return None
            result[key] = quoted[1].replace("''", "'")
        else:
            result[key] = re.split(r'\s+#', value, maxsplit=1)[0].strip()
    return None


def walk_skills(root):
    if not root.is_dir() or root.is_symlink():
        return []
    found = []
    for folder, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in {'node_modules','__pycache__','vendor'} and not (Path(folder)/d).is_symlink()]
        for name in ('SKILL.md','skill.md'):
            if name in files:
                found.append(Path(folder)/name)
                break
    return found


def discover(root, workspace=False):
    root = Path(root).resolve()
    monorepo = (root/'install.sh').is_file() and (root/'plugins').is_dir()
    roots = [root/'skills', root/'plugins', root/'projects/selfos/.claude/skills'] if monorepo else [root]
    result = [{'path':p, 'scope':'public'} for directory in roots for p in sorted(walk_skills(directory))]
    if workspace:
        result += [{'path':p,'scope':'workspace'} for p in walk_skills(root/'.agents/skills') if p.parent.name != 'project-skill']
    return result  # roots define legacy installer precedence: standalone, plugins, project


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root', type=Path, nargs='?', default=Path.cwd())
    parser.add_argument('--null', action='store_true')
    parser.add_argument('--workspace', action='store_true')
    args = parser.parse_args()
    values = discover(args.root, args.workspace)
    if args.null:
        sys.stdout.buffer.write(b''.join(os.fsencode(v['path'])+b'\0' for v in values))
    else:
        print(json.dumps([{'path':str(v['path'].relative_to(args.root.resolve())), 'scope':v['scope']} for v in values], indent=2))


if __name__ == '__main__':
    main()
