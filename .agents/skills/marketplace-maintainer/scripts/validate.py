#!/usr/bin/env python3
r"""Check that this repo's Codex plugin marketplace is consistent.

Run from anywhere inside the repo:
    python .agents/skills/marketplace-maintainer/scripts/validate.py

Checks:
- marketplace.json is valid, entry names are unique, and paths are relative.
- Each entry's folder has a .codex-plugin/plugin.json whose name matches.
- Each plugin's skills path holds at least one skill. Both layouts are accepted:
  a folder of skill folders (skills/<name>/SKILL.md) or a folder holding
  SKILL.md directly (skill/SKILL.md, as the HR plugins use).
- Each SKILL.md has a name and description; icon paths in agents/openai.yaml
  and in plugin.json point at real files.
- No file inside a skill folder contains an absolute path (C:\..., \\server\...,
  /Users/..., /home/...). Home-folder paths (~/, $HOME, %USERPROFILE%) are
  warnings, because they only work on a machine laid out like the author's.
- Plugin folders that aren't listed in marketplace.json.
- Relative links, images, and #anchors in every Markdown file (the READMEs,
  INSTALL.md, MAINTAIN.md, and any other .md in the repo).

Exits 0 when there are no errors (warnings are allowed) and 1 otherwise.
Uses the standard library only.
"""
import json
import re
import sys
from pathlib import Path

MARKETPLACE = Path(".agents/plugins/marketplace.json")
PLUGINS_DIR = Path("plugins")

# A path runs until whitespace, a quote, a backtick, or a closing bracket.
_PATH_TAIL = r"[^\s\"'`)<>\]]*"
ABSOLUTE_PATHS = [
    ("Windows path", re.compile(r"(?<![A-Za-z0-9])[A-Za-z]:[\\/]" + _PATH_TAIL)),
    ("network path", re.compile(r"(?<![\w\\])\\\\[\w.$-]+\\" + _PATH_TAIL)),
    # Only well-known roots, so slash commands like /plugins and URLs don't match.
    ("absolute path", re.compile(
        r"(?<![\w.:/~-])/(?:Users|home|root|etc|var|tmp|opt|usr|mnt|private|Volumes|srv)/" + _PATH_TAIL)),
]
HOME_PATH = re.compile(
    r"(?<![\w/])(?:~[\\/]|\$HOME\b|\$\{HOME\}|\$env:USERPROFILE|%USERPROFILE%|%HOMEPATH%)" + _PATH_TAIL)


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.counts = {"plugins": 0, "skills": 0, "links": 0}

    def error(self, where, message):
        self.errors.append(f"{where}: {message}")

    def warn(self, where, message):
        self.warnings.append(f"{where}: {message}")


def find_root():
    for start in (Path.cwd().resolve(), Path(__file__).resolve().parent):
        for folder in (start, *start.parents):
            if (folder / MARKETPLACE).is_file():
                return folder
    return None


def load_json(path, report, where):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error(where, f"missing file {path.name}")
    except json.JSONDecodeError as exc:
        report.error(where, f"invalid JSON at line {exc.lineno}: {exc.msg}")
    return None


def check_relative(value, report, where, field):
    """Paths must be relative and, per the Codex docs, start with ./"""
    if not isinstance(value, str) or not value:
        report.error(where, f"`{field}` is missing or not a string")
        return False
    if value.startswith(("/", "\\")) or re.match(r"^[A-Za-z]:", value):
        report.error(where, f"`{field}` is an absolute path ({value}); use a path starting with ./")
        return False
    if not value.startswith("./"):
        report.warn(where, f"`{field}` should start with ./ ({value})")
    return True


def frontmatter(text):
    match = re.match(r"^---\n(.*?)\n---", text.replace("\r\n", "\n"), re.S)
    if not match:
        return None
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep:
            fields[key.strip()] = value.strip().strip("\"'")
    return fields


def yaml_value(text, key):
    match = re.search(rf"^\s*{re.escape(key)}:\s*(.+?)\s*$", text, re.M)
    return match.group(1).strip("\"'") if match else None


