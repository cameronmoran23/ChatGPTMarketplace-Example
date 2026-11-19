[Tour home](../../README.md#take-the-tour) › **Stop 4: HR**

# HR

> [!NOTE]
> **What this stop shows:** installing skills one at a time. Every HR skill is its own plugin with its own marketplace entry. Someone who only writes job descriptions installs only that skill. The trade-off is one manifest and one marketplace entry per skill.

## Folder contents

```
HR/
└── skills/
    ├── hr-interview-plan/            # Plugin: hr-interview-plan
    │   ├── .codex-plugin/plugin.json # Points skills at ./skill/
    │   └── skill/
    │       ├── SKILL.md
    │       └── agents/openai.yaml
    └── hr-job-description/           # Plugin: hr-job-description
        ├── .codex-plugin/plugin.json
        └── skill/
            ├── SKILL.md
            └── agents/openai.yaml
```

Compare this with [Global](../Global): there, one `plugin.json` covers every skill in `skills/`. Here, each skill folder has its own `plugin.json`.

## Skills

| Skill | Shown in the marketplace as | What it does |
|---|---|---|
| [`hr-interview-plan`](skills/hr-interview-plan) | HR - Interview Plan | Builds a structured interview plan from role criteria. |
| [`hr-job-description`](skills/hr-job-description) | HR - Job Description Draft | Drafts a clear job description from role requirements. |

Each plugin's `displayName` starts with "HR - ", so the separate entries still read as one group in the marketplace.

## How it's installed

[`marketplace.json`](../../.agents/plugins/marketplace.json) has one entry per skill, and each entry points directly at that skill's folder.

---

[‹ Previous stop: QA team](../IT/QA_Team) · **Next stop: [Interview Plan ›](skills/hr-interview-plan)**
