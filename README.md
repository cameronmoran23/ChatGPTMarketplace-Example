# ChatGPTMarketplace-Example

## Marketplace file: `.agents/plugins/marketplace.json`

### What it is

`marketplace.json` lists the plugins in this repository. Codex reads it to show which plugins exist, where each one lives, and how it can be installed.

### Why it exists

A plugin can only be installed if it appears in this file. Each team or department plugin gets its own entry, so people install only the plugins they need. For example, the IT Development, QA and Operations teams each have their own entry instead of sharing one IT entry.

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

### How to update it

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