def find_skills(skills_dir, report, where):
    if (skills_dir / "SKILL.md").is_file():
        return [skills_dir], False
    skills = []
    for child in sorted(p for p in skills_dir.iterdir() if p.is_dir()):
        if (child / "SKILL.md").is_file():
            skills.append(child)
        else:
            report.warn(where, f"folder `{child.name}` in the skills folder has no SKILL.md")
    return skills, True


def check_skill(skill_dir, standard_layout, report, root):
    where = skill_dir.relative_to(root).as_posix()
    fields = frontmatter((skill_dir / "SKILL.md").read_text(encoding="utf-8"))
    if fields is None:
        report.error(where, "SKILL.md has no frontmatter (--- name/description ---)")
        return
    name = fields.get("name")
    for key in ("name", "description"):
        if not fields.get(key):
            report.error(where, f"SKILL.md frontmatter is missing `{key}`")
    if name and standard_layout and name != skill_dir.name:
        report.warn(where, f"SKILL.md name `{name}` doesn't match its folder name `{skill_dir.name}`")

    yaml_path = skill_dir / "agents" / "openai.yaml"
    if not yaml_path.is_file():
        return
    text = yaml_path.read_text(encoding="utf-8")
    for key in ("icon_small", "icon_large"):
        value = yaml_value(text, key)
        if value and check_relative(value, report, f"{where}/agents/openai.yaml", key):
            # Icon paths resolve from the skill folder (confirmed in the ChatGPT app).
            if not (skill_dir / value).is_file():
                report.error(f"{where}/agents/openai.yaml", f"`{key}` points to a missing file ({value})")
    prompt = yaml_value(text, "default_prompt")
    if name and prompt and f"${name}" not in prompt:
        report.warn(f"{where}/agents/openai.yaml", f"default_prompt doesn't mention ${name}")


def check_skill_paths(skill_dir, report, root):
    """Flag absolute and home-folder paths in every text file in a skill."""
    for path in sorted(p for p in skill_dir.rglob("*") if p.is_file()):
        data = path.read_bytes()
        if b"\0" in data:
            continue  # binary file, such as a PNG
        try:
            text = data.decode("utf-8")
        except UnicodeDecodeError:
            continue
        where = path.relative_to(root).as_posix()
        for number, line in enumerate(text.splitlines(), start=1):
            for label, pattern in ABSOLUTE_PATHS:
                for match in pattern.finditer(line):
                    found = match.group(0).rstrip(".,;:!?")  # drop sentence punctuation
                    report.error(f"{where}:{number}",
                                 f"{label} `{found}`; skills must use paths relative to the skill folder")
            for match in HOME_PATH.finditer(line):
                found = match.group(0).rstrip(".,;:!?")
                report.warn(f"{where}:{number}",
                            f"home-folder path `{found}` only works on machines laid out like yours")


def check_plugin(entry, index, report, root):
    name = entry.get("name") if isinstance(entry, dict) else None
    where = f"marketplace.json plugins[{index}]" + (f" ({name})" if name else "")
    if not name:
        report.error(where, "entry has no `name`")
        return None
    source = entry.get("source") or {}
    if source.get("source") != "local":
        report.warn(where, "source isn't local, so its files weren't checked")
        return None
    path = source.get("path")
    if not check_relative(path, report, where, "source.path"):
        return None
    plugin_dir = (root / path).resolve()
    if not plugin_dir.is_dir():
        report.error(where, f"source.path points to a missing folder ({path})")
        return None

    manifest_where = f"{plugin_dir.relative_to(root).as_posix()}/.codex-plugin/plugin.json"
    manifest = load_json(plugin_dir / ".codex-plugin" / "plugin.json", report, manifest_where)
    if manifest is None:
        return plugin_dir
    report.counts["plugins"] += 1
    if manifest.get("name") != name:
        report.error(manifest_where, f"name `{manifest.get('name')}` doesn't match marketplace entry `{name}`")
    if not manifest.get("version"):
        report.warn(manifest_where, "no `version`")
    interface = manifest.get("interface") or {}
    if not interface.get("displayName"):
        report.warn(manifest_where, "no `interface.displayName`")
    if entry.get("category") and interface.get("category") and entry["category"] != interface["category"]:
        report.warn(manifest_where, f"category `{interface['category']}` differs from marketplace `{entry['category']}`")

    for key in ("composerIcon", "logo"):
        value = interface.get(key)
        if value and check_relative(value, report, manifest_where, f"interface.{key}"):
            if not (plugin_dir / value).is_file():
                report.error(manifest_where, f"`interface.{key}` points to a missing file ({value})")

    skills_path = manifest.get("skills")
    if not check_relative(skills_path, report, manifest_where, "skills"):
        return plugin_dir
    skills_dir = plugin_dir / skills_path
    if not skills_dir.is_dir():
        report.error(manifest_where, f"`skills` points to a missing folder ({skills_path})")
        return plugin_dir
    skills, standard_layout = find_skills(skills_dir, report, manifest_where)
    if not skills:
        report.error(manifest_where, f"no SKILL.md found in {skills_path}")
    for skill_dir in skills:
        report.counts["skills"] += 1
        check_skill(skill_dir, standard_layout, report, root)
        check_skill_paths(skill_dir, report, root)
    return plugin_dir


