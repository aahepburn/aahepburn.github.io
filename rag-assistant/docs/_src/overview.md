# Overview

RAG Assistant for Zotero indexes the PDFs in your Zotero library and uses
retrieval-augmented generation to answer questions grounded in their content.
Every answer includes citations to the specific documents and page numbers it
drew from, so you can verify each claim instead of trusting an opaque summary.

It runs fully local with [Ollama or LM Studio](./providers.html) — your library
never leaves your machine — or connects to cloud models when you prefer.

## What it does

- **Hybrid search** — dense semantic embeddings combined with BM25 keyword search
  (merged by Reciprocal Rank Fusion), then reranked by a cross-encoder. Captures
  both conceptual similarity and exact terminology.
- **Cited answers** — responses reference the documents and page numbers they use,
  with an Evidence Panel showing the exact passages.
- **Metadata filtering** — filter by year, tags, collections, authors, or item
  type, manually or by describing the constraint in natural language.
- **Conversational follow-ups** — pronouns and context are rewritten into
  standalone queries before retrieval.
- **[Multiple LLM providers](./providers.html)** — local or cloud, switchable
  anytime.
- **[Profiles](./profiles.html)** — separate workspaces per research project.

## How it works

PDFs are extracted with page-level granularity and split into ~800-character
chunks with 200-character overlap on sentence boundaries. Each chunk carries its
item ID, title, authors, year, tags, collections, item type, and page number.
Embeddings are generated with SentenceTransformers and stored in ChromaDB. See
[Indexing Your Library](./indexing.html) for the details.

The backend is FastAPI, the frontend React and TypeScript, packaged as an
Electron desktop app with automatic updates.

Ready to start? Head to [Installation](./installation.html).
