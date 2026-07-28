# App won't start after deleting a profile

You most likely deleted the only profile there was, which makes the app crash on
startup. You can recreate a default profile by running the command for your
platform in a terminal, then restarting the app.

## macOS / Linux

Run in Terminal:

```
mkdir -p ~/.zotero-llm/profiles/default/chroma && echo '{"id":"default","name":"Default Profile","description":"","createdAt":"'$(date -u +"%Y-%m-%dT%H:%M:%S")'Z","updatedAt":"'$(date -u +"%Y-%m-%dT%H:%M:%S")'Z","version":"1.0"}' > ~/.zotero-llm/profiles/default/profile.json && echo '{}' > ~/.zotero-llm/profiles/default/settings.json && echo '{"sessions":{},"currentSessionId":null}' > ~/.zotero-llm/profiles/default/sessions.json && echo '{"activeProfileId":"default"}' > ~/.zotero-llm/active_profile.json
```

## Windows

Open PowerShell (press **Win+X** and select "Windows PowerShell"), then run:

```
New-Item -ItemType Directory -Force -Path "$env:USERPROFILE\.zotero-llm\profiles\default\chroma" | Out-Null; $timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ss") + "Z"; Set-Content -Path "$env:USERPROFILE\.zotero-llm\profiles\default\profile.json" -Value "{`"id`":`"default`",`"name`":`"Default Profile`",`"description`":`"`",`"createdAt`":`"$timestamp`",`"updatedAt`":`"$timestamp`",`"version`":`"1.0`"}"; Set-Content -Path "$env:USERPROFILE\.zotero-llm\profiles\default\settings.json" -Value "{}"; Set-Content -Path "$env:USERPROFILE\.zotero-llm\profiles\default\sessions.json" -Value "{`"sessions`":{},`"currentSessionId`":null}"; Set-Content -Path "$env:USERPROFILE\.zotero-llm\active_profile.json" -Value "{`"activeProfileId`":`"default`"}"
```

After running the command for your platform, restart the application. To avoid
this in future, keep at least one profile — see [Profiles](./profiles.html).
