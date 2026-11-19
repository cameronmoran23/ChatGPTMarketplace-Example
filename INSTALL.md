[Tour home](README.md#tour) › **Install**

# Install

How to add this marketplace to Codex and install its plugins, in the ChatGPT desktop app or the Codex CLI.

## Add The Marketplace

The ChatGPT desktop app and the Codex CLI share their settings, so you only need to add the marketplace once. Run one of these:

- **From GitHub:**
  ```
  codex plugin marketplace add cameronmoran23/ChatGPTMarketplace-Example
  ```
- **From a local clone,** run inside the cloned folder:
  ```
  codex plugin marketplace add .
  ```

To confirm it worked:

- **CLI:** `codex plugin marketplace list` should list `example-marketplace`.
- **Desktop app:** restart it, then open **Plugins** › **Personal**. Example Marketplace should appear.

The desktop app also reads `.agents/plugins/marketplace.json` from whichever repo you open as your project. With a local clone open, the marketplace appears even without the command.

To pick up new commits after adding from GitHub, run `codex plugin marketplace upgrade`.

## Install Plugins

Each plugin installs separately. Use the name in the second column with the CLI:

| Plugin | Name |
|---|---|
| Finance | `finance` |
| Global | `global` |
| IT Development | `it-development` |
| IT QA | `it-qa` |
| HR - Interview Plan | `hr-interview-plan` |
| HR - Job Description Draft | `hr-job-description` |

### ChatGPT Desktop App

1. Open **Plugins** › **Personal** and find **Example Marketplace**.
2. Select **+** next to a plugin. Installed plugins show a **…** menu instead and appear under **Installed** in the sidebar.
3. Start a new chat. Type `$` to see the plugin's skills.

### Codex CLI

1. Install a plugin by name, repeating for each plugin you want:
   ```
   codex plugin add finance@example-marketplace
   ```
2. Start a new `codex` session. Type `$` to see the plugin's skills.

To browse instead, run `codex` and type `/plugins`, then use ← and → to reach the **Example Marketplace** tab. **Tab** turns an installed plugin on or off, and **Ctrl+R** removes it.

## Uninstall Plugins

- **Desktop app:** open the plugin and select **Uninstall plugin**.
- **CLI:** run `codex plugin remove finance@example-marketplace`.

---

[‹ Previous: Showcase](README.md#showcase) · [Tour home](README.md#tour) · **[Next: Global, the basic layout ›](plugins/Global)**
