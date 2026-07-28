# Privacy & Data Controls

RAG Assistant is designed so you decide how much, if anything, leaves your
machine. Indexing runs on your own CPU and everything is stored locally; retrieval
happens on your device before any LLM is called.

## Local by default

If you use a local model via [Ollama or LM Studio](./providers.html), **nothing
leaves your machine at all** — your PDFs, your queries, and the generated answers
stay on your computer.

## When you use a cloud provider

If you choose a cloud provider (OpenAI, Anthropic, Google, Mistral, Groq,
OpenRouter), the only data sent to its API is:

- your query,
- the **10–12 text chunks** retrieved from your library for that query, and
- earlier responses from the same chat session (for follow-up context).

Your full library is never uploaded — only the passages retrieved for the current
question.

## Shielding parts of your library

If you use a cloud model but want to keep some material off it, you can exclude
whole Zotero **collections and tags** from the index entirely. Excluded items are
never embedded, so they can never be retrieved or sent to a third-party provider.
See [Indexing Your Library](./indexing.html) for how to set exclusions.

## Where your data lives

Everything is stored locally, per [profile](./profiles.html):

```
~/.zotero-llm/profiles/<profile>/
├── profile.json    metadata
├── settings.json   settings and API keys
├── sessions.json   chat history
└── chroma/         vector database (embeddings)
```

- **API keys** are stored locally in `settings.json`, masked in the UI, and never
  logged.
- **Embeddings and chat history** never leave your machine.
- The app **reads** your Zotero database (`zotero.sqlite`) but does not modify it.

## No telemetry

The app does not collect analytics or send usage data. Your only outbound traffic
is to the LLM provider you actively choose to use.
