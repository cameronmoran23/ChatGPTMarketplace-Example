[Tour home](../../../../README.md#tour) › [HR](../../README.md) › **Stop 4a: Interview Plan**

# HR - Interview Plan

A plugin containing a single skill. Its marketplace entry is `hr-interview-plan`. Installing it adds this skill and nothing else from HR.

The skill builds a structured interview plan from role criteria. Each question maps to a job-related competency and comes with a short scoring guide.

| File | Purpose |
|---|---|
| [`.codex-plugin/plugin.json`](.codex-plugin/plugin.json) | Manifest for this skill alone. `skills` points at `./skill/`. |
| [`skill/SKILL.md`](skill/SKILL.md) | The skill instructions. |
| [`skill/agents/openai.yaml`](skill/agents/openai.yaml) | Display name and default prompt. |

---

[‹ Previous: HR](../../README.md) · [Tour home](../../../../README.md#tour) · **[Next: Job Description Draft ›](../hr-job-description)**
