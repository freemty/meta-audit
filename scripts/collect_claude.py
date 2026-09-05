#!/usr/bin/env python3
"""Legacy Claude configuration snapshot; not a runtime or cross-host benchmark."""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess

def read(path):
    try:
        value=json.loads(path.read_text())
        return value if isinstance(value,dict) else {}
    except (OSError,ValueError):
        return {}

def files(path, pattern):
    return list(path.glob(pattern)) if path.is_dir() else []

def main():
    root=Path(os.environ.get('CLAUDE_DIR',str(Path.home()/'.claude')))
    settings=read(root/'settings.json')
    hooks=settings.get('hooks',{})
    entries=[handler for groups in hooks.values() if isinstance(groups,list) for group in groups if isinstance(group,dict) for handler in group.get('hooks',[]) if isinstance(handler,dict)]
    installed=read(root/'plugins/installed_plugins.json').get('plugins',{})
    try:
        count=subprocess.run(['git','rev-list','--count','--since=30 days ago','HEAD'],capture_output=True,text=True)
        velocity=int(count.stdout) if count.returncode==0 else 0
    except (OSError,ValueError):
        velocity=0
    instruction=Path('CLAUDE.md')
    result={
        'collected_at':datetime.now(timezone.utc).isoformat(),
        'scope':'claude-configuration-only',
        'limitations':['Counts are observed configuration, not executed behavior.',
                       'Codex, plugin runtime hook expansion, cron and model capability are not measured.'],
        'skills':{'count':sum((p/'SKILL.md').is_file() or (p/'skill.md').is_file() for p in files(root/'skills','*'))},
        'agents':{'count':len(files(root/'agents','*.md'))},
        'rules':{'count':len(files(root/'rules','*.md'))},
        'hooks':{'total_entries':len(entries),'event_types_used':sum(bool(v) for v in hooks.values() if isinstance(v,list)),
                 'has_project_level':bool(read(Path('.claude/settings.json')).get('hooks'))},
        'plugins':{'count':len(installed) if isinstance(installed,(dict,list)) else 0},
        'headless':{'has_cron':False,'cron_observed':False,'has_ci':bool(files(Path('.github/workflows'),'*.yml')+files(Path('.github/workflows'),'*.yaml'))},
        'meta_learning':{'has_reflection':(root/'audit-history').is_dir(),'basis':'directory existence only'},
        'activity':{'commit_velocity_30d':velocity,'claudemd_lines':len(instruction.read_text().splitlines()) if instruction.is_file() else 0},
    }
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
