[Tour home](../../README.md#tour) › **Stop 2: Finance**

<img src="assets/logo.png" alt="Finance plugin logo" width="96">

# Finance

> [!NOTE]
> **What this stop shows:** assets. Finance uses the same layout as [Global](../Global), plus image and template files. These give the plugin and each skill their own icons, and give one skill a template to fill in.

## Folder contents

```
Finance/
├── .codex-plugin/
│   └── plugin.json                  # References the plugin icon and logo
├── assets/
│   ├── icon.png                     # Plugin icon (128×128)
│   └── logo.png                     # Plugin logo (512×512)
└── skills/
    ├── finance-close-review/
    │   ├── SKILL.md
    │   ├── agents/openai.yaml       # References the skill icons
    │   └── assets/
    │       ├── small-logo.svg
    │       └── large-logo.png
    └── finance-expense-check/
        ├── SKILL.md                 # Tells Codex to use the report template
        ├── agents/openai.yaml
        └── assets/
            ├── small-logo.svg
            ├── large-logo.png
            └── exception-report-template.md
```

## Three ways this plugin uses assets

### 1. Plugin icon and logo

[`assets/`](assets) holds the images that represent the whole plugin. [`plugin.json`](.codex-plugin/plugin.json) points to them:

```json
"brandColor": "#0F766E",
"composerIcon": "./assets/icon.png",
"logo": "./assets/logo.png"
```

### 2. Skill icons

Each skill has its own `assets/` folder with a small and a large icon. The skill's `agents/openai.yaml` points to them:

```yaml
icon_small: "./assets/small-logo.svg"
icon_large: "./assets/large-logo.png"
brand_color: "#0F766E"
```

### 3. A template the skill fills in

[`exception-report-template.md`](skills/finance-expense-check/assets/exception-report-template.md) is a report layout. [`finance-expense-check/SKILL.md`](skills/finance-expense-check/SKILL.md) tells Codex to format its results using that template, so every expense review comes back in the same structure.

## Skills

| | Skill | What it does |
|---|---|---|
| <img src="skills/finance-close-review/assets/small-logo.svg" alt="" width="32"> | [`finance-close-review`](skills/finance-close-review/SKILL.md) | Reviews a month-end close package for missing items and explains variances. |
| <img src="skills/finance-expense-check/assets/small-logo.svg" alt="" width="32"> | [`finance-expense-check`](skills/finance-expense-check/SKILL.md) | Checks expense claims against a policy and reports exceptions using the template. |

## How it's installed

One entry in [`marketplace.json`](../../.agents/plugins/marketplace.json), named `finance`. Installing it adds both skills and their assets.

---

[‹ Previous: Global](../Global) · [Tour home](../../README.md#tour) · **[Next: IT, separate team plugins ›](../IT)**
