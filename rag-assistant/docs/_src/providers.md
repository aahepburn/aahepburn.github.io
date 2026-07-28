# LLM Providers & API Keys

RAG Assistant supports multiple LLM providers through a provider-agnostic
architecture. Run a local model for free and private, or connect a cloud model
for more capability.

- **Ollama** (local, free)
- **LM Studio** (local, free)
- **OpenAI** (GPT models)
- **Anthropic** (Claude)
- **Mistral** (Mistral Large, Mixtral)
- **Google** (Gemini)
- **Groq** (fast Llama)
- **OpenRouter** (unified access to many models)

## Configure in the app

1. Open the Settings page.
2. Enable the providers you want.
3. Add API keys (not needed for local providers).
4. Test the connections.
5. Select the active provider and model.
6. Save and start asking questions.

You can enable multiple providers at once and switch the active one anytime.
Retrieval limits scale automatically to the active model's context window.

## Getting API keys

Local providers (Ollama, LM Studio) need no key. For cloud providers:

- **OpenAI** — <https://platform.openai.com/api-keys>
- **Anthropic** — <https://console.anthropic.com/account/keys>
- **Google (Gemini)** — <https://makersuite.google.com/app/apikey>
- **Mistral / Groq / OpenRouter** — create a key in each provider's console.

Create a key, copy it, and paste it into Settings.

## Security

- API keys are masked in the UI.
- Keys are stored locally in `~/.zotero-llm/profiles/<profile>/settings.json`.
- Keys are never logged or exposed.
- Each provider is validated independently.

See [Privacy & Data Controls](./privacy.html) for what is and isn't sent to
providers.
