# The app won't index my library

Make sure your **Zotero client is completely closed** before you start indexing.
The app reads Zotero's local SQLite database (`zotero.sqlite`) directly, and
Zotero locks that file while it's open — so if Zotero is running, the app can't
access your library and indexing will fail.

Quit Zotero fully (not just close the window), then start indexing again. See
[Indexing Your Library](./indexing.html) for how indexing works.
