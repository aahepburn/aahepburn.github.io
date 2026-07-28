# Platform Support

## macOS

macOS 11 Big Sur or later. Apple Silicon (M1/M2/M3) is recommended — Intel builds
may have limited support due to PyTorch compatibility. Builds are signed and
notarized.

## Windows

Windows 10 or later (64-bit). Install via `winget` or the installer from
[Releases](https://github.com/Quiet-Signals-Lab/RAG-Assistant-for-Zotero/releases).
Builds are not code-signed yet, so SmartScreen may warn on first launch.

## Linux

Debian/Ubuntu-based distributions (Ubuntu 18.04+, Debian 10+). Install the `.deb`
package; Python and all dependencies are bundled.

## Zotero

All platforms require the Zotero desktop client, installed with your library
synced. The app reads your local `zotero.sqlite` database for PDFs and metadata.
Zotero must be **fully closed** while indexing — see
[The app won't index my library](./wont-index.html).