def slug(heading):
    text = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return text.replace(" ", "-")


def strip_code(text):
    return re.sub(r"```.*?```", "", text, flags=re.S)


def check_markdown_links(report, root):
    link = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)|<img[^>]*\bsrc=\"([^\"]+)\"")
    heading = re.compile(r"^#{1,6}\s+(.*)$", re.M)
    anchors = {}

    def anchors_for(path):
        if path not in anchors:
            anchors[path] = {slug(h) for h in heading.findall(strip_code(path.read_text(encoding="utf-8")))}
        return anchors[path]

    for readme in sorted(root.rglob("*.md")):
        if ".git" in readme.relative_to(root).parts:
            continue
        where = readme.relative_to(root).as_posix()
        for match in link.finditer(strip_code(readme.read_text(encoding="utf-8"))):
            target = match.group(1) or match.group(2)
            if re.match(r"^[a-z][a-z0-9+.-]*:", target, re.I):
                continue  # http:, https:, mailto:
            report.counts["links"] += 1
            path, _, anchor = target.partition("#")
            dest = (readme.parent / path).resolve() if path else readme
            if not dest.exists():
                report.error(where, f"broken link {target}")
            elif anchor and (dest.is_dir() or anchor not in anchors_for(dest)):
                report.error(where, f"link {target} points to a heading that doesn't exist")


def main():
    root = find_root()
    if root is None:
        print(f"Couldn't find {MARKETPLACE.as_posix()}. Run this from inside the repo.")
        return 1
    report = Report()
    marketplace = load_json(root / MARKETPLACE, report, MARKETPLACE.as_posix())

    listed = set()
    if marketplace is not None:
        entries = marketplace.get("plugins")
        if not isinstance(entries, list) or not entries:
            report.error(MARKETPLACE.as_posix(), "`plugins` is missing or empty")
            entries = []
        names = [e.get("name") for e in entries if isinstance(e, dict)]
        for dup in sorted({n for n in names if n and names.count(n) > 1}):
            report.error(MARKETPLACE.as_posix(), f"plugin name `{dup}` is listed more than once")
        seen = set()
        for index, entry in enumerate(entries):
            name = entry.get("name") if isinstance(entry, dict) else None
            if name and name in seen:
                continue  # already reported as a duplicate; don't check it twice
            seen.add(name)
            plugin_dir = check_plugin(entry, index, report, root)
            if plugin_dir:
                listed.add(plugin_dir)

    for manifest in sorted((root / PLUGINS_DIR).rglob(".codex-plugin/plugin.json")):
        plugin_dir = manifest.parent.parent.resolve()
        if plugin_dir not in listed:
            report.warn(plugin_dir.relative_to(root).as_posix(),
                        "has a plugin.json but isn't listed in marketplace.json, so it can't be installed")

    check_markdown_links(report, root)

    c = report.counts
    print(f"Checked {c['plugins']} plugins, {c['skills']} skills, {c['links']} Markdown links.")
    for title, items in (("Errors", report.errors), ("Warnings", report.warnings)):
        if items:
            print(f"\n{title} ({len(items)}):")
            for item in items:
                print(f"  - {item}")
    print("\nResult: " + ("FAIL" if report.errors else "PASS"))
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
