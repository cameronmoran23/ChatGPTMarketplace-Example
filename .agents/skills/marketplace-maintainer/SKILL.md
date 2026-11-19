---
name: marketplace-maintainer
description: "Add, change, rename, or remove plugins and skills in this repo's Codex plugin marketplace, keep marketplace.json, plugin manifests, and READMEs in sync, then run the repo check. Use for any change under plugins/ or .agents/plugins/."
---

# Marketplace Maintainer

Make changes to this repo's plugin marketplace without leaving anything out of sync, then check the result.

## How the repo is organized

`.agents/plugins/marketplace.json` lists every installable plugin. Each entry's `source.path` points at a folder containing `.codex-plugin/plugin.json`. The marketplace's own `name` is `example-marketplace`.

The `plugins/` folder uses four layouts, and each one is a stop on the README tour:

| Layout | Example | Plugin folder | Marketplace entries |
|---|---|---|---|
| One plugin per department | Global, Finance | `plugins/<Dept>/` | One per department |
| One plugin per team | IT | `plugins/<Dept>/<Team>_Team/` | One per team; the department folder isn't a plugin |
| One plugin per skill | HR | `plugins/<Dept>/skills/<skill>/` | One per skill |
| Assets | Finance | Any of the above, plus `assets/` folders | No change |

Skill folders come in two shapes, and Codex loads both:

- **Standard:** `plugin.json` has `"skills": "./skills/"`, and each skill is `skills/<skill-name>/SKILL.md`.
- **Single-skill (HR):** `plugin.json` has `"skills": "./skill/"`, and `SKILL.md` sits directly in `skill/`.

## Rules

- Plugin and skill names are lowercase with hyphens. A marketplace entry's `name` must equal the `name` in that plugin's `plugin.json`.
- Paths are relative and start with `./`:
  - `source.path` in `marketplace.json` is relative to the repo root.
  - Paths in `plugin.json` (`skills`, `interface.composerIcon`, `interface.logo`) are relative to the plugin folder.
  - `icon_small` and `icon_large` in a skill's `agents/openai.yaml` are relative to the skill folder, not the `agents/` folder.
- Nothing inside a skill folder may contain an absolute path, in any file (`SKILL.md`, `agents/openai.yaml`, templates, scripts, references). That covers drive paths like `C:\...`, network paths like `\\server\share\...`, and system paths like `/Users/...` or `/home/...`. They only exist on the author's machine, so the skill breaks for everyone else. Refer to the skill's own files with paths relative to the skill folder, such as `assets/template.md`.
  - The check reports absolute paths as errors.
  - It reports home-folder paths (`~/`, `$HOME`, `%USERPROFILE%`) as warnings. Keep one only if the skill really needs a file in the user's home folder, and say why.
- Every skill has:
  - a `SKILL.md` whose frontmatter includes `name` and `description`;
  - an `agents/openai.yaml` with `display_name`, `short_description`, a `default_prompt` that mentions `$<skill-name>`, and `policy.allow_implicit_invocation`.
- Copy the format of an existing file of the same kind instead of inventing fields.
- HR plugins' `interface.displayName` starts with `HR - `.
- JSON allows no comments and no trailing commas.
- Never edit files under `~/.codex/plugins/cache/`. They are installed copies and get replaced on reinstall.

## Workflows

### Add a skill to an existing plugin

1. Create `skills/<skill-name>/SKILL.md` and `skills/<skill-name>/agents/openai.yaml` in the plugin folder.
2. Add a row for the skill to the plugin folder's README skills table.
3. `marketplace.json` doesn't change.

### Add a plugin

1. Choose the layout (see the table above) and create the plugin folder.
2. Create `.codex-plugin/plugin.json` with `name`, `version`, `description`, `skills`, and `interface` (`displayName`, `shortDescription`, `developerName`, `category`).
3. Add at least one skill.
4. Add an entry to `marketplace.json` by copying an existing entry. Set `name`, `source.path`, and `category`.
5. Update the README tour:
   - Write a README in the new folder using the same format as the others: a breadcrumb line, a NOTE box saying what the stop shows, folder contents, a skills table, how it's installed, and a Previous/Next footer.
   - Add a row to the tour table in the root `README.md`. Update the comparison table if the plugin introduces a new department or layout.
   - Update the Previous/Next links on the stops before and after the new one so the chain stays unbroken.

### Rename a plugin or skill

- **Plugin:**
  1. Change `name` in `plugin.json` and in the marketplace entry together.
  2. Update every README that mentions it.
  3. Remove the copy installed under the old name: `codex plugin remove <old-name>@example-marketplace`.
- **Skill:** rename the folder, then update the `SKILL.md` `name`, the `$<name>` in `default_prompt`, and the README rows.

### Remove a plugin or skill

- **Plugin:**
  1. Delete its marketplace entry and its folder.
  2. Remove its row from the root README tour table and update the comparison table.
  3. Relink the Previous/Next links of the stops on either side.
  4. Uninstall it: `codex plugin remove <name>@example-marketplace`.
- **Skill:** delete its folder and its README rows. If it was the plugin's last skill, remove the plugin too.

### Add assets

- **Plugin icon and logo:** put PNG files in `<plugin>/assets/`. Set `interface.composerIcon`, `interface.logo`, and `interface.brandColor` in `plugin.json`.
- **Skill icons:** put files in `<skill>/assets/`. Set `icon_small`, `icon_large`, and `brand_color` in the skill's `agents/openai.yaml`, using `./assets/...` paths.
- **Templates and other resources:** put them in `<skill>/assets/`, then tell Codex in `SKILL.md` which file to use and when.

## After every change

1. From the repo root, run:
   ```
   python .agents/skills/marketplace-maintainer/scripts/validate.py
   ```
   Fix every error, then rerun until the result is PASS. Review any warnings and either fix them or say why they're acceptable.
2. To try the change in Codex, run `codex plugin add <plugin-name>@example-marketplace`, then start a new chat. The command works even if the plugin is already installed; it replaces the installed copy with the current repo files. Editing the repo alone does not update an installed plugin.
3. Report what changed, which files were touched, and the check result.
