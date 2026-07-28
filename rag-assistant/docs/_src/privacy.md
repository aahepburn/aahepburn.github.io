# Privacy & Data Controls

RAG Assistant is designed so you decide how much, if anything, leaves your
machine. All indexing and processing happen locally.

## Local by default

If you use a local model via [Ollama or LM Studio](./providers.html), **nothing
leaves your machine at all** — your PDFs, your queries, and the generated answers
stay on your computer.

## When you use a cloud provider

If you choose a cloud provider (OpenAI, Anthropic, Google, Mistral, Groq,
OpenRouter), only your **query and the retrieved document chunks** are sent to
that provider's API to generate an answer. Your full library is never uploaded —
only the specific passages retrieved for the current question.

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
