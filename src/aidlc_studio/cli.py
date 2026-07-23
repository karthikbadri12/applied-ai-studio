"""aidlc — install the Applied AI Studio agent pack into any project, for any IDE.

Usage:
  uvx aidlc init [PATH] --ide all          # scaffold everything
  uvx aidlc init [PATH] --ide claude       # Claude Code custom agents + skills
  uvx aidlc init [PATH] --ide cursor       # Cursor rules + AGENTS.md
  uvx aidlc init [PATH] --ide copilot      # VS Code Copilot chatmodes + AGENTS.md
  uvx aidlc init [PATH] --ide antigravity  # AGENTS.md (Antigravity/Windsurf standard)
  aidlc list                               # show the 23-agent roster
  aidlc check [PATH]                       # verify an install
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

IDES = ("all", "claude", "cursor", "copilot", "antigravity", "windsurf")

# Core files every IDE flavor needs: the constitution, methodology, registry,
# templates, connectors, domains, and the cross-tool AGENTS.md entry point.
CORE = [
    "AGENTS.md",
    "CONSTITUTION.md",
    "ARCHITECTURE.md",
    "SKILLS.md",
    "registry",
    "artifacts",
    "connectors",
    "domains",
    "pipelines",
    "docs",
]

PER_IDE = {
    "claude": [".claude"],
    "cursor": [".cursor"],
    "copilot": [],       # chatmodes are generated from the agent files at init time
    "antigravity": [],   # AGENTS.md standard only
    "windsurf": [],      # AGENTS.md standard only
}


def pack_root() -> Path:
    """Locate the bundled pack (wheel install) or the repo itself (dev checkout)."""
    bundled = Path(__file__).resolve().parent / "pack"
    if bundled.is_dir():
        return bundled
    repo = Path(__file__).resolve().parents[2]
    if (repo / "CONSTITUTION.md").is_file():
        return repo
    sys.exit("aidlc: could not locate the agent pack (broken install?)")


def copy_item(src: Path, dst: Path, force: bool) -> int:
    """Copy a file or tree, skipping existing files unless --force. Returns files written."""
    written = 0
    if src.is_dir():
        for f in sorted(src.rglob("*")):
            if f.is_dir() or "__pycache__" in f.parts:
                continue
            target = dst / f.relative_to(src)
            if target.exists() and not force:
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, target)
            written += 1
    elif src.is_file():
        if dst.exists() and not force:
            return 0
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        written = 1
    return written


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Minimal YAML-ish frontmatter parser (name/description/model keys)."""
    meta: dict = {}
    body = text
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            body = parts[2].lstrip("\n")
            for line in parts[1].splitlines():
                if ":" in line:
                    k, _, v = line.partition(":")
                    meta[k.strip()] = v.strip()
    return meta, body


def generate_chatmodes(pack: Path, target: Path, force: bool) -> int:
    """VS Code Copilot: turn each agent into .github/chatmodes/<name>.chatmode.md."""
    written = 0
    agents_dir = pack / ".claude" / "agents"
    out_dir = target / ".github" / "chatmodes"
    for agent_file in sorted(agents_dir.glob("*.md")):
        meta, body = parse_frontmatter(agent_file.read_text(encoding="utf-8"))
        name = meta.get("name", agent_file.stem)
        desc = meta.get("description", "").replace("\n", " ")[:500]
        out = out_dir / f"{name}.chatmode.md"
        if out.exists() and not force:
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(f"---\ndescription: {desc}\n---\n{body}", encoding="utf-8")
        written += 1
    return written


GLOBAL_NOTE = """
## Global install note
This agent is installed user-globally. Its support files live in `~/.claude/aidlc/`:
- Constitution: `~/.claude/aidlc/CONSTITUTION.md` (read it FIRST, always)
- Registries: `~/.claude/aidlc/registry/` (stages.json · agents.json · skills.json)
- Artifact templates: `~/.claude/aidlc/artifacts/templates/`
- Skills: `~/.claude/skills/<name>/SKILL.md`
- Domains / connectors / pipelines: `~/.claude/aidlc/`
If the current project has its own copies (a project-scoped install), prefer those.
Write stage artifacts into the current project's `artifacts/` directory.
"""


def cmd_global(pack: Path, force: bool) -> None:
    """Install user-globally: agents+skills into ~/.claude, support pack into ~/.claude/aidlc."""
    home = Path.home() / ".claude"
    total = 0

    # Agents — copied with a note pointing at the global support pack.
    agents_out = home / "agents"
    agents_out.mkdir(parents=True, exist_ok=True)
    for agent_file in sorted((pack / ".claude" / "agents").glob("*.md")):
        out = agents_out / agent_file.name
        if out.exists() and not force:
            continue
        out.write_text(agent_file.read_text(encoding="utf-8").rstrip() + "\n" + GLOBAL_NOTE,
                       encoding="utf-8")
        total += 1

    # Skills — verbatim.
    total += copy_item(pack / ".claude" / "skills", home / "skills", force)

    # Support pack — constitution, registries, templates, domains, connectors, pipelines, docs.
    support = home / "aidlc"
    for item in CORE:
        src = pack / item
        if src.exists():
            total += copy_item(src, support / item, force)

    print(f"✔ Applied AI Studio installed GLOBALLY (files written: {total})")
    print(f"  • agents  → {agents_out}  (23 custom agents, every project)")
    print(f"  • skills  → {home / 'skills'}  (14 skills)")
    print(f"  • support → {support}  (constitution · registries · templates · domains)")
    print("\nOpen ANY folder in VS Code / your IDE, run `claude`, then `/agents` — the roster is there.")
    print("Say: “Use the orchestrator agent. Problem statement: …”  Artifacts land in ./artifacts/.")
    print("Update later: re-run this command with --force. Uninstall: remove the files above.")


