# Indexing Your Library

Indexing is what makes your library searchable: the app reads the PDFs attached
to your Zotero items, breaks them into passages, and builds embeddings it can
search later.

> **Close Zotero first.** The app reads your local `zotero.sqlite` database
> directly, and Zotero locks that file while it's open. If indexing won't start,
> see [The app won't index my library](./wont-index.html).

## How it works

- **Extraction** — PDFs are extracted with page-level granularity, so citations
  can point to the exact page.
- **Chunking** — text is split into roughly 800-character chunks with 200-character
  overlap, cut on sentence boundaries.
- **Metadata** — each chunk carries its item ID, title, authors, year, tags,
  collections, item type, and page number. This is what powers both metadata
  filtering and citations.
- **Storage** — embeddings are stored in a local ChromaDB database inside the
  active [profile](./profiles.html).

## Embedding models

Embeddings are generated with SentenceTransformers, downloaded automatically on
first use. Choose the model in Settings:

| Model | Best for |
|---|---|
| BGE-base (default) | Best overall quality |
| SPECTER | Scientific papers |
| MiniLM-L6 | Balanced speed/quality |
| MiniLM-L3 | Fastest |

Each model creates its own collection, so you can switch between models without
re-indexing if that model's index already exists.

## Re-indexing and updates

Initial indexing builds embeddings for every PDF and can take a while for large
libraries. Subsequent runs only process new or changed items. Only PDFs with
selectable text can be indexed — scanned documents need OCR first.

## Scope and exclusions

You can limit what gets indexed to specific collections, and exclude items you
don't want in the index, so a large library doesn't force you to embed
everything at once.
