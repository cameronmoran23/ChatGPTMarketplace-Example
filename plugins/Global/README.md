[Tour home](../../README.md#tour) › **Stop 1: Global**

# Global

> [!NOTE]
> **What this stop shows:** the basic layout. Global is one plugin with a general set of skills that anyone in the company can install. Every other stop on the tour is a variation on this layout.

## Folder Contents

```
Global/
├── .codex-plugin/
│   └── plugin.json            # The plugin manifest
└── skills/
    ├── file-organizer/
    │   ├── SKILL.md           # Instructions Codex follows
    │   └── agents/openai.yaml # Display name, description, default prompt
    └── meeting-notes-cleanup/
        ├── SKILL.md
        └── agents/openai.yaml
```

| File | Purpose |
|---|---|
| [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) | Names the plugin, sets its version and display details, and points `skills` at `./skills/`. |
| `skills/<skill>/SKILL.md` | The skill itself: a short description in the frontmatter, then the instructions Codex follows. |
| `skills/<skill>/agents/openai.yaml` | How the skill appears in Codex: display name, short description, default prompt, and whether Codex can use it without being asked. |

## Skills

| Skill | What it does |
|---|---|
| [`file-organizer`](skills/file-organizer/SKILL.md) | Proposes a folder structure and a sort plan for a set of files. |
| [`meeting-notes-cleanup`](skills/meeting-notes-cleanup/SKILL.md) | Turns rough meeting notes into organized minutes with decisions and actions. |

## How It's Installed

One entry in [`marketplace.json`](../../.agents/plugins/marketplace.json), named `global`. Installing it adds both skills.

---

[‹ Previous: Install](../../INSTALL.md) · [Tour home](../../README.md#tour) · **[Next: Finance, using assets ›](../Finance)**
