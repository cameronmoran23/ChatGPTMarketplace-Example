[Tour home](../../README.md#tour) › **Stop 3: IT**

# IT

> [!NOTE]
> **What this stop shows:** separate teams within one department. `IT/` isn't a plugin itself; it has no `.codex-plugin/` folder. Each team folder inside it is a complete plugin with its own marketplace entry. A developer installs only the Development skills, and a tester installs only the QA skills.

## Folder Contents

```
IT/
├── Development_Team/          # Plugin: it-development
│   ├── .codex-plugin/plugin.json
│   └── skills/
│       ├── dev-code-review/
│       └── dev-technical-design/
└── QA_Team/                   # Plugin: it-qa
    ├── .codex-plugin/plugin.json
    └── skills/
        ├── qa-bug-report/
        └── qa-test-plan/
```

## Teams

| Team | Marketplace entry | Skills |
|---|---|---|
| [Development_Team](Development_Team) | `it-development` | `dev-code-review`, `dev-technical-design` |
| [QA_Team](QA_Team) | `it-qa` | `qa-test-plan`, `qa-bug-report` |

## How It's Installed

[`marketplace.json`](../../.agents/plugins/marketplace.json) has one entry per team, and each entry points to that team's folder. Both entries use the category `IT`, so they're listed together in the marketplace but installed separately.

To add a team, create a folder with the same layout as a team folder, then add a marketplace entry for it.

---

[‹ Previous: Finance](../Finance) · [Tour home](../../README.md#tour) · **[Next: Development team ›](Development_Team)**
