# Installation

RAG Assistant is available for macOS, Windows, and Linux. Check
[Platform Support](./platform-support.html) for system requirements first.

## macOS

Install via Homebrew:

```
brew tap Quiet-Signals-Lab/rag-assistant-for-zotero
brew install --cask rag-assistant-for-zotero
```

macOS builds are signed and notarized, so they launch without extra steps.
Apple Silicon (M1/M2/M3 or newer) only — there are no Intel builds.

## Windows

Install via winget:

```
winget install aahepburn.RAGAssistantForZotero
```

Windows builds are not code-signed yet, so SmartScreen may show a warning on
first launch — choose **More info → Run anyway**.

## Linux

Download the `.deb` package from the
[GitHub Releases page](https://github.com/Quiet-Signals-Lab/RAG-Assistant-for-Zotero/releases)
and install it. Python and all dependencies are bundled.

## Next steps

You'll also need the Zotero desktop client installed with your library synced —
the app reads your local `zotero.sqlite` database. Then see
[Indexing Your Library](./indexing.html) to build your first index.
