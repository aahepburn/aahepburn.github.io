# Profiles

Profiles let you maintain separate workspaces within RAG Assistant. Each profile
has its own:

- Settings (API keys, model preferences, etc.)
- Chat history and sessions
- Document embeddings (vector database)

Use one profile per research project to keep libraries, settings, and history
isolated.

## Creating a new profile

1. Open the Settings page (gear icon).
2. In the "Profile" section at the top, click **+ New**.
3. Enter a name (e.g. "Work", "Personal", "Research").
4. Click **Create**. The new profile starts with default settings.

## Switching profiles

1. Open the Settings page.
2. Select a different profile from the **Profile** dropdown.
3. Confirm the switch — this reloads the application.

**Important:** switching profiles reloads the app. Save any settings first, as
unsaved work will be lost.

## Managing profiles

- **View active profile** — shown in the dropdown.
- **Switch** — select from the dropdown and confirm the reload.
- **Delete** — you can't delete the active profile; switch to another first.

> **Careful:** if you delete the *only* profile, the app will fail to start. If
> that happens, see
> [App won't start after deleting a profile](./profile-wont-start.html).

## Data storage

All profile data is stored locally at `~/.zotero-llm/profiles/`. Each profile has
its own folder:

- `profile.json` — metadata (name, description, timestamps)
- `settings.json` — settings and API keys
- `sessions.json` — chat history
- `chroma/` — vector database for document embeddings

## Best practices

1. **Use descriptive names** (e.g. "Client-ProjectX", "Personal-Reading").
2. **Keep backups** of important profiles.
3. **Separate sensitive data** — different profiles for work and personal.
4. **Test changes** in a throwaway profile before major settings changes.

## Migration from single-profile setups

If you used the app before profiles existed, your settings, chat history, and
vector database are automatically migrated into a "default" profile. Everything
keeps working, and you can add more profiles as needed. No manual migration is
required.