def cmd_init(args: argparse.Namespace) -> None:
    pack = pack_root()
    if getattr(args, "global_install", False):
        cmd_global(pack, args.force)
        return
    target = Path(args.path).resolve()
    target.mkdir(parents=True, exist_ok=True)

    ides = list(PER_IDE) if args.ide == "all" else [args.ide]
    # windsurf/antigravity are AGENTS.md-only; both resolve to core files
    items = list(CORE)
    for ide in ides:
        items += PER_IDE.get(ide, [])

    total = 0
    for item in items:
        src = pack / item
        if not src.exists():
            continue
        total += copy_item(src, target / item, args.force)

    if "copilot" in ides:
        total += generate_chatmodes(pack, target, args.force)

    print(f"✔ Applied AI Studio installed into {target}")
    print(f"  IDE flavor(s): {', '.join(ides)}  ·  files written: {total}"
          + ("" if args.force else "  (existing files skipped; use --force to overwrite)"))
    print("\nNext steps:")
    if "claude" in ides:
        print("  • Claude Code:  cd into the project, run `claude`, then `/agents` — the 23 agents are loaded.")
    if "cursor" in ides:
        print("  • Cursor:       open the project; .cursor/rules + AGENTS.md load automatically.")
    if "copilot" in ides:
        print("  • VS Code:      Copilot agent mode reads AGENTS.md; per-agent chatmodes in .github/chatmodes/.")
    if "antigravity" in ides or "windsurf" in ides:
        print("  • Antigravity/Windsurf: AGENTS.md is picked up automatically on open.")
    print("  • Start:        “Act as the orchestrator. Problem statement: …”")
    print("  • Connectors:   copy blocks from connectors/mcp.example.json into your IDE's MCP config.")
    print("  • Smoke test:   docs/INSTALL.md (2 minutes).")


def cmd_list(_: argparse.Namespace) -> None:
    pack = pack_root()
    reg = json.loads((pack / "registry" / "agents.json").read_text(encoding="utf-8"))
    skills = json.loads((pack / "registry" / "skills.json").read_text(encoding="utf-8"))["agents"]
    by_type: dict = {}
    for a in reg["agents"]:
        by_type.setdefault(a["type"], []).append(a)
    for group in ("orchestrator", "pipeline", "advisor", "dev-pipeline"):
        print(f"\n{group.upper()} ({len(by_type.get(group, []))})")
        for a in by_type.get(group, []):
            s = skills.get(a["id"], {})
            extra = f"  [{s.get('bmadPersona', '')} · {s.get('speckitPhase', '')}]" if s else ""
            stage = f"  stage {a['stage']:>2}" if "stage" in a else ""
            print(f"  • {a['id']:<18}{stage}{extra}")
    print(f"\nTotal: {len(reg['agents'])} agents · 14 skills · constitution-governed")


def cmd_check(args: argparse.Namespace) -> None:
    target = Path(args.path).resolve()
    core = {
        "CONSTITUTION.md": target / "CONSTITUTION.md",
        "AGENTS.md": target / "AGENTS.md",
        "stage registry": target / "registry" / "stages.json",
        "skills registry": target / "registry" / "skills.json",
        "templates": target / "artifacts" / "templates",
    }
    ok = True
    for label, p in core.items():
        found = p.exists()
        n = f" ({len(list(p.glob('**/*.md')))} files)" if found and p.is_dir() else ""
        print(f"  {'✔' if found else '✘'} {label}{n}")
        ok = ok and found

    # Agent definitions can live in any flavor's location — at least one must exist.
    flavors = {
        "Claude Code (.claude/agents + skills)": target / ".claude" / "agents",
        "Cursor (.cursor/rules)": target / ".cursor" / "rules",
        "Copilot (.github/chatmodes)": target / ".github" / "chatmodes",
    }
    any_flavor = False
    for label, p in flavors.items():
        found = p.is_dir() and any(p.glob("**/*.md*"))
        any_flavor = any_flavor or found
        print(f"  {'✔' if found else '·'} {label}")
    if not any_flavor:
        print("  ✘ no IDE agent definitions found (run `aidlc init --ide <flavor>`)")
    print("  note: Antigravity/Windsurf installs are AGENTS.md-only — core ✔ is sufficient.")
    sys.exit(0 if (ok and any_flavor) else 1)


def main() -> None:
    parser = argparse.ArgumentParser(prog="aidlc", description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_init = sub.add_parser("init", help="scaffold the agent pack into a project")
    p_init.add_argument("path", nargs="?", default=".", help="target project directory (default: .)")
    p_init.add_argument("--ide", choices=IDES, default="all", help="which IDE flavor to install (default: all)")
    p_init.add_argument("--global", dest="global_install", action="store_true",
                        help="install user-globally (~/.claude) so the agents exist in EVERY project")
    p_init.add_argument("--force", action="store_true", help="overwrite existing files")
    p_init.set_defaults(fn=cmd_init)

    p_list = sub.add_parser("list", help="show the agent roster")
    p_list.set_defaults(fn=cmd_list)

    p_check = sub.add_parser("check", help="verify an installed pack")
    p_check.add_argument("path", nargs="?", default=".", help="project directory to check")
    p_check.set_defaults(fn=cmd_check)

    args = parser.parse_args()
    args.fn(args)


if __name__ == "__main__":
    main()
