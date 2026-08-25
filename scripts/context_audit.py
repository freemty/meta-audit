#!/usr/bin/env python3
"""Report context-engineering debt without modifying the target repository."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


HARD = re.compile(r"\b(?:MUST|NEVER|ALWAYS|DO NOT|REQUIRED)\b|必须|禁止|不得|永远|务必")
HOST = re.compile(
    r"Claude Code|Codex|Antigravity|WebFetch|Agent tool|/loop\b|"
    r"@(domain-expert|project-advisor|exp-manager|slides-maker|viz-frontend)"
)


def skill_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for path in root.rglob("*"):
        if path.name not in {"SKILL.md", "skill.md"} or not path.is_file():
            continue
        if any(part in {".git", "node_modules", ".venv"} for part in path.parts):
            continue
        relative = path.relative_to(root)
        if tuple(relative.parts[-4:]) in {
            (".agents", "skills", "project-skill", "SKILL.md"),
            (".claude", "skills", "project-skill", "SKILL.md"),
        }:
            continue
        files.append(path)
    return sorted(files)


def split_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---\n"):
        return "", text
    end = text.find("\n---\n", 4)
    if end < 0:
        return "", text
    return text[4:end], text[end + 5 :]


def description(frontmatter: str) -> str:
    match = re.search(r"^description:\s*(.*)$", frontmatter, re.MULTILINE)
    return match.group(1).strip() if match else ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, nargs="?", default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero when any skill entrypoint is flagged",
    )
    args = parser.parse_args()
    root = args.root.resolve()
    skills = []
    for path in skill_files(root):
        text = path.read_text(encoding="utf-8", errors="replace")
        frontmatter, body = split_frontmatter(text)
        words = len(re.findall(r"\b[\w'-]+\b", text))
        findings = []
        if words > 500:
            findings.append("entrypoint-over-500-words")
        # allowed-tools is intentionally kept: Claude Code enforces it and
        # other hosts ignore unknown frontmatter keys harmlessly.
        desc = description(frontmatter)
        if desc and not (desc.startswith("Use when") or desc in {">", "|", ">-", "|-"}):
            findings.append("description-is-not-trigger-first")
        if HOST.search(body):
            findings.append("host-specific-body")
        hard_count = len(HARD.findall(body))
        if hard_count >= 8:
            findings.append("high-imperative-density")
        skills.append(
            {
                "path": str(path.relative_to(root)),
                "words": words,
                "hard_directives": hard_count,
                "findings": findings,
            }
        )

    instruction_files = []
    for name in ("AGENTS.md", "CLAUDE.md"):
        for path in root.rglob(name):
            if ".git" in path.parts:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            instruction_files.append(
                {
                    "path": str(path.relative_to(root)),
                    "words": len(re.findall(r"\b[\w'-]+\b", text)),
                }
            )

    hook_configs = []
    for path in root.rglob("hooks.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
            handlers = sum(
                len(entry.get("hooks", []))
                for entries in payload.get("hooks", {}).values()
                for entry in entries
            )
            hook_configs.append(
                {
                    "path": str(path.relative_to(root)),
                    "events": len(payload.get("hooks", {})),
                    "handlers": handlers,
                }
            )
        except (OSError, json.JSONDecodeError):
            hook_configs.append(
                {"path": str(path.relative_to(root)), "error": "invalid-json"}
            )

    payload = {
        "root": str(root),
        "skills": skills,
        "instructions": instruction_files,
        "hooks": hook_configs,
        "summary": {
            "skill_count": len(skills),
            "flagged_skills": sum(bool(item["findings"]) for item in skills),
            "total_skill_words": sum(item["words"] for item in skills),
        },
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(
            f"{payload['summary']['skill_count']} skills; "
            f"{payload['summary']['flagged_skills']} flagged"
        )
        for item in skills:
            if item["findings"]:
                print(
                    f"- {item['path']}: {item['words']} words; "
                    + ", ".join(item["findings"])
                )
    return 1 if args.check and payload["summary"]["flagged_skills"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
