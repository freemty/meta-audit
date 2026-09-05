#!/usr/bin/env python3
"""Read-only instruction audit: hard local contracts and separate review signals."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from skill_inventory import discover, parse_frontmatter

HARD = re.compile(r"\b(?:MUST|NEVER|ALWAYS|DO NOT|REQUIRED)\b|必须|禁止|不得|永远|务必")
HOST = re.compile(r"WebFetch|Agent tool|/loop\b|@(domain-expert|project-advisor|exp-manager|slides-maker|viz-frontend)")
OLD_PATH = re.compile(r"~/(?:\.claude/plugins|\.claude/skills)|/Users/[^/]+/(?:code|\.claude|\.codex)")
PLACEHOLDER = re.compile(r"[{}<>*]|\.\.\.|\b(?:URL|NAME|SLUG|FILE|PATH)\b")
SUFFIXES = {'.md','.py','.sh','.json','.yaml','.yml','.tex','.html'}

def prose(text):
    return re.sub(r"(?ms)^(`{3,}|~{3,}).*?^\1[^\n]*$", "", text)

def links(text):
    text = prose(text)
    found = [(m.group(1).split('#')[0], True) for m in re.finditer(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", text)]
    for token in re.findall(r"`([^`\n]+)`", text):
        if Path(token).suffix in SUFFIXES or (token.endswith('/') and any(part in token.split('/') for part in ('references','guides','agents'))):
            found.append((token.split('#')[0], False))
    return found

def resolve_link(token, path, skill, root):
    plugin = next((p for p in skill.parents if (p/'.codex-plugin').is_dir() or (p/'.claude-plugin').is_dir()), skill.parent)
    for marker, base in {'<plugin-root>/':plugin, '<skill-dir>/':skill.parent, '{skill_root}/':skill.parent}.items():
        if token.startswith(marker):
            candidate = base/token[len(marker):]
            return (candidate.resolve(), False) if candidate.exists() else (None, True)
    if not token or re.match(r"\w+://|mailto:|#",token) or PLACEHOLDER.search(token) or token.startswith(('~','/')):
        return None, False
    bases = [path.parent, skill.parent]
    if '/' in token:
        bases += [p for p in skill.parents if p == root or root in p.parents]
    for base in dict.fromkeys(bases):
        candidate = (base/token).resolve()
        if candidate.exists():
            return candidate, False
    # Markdown links promise a local resource; inline project output paths do not.
    return None, token != 'agents/' and token.startswith(('references/','scripts/','agents/','../'))

def historical(rel):
    value = rel.as_posix()
    return value.startswith(('projects/selfos/wiki/','projects/selfos/raw/')) or any(
        marker in '/' + value for marker in ('/docs/specs/','/docs/papers/','/clones/'))

def resources(skill, root):
    skill, root = skill.resolve(), root.resolve()
    visited, errors, queue = {}, [], [skill]
    while queue:
        path = queue.pop()
        if path in visited or path.suffix.lower() != '.md':
            continue
        text = path.read_text(encoding='utf-8', errors='replace')
        visited[path] = text
        for token, explicit in links(text):
            target, required = resolve_link(token, path, skill, root)
            if target is None:
                if required or (explicit and token and not (re.match(r"\w+://|mailto:|#",token) or PLACEHOLDER.search(token) or token.startswith(('~','/')))):
                    errors.append(f'{path.relative_to(root)}: missing reference {token}')
                continue
            # Never load historical source corpora or generated/user data as instructions.
            rel = target.relative_to(root) if target.is_relative_to(root) else None
            if rel and not historical(rel):
                if target.is_dir():
                    queue.extend(target.rglob('*.md'))
                if target.suffix.lower() == '.md' and target.is_file():
                    queue.append(target)
    return visited, sorted(set(errors))

def audit(root):
    root = root.resolve()
    records = []
    for item in discover(root, workspace=True):
        path = item['path']
        text = path.read_text(encoding='utf-8')
        fm = parse_frontmatter(text)
        loaded, errors = resources(path, root)
        if not fm or not fm.get('name') or not fm.get('description'):
            errors.append('missing/malformed name or description')
        policy = path.parent/'agents/openai.yaml'
        if policy.exists():
            policy_text = policy.read_text()
            matches = re.findall(r'^\s+allow_implicit_invocation:\s*(\S+)\s*$',policy_text,re.M)
            if 'allow_implicit_invocation' in policy_text and (len(matches) != 1 or matches[0] not in {'true','false'}):
                errors.append('invalid invocation policy')
        findings, details = [], []
        for resource, body in loaded.items():
            # Supported host frontmatter does not constrain shared body portability.
            if body.startswith('---\n'):
                body = body.split('---',2)[-1]
            signals = []
            if HOST.search(prose(body)): signals.append('host-specific-instruction-review')
            if OLD_PATH.search(body): signals.append('personal-install-path-review')
            if len(HARD.findall(body)) >= 8: signals.append('imperative-density-review')
            if signals:
                findings.extend(signals)
                details.append({'path':str(resource.relative_to(root)), 'signals':signals})
        words = len(text.split())
        if words > 500: findings.append('entrypoint-length-review')
        records.append({'path':str(path.relative_to(root)), 'scope':item['scope'], 'words':words,
                        'resources':[str(p.relative_to(root)) for p in loaded],
                        'errors':errors,'findings':sorted(set(findings)), 'resource_findings':details})
    hooks = []
    for path in (root/'plugins').glob('*/hooks/hooks.json') if (root/'plugins').is_dir() else root.glob('hooks/hooks.json'):
        try:
            value = json.loads(path.read_text())['hooks']
            hooks.append({'path':str(path.relative_to(root)), 'events':len(value),
                          'handlers':sum(len(e.get('hooks',[])) for entries in value.values() for e in entries)})
        except (KeyError, ValueError):
            hooks.append({'path':str(path.relative_to(root)),'error':'invalid-hooks-json'})
    return {'skills':records,'hooks':hooks,'summary':{
        'skill_count':sum(r['scope']=='public' for r in records),
        'workspace_count':sum(r['scope']=='workspace' for r in records),
        'flagged_skills':sum(bool(r['findings']) for r in records),
        'errors':sum(len(r['errors']) for r in records)+sum('error' in h for h in hooks)}}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('root',type=Path,nargs='?',default=Path.cwd())
    parser.add_argument('--json',action='store_true')
    parser.add_argument('--check',action='store_true',help='Fail on hard errors, not review signals')
    args=parser.parse_args()
    result=audit(args.root.resolve())
    if args.json:
        print(json.dumps(result,ensure_ascii=False,indent=2))
    else:
        s=result['summary']
        print(f"{s['skill_count']} public skills; {s['workspace_count']} workspace; {s['errors']} errors; {s['flagged_skills']} review signals")
        for r in result['skills']:
            for error in r['errors']: print(f"ERROR {r['path']}: {error}")
            for detail in r['resource_findings']: print(f"REVIEW {detail['path']}: {', '.join(detail['signals'])}")
    return int(args.check and bool(result['summary']['errors']))

if __name__=='__main__':
    raise SystemExit(main())
