# ChatGPTMarketplace-Example

An example Codex plugin marketplace. It packages skills four different ways, so you can compare the layouts and pick the right one for your own teams.

## Take the tour

Click a stop to open its folder. GitHub shows the folder's README below the file list, and every README ends with links to the previous and next stops.

| Stop | Folder | What it shows |
|---|---|---|
| Start | [The marketplace file](#marketplace-file-agentspluginsmarketplacejson) | The catalogue of every plugin Codex can install. Described below. |
| 1 | [Global](plugins/Global) | The basic layout: one plugin, a few skills, available to everyone. |
| 2 | [Finance](plugins/Finance) | Assets: icons for the plugin and each skill, plus a template a skill fills in. |
| 3 | [IT](plugins/IT) | Teams within one department, each with its own plugin. |
| 3a | [IT › Development_Team](plugins/IT/Development_Team) | One team's plugin. |
| 3b | [IT › QA_Team](plugins/IT/QA_Team) | A second team's plugin in the same department. |
| 4 | [HR](plugins/HR) | One plugin per skill, so people install skills individually. |
| 4a | [HR › hr-interview-plan](plugins/HR/skills/hr-interview-plan) | A plugin containing a single skill. |
| 4b | [HR › hr-job-description](plugins/HR/skills/hr-job-description) | A second single-skill plugin. |

**[Begin at stop 1: Global ›](plugins/Global)**

### The four layouts compared

| | [Global](plugins/Global) | [Finance](plugins/Finance) | [IT](plugins/IT) | [HR](plugins/HR) |
|---|---|---|---|---|
| Plugins in the folder | 1 | 1 | 1 per team | 1 per skill |
| Marketplace entries | `global` | `finance` | `it-development`, `it-qa` | `hr-interview-plan`, `hr-job-description` |
| Installing one entry gives you | Every Global skill | Every Finance skill, with icons and templates | One team's skills | One skill |

## Making changes

Use the **marketplace-maintainer** skill for any change to plugins, skills, or the marketplace. It lists every file the change affects, including these READMEs, then checks the repo.

- **Codex:** type `$marketplace-maintainer` followed by the change, for example `$marketplace-maintainer add a Legal plugin with a contract-review skill`.
- **Claude Code:** type `/marketplace-maintainer` followed by the change.
- **Check only:** run `python .agents/skills/marketplace-maintainer/scripts/validate.py` from the repo root.
- **Try a change in Codex:** run `codex plugin add <plugin-name>@example-marketplace`, then start a new chat. Editing the repo doesn't update an installed plugin until you run this.

The skill lives in [`.agents/skills/marketplace-maintainer`](.agents/skills/marketplace-maintainer). The Claude Code copy in [`.claude/skills/marketplace-maintainer`](.claude/skills/marketplace-maintainer) points to the same instructions.

## Marketplace File: `.agents/plugins/marketplace.json`

### Description

`marketplace.json` lists the plugins in this repository. Codex reads it to show which plugins exist, where each one lives, and how it can be installed.

### Purpose

A plugin can only be installed if it appears in this file. Each team or department plugin gets its own entry, so people install only the plugins they need. For example, the IT Development and QA teams each have their own entry instead of sharing one IT entry.

### Structure

```json
{
  "name": "example-marketplace",
  "interface": {
    "displayName": "Example Marketplace"
  },
  "plugins": [
    {
      "name": "it-qa",
      "source": {
        "source": "local",
        "path": "./plugins/IT/QA_Team"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "IT"
    }
  ]
}
```

| Field | Meaning |
|---|---|
| `name` (top level) | The marketplace's ID. |
| `interface.displayName` | The marketplace name people see. |
| `plugins[].name` | The plugin's ID. Must match `name` in that plugin's `.codex-plugin/plugin.json`. |
| `plugins[].source.path` | The plugin folder, relative to the repository root. That folder must contain `.codex-plugin/plugin.json`. |
| `plugins[].policy.installation` | Whether people can install the plugin. `AVAILABLE` means anyone can install it. |
| `plugins[].policy.authentication` | When sign-in is requested. `ON_INSTALL` asks when the plugin is installed. |
| `plugins[].category` | The group the plugin is listed under, such as `IT` or `Finance`. |

### Updates

**Add a plugin**

1. Create the plugin folder with a `.codex-plugin/plugin.json` and a `skills/<skill-name>/SKILL.md` for each skill.
2. Add an entry to the `plugins` array. Set `name` to the plugin's `name` and `source.path` to the plugin folder.
3. Check that the file is still valid JSON. JSON doesn't allow comments or trailing commas.

**Change a plugin**

- **Plugin moved:** update `source.path`.
- **Plugin renamed:** update `name` here and in the plugin's `plugin.json`.
- **Edits inside the plugin folder:** skills, descriptions and other content changes don't require changes to this file.

**Remove a plugin**

- Delete its entry from the `plugins` array. Removing the entry stops the plugin being offered even if its folder is still in the repository.

## Tour complete

You've seen all four layouts. To choose one for a new group of skills:

- **Everyone needs the same skills:** use the [Global](plugins/Global) layout.
- **You want icons or templates:** add assets as [Finance](plugins/Finance) does. This works with any layout.
- **A department has distinct teams:** give each team its own plugin, as [IT](plugins/IT) does.
- **People need to pick individual skills:** make each skill its own plugin, as [HR](plugins/HR) does.

Then add the plugin to the marketplace by following [Updates](#updates).

[↑ Back to the tour](#take-the-tour)
