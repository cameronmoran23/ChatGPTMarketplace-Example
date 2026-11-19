---
name: marketplace-maintainer
description: "Add, change, rename, or remove plugins and skills in this repo's Codex plugin marketplace, keep marketplace.json, plugin manifests, and READMEs in sync, then run the repo check. Use for any change under plugins/ or .agents/plugins/."
---

# Marketplace Maintainer

This skill is shared with Codex, and its instructions live in one place so the two copies can't drift apart.

Before making any change, read `.agents/skills/marketplace-maintainer/SKILL.md` in full and follow it. When the change is done, run its check from the repo root:

```
python .agents/skills/marketplace-maintainer/scripts/validate.py
```
