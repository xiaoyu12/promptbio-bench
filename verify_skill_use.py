#!/usr/bin/env python3
"""Check whether the PromptBio-Bench agent runs used any Agent Skill.

Claude Code writes one JSONL transcript per subagent under
  ~/.claude/projects/<project-dir>/<session-id>/subagents/**/agent-*.jsonl
Every tool call the agent makes is recorded there. A skill's content can only reach an agent
through a tool call: the Skill tool, or reading/grepping a file under .claude/skills/ (SKILL.md
and its scripts). So, per run, this script reports:

  1. coverage    - transcripts found, and whether every benchmark task has at least one
  2. available   - transcripts whose context lists the installed skills (names from .claude/skills)
  3. Skill tool  - calls to the Skill tool, and which skills
  4. skill files - tool calls whose input mentions .claude/skills or SKILL.md, or a skill-specific path
  5. mentions    - agent-visible text or tool input naming "skill" or an installed skill

Usage:
  python3 run/verify_skill_use.py                       # both runs, default locations
  python3 run/verify_skill_use.py --show 5              # also print up to 5 matching lines per check
"""

import argparse
import glob
import json
import os
import re
from collections import Counter

RUNS = {
    "claude-skills": {
        "transcripts": "~/.claude/projects/-mnt-e-workspace-promptbio-bench-data",
        "skills_dir": "promptbio-bench-claude-skills/.claude/skills",
        "tasks_dir": "promptbio-bench-claude-skills/tasks",
    },
    "claude-no-skills": {
        "transcripts": "~/.claude/projects/-mnt-e-workspace-promptbio-bench-no-skills",
        "skills_dir": "promptbio-bench-no-skills/.claude/skills",
        "tasks_dir": "promptbio-bench-no-skills/tasks",
    },
}
TASK_RE = re.compile(r"tasks/([ab]-\d+-\d+)\b")
SKILL_PATH_RE = re.compile(r"\.claude/skills|SKILL\.md", re.I)


def text_of(content):
    if isinstance(content, str):
        return content
    parts = []
    for block in content or []:
        if block.get("type") == "text":
            parts.append(block.get("text", ""))
        elif block.get("type") == "tool_result":
            parts.append(text_of(block.get("content")))
    return "\n".join(parts)


def check_run(name, cfg, show):
    skills = sorted(os.listdir(cfg["skills_dir"])) if os.path.isdir(cfg["skills_dir"]) else []
    tasks = sorted(d for d in os.listdir(cfg["tasks_dir"]) if TASK_RE.match(f"tasks/{d}"))
    files = [f for f in glob.glob(os.path.expanduser(cfg["transcripts"]) + "/**/*.jsonl", recursive=True)
             if os.sep + "subagents" + os.sep in f]
    # distinctive skill names only (avoid generic words like "dnasp" matching prose by chance is fine; skip short ones)
    named = [s for s in skills if len(s) >= 8]
    name_re = re.compile("|".join(re.escape(s) for s in named)) if named else None

    covered, available = set(), 0
    skill_calls, path_hits, mentions = Counter(), [], []
    for fp in files:
        has_listing = False
        for line in open(fp, errors="replace"):
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = d.get("message") or {}
            if d.get("type") in ("user", "system") or d.get("type") == "attachment":
                txt = text_of(msg.get("content")) if msg else json.dumps(d)
                covered.update(TASK_RE.findall(txt))
                if name_re and len(name_re.findall(txt)) >= 5:   # a skill catalogue lists many names
                    has_listing = True
            if d.get("type") != "assistant":
                continue
            for b in msg.get("content") or []:
                if b.get("type") == "tool_use":
                    inp = json.dumps(b.get("input"))
                    covered.update(TASK_RE.findall(inp))
                    if b.get("name") == "Skill":
                        skill_calls[(b.get("input") or {}).get("skill")] += 1
                    if SKILL_PATH_RE.search(inp):
                        path_hits.append(f"{os.path.basename(fp)}: {b.get('name')} {inp[:150]}")
                    if name_re and name_re.search(inp):
                        mentions.append(f"{os.path.basename(fp)}: tool input: {inp[:150]}")
                elif b.get("type") == "text":
                    t = b.get("text", "")
                    if re.search(r"\bskills?\b", t, re.I) or (name_re and name_re.search(t)):
                        mentions.append(f"{os.path.basename(fp)}: text: {t[:150]!r}")
        available += has_listing

    print(f"\n=== {name}")
    print(f"  installed skills            : {len(skills)}")
    print(f"  subagent transcripts        : {len(files)}")
    missing = [t for t in tasks if t not in covered]
    print(f"  tasks with a transcript     : {len(set(tasks) & covered)}/{len(tasks)}"
          + (f"  (missing: {', '.join(missing[:10])})" if missing else ""))
    print(f"  transcripts listing skills  : {available}")
    print(f"  Skill tool calls            : {sum(skill_calls.values())} {dict(skill_calls) if skill_calls else ''}")
    print(f"  tool calls touching skills  : {len(path_hits)}")
    print(f"  mentions of skills by agent : {len(mentions)}")
    for label, hits in (("touching skills", path_hits), ("mentions", mentions)):
        for h in hits[:show]:
            print(f"    [{label}] {h}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--show", type=int, default=0, help="print up to N matching lines per check")
    args = ap.parse_args()
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    for name, cfg in RUNS.items():
        check_run(name, cfg, args.show)


if __name__ == "__main__":
    main()
