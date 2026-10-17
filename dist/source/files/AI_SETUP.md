# Optional Groq or Grok connection

The published static demo uses local bilingual search. The included Python server can optionally use an external model to interpret free-form English/Finnish questions. **Groq and Grok are different services.** The attached Vestafy README used Groq.

Set these environment variables in your server environment (never in frontend code or committed files):

- `MICROBELOG_AI_PROVIDER`: `groq` or `xai`
- `MICROBELOG_AI_MODEL`: a currently available chat model ID from your provider
- `GROQ_API_KEY` for Groq, or `XAI_API_KEY` for xAI/Grok

Then run `python serve.py`. The server binds to localhost. No key is needed for local search.

`GET /api/ai/status` reports availability without exposing a key. `POST /api/ai/interpret` sends only the question and allowed vocabulary (species, location names/codes, antibiotics) to the configured provider. It does not send CSVs, patient history or database credentials. The model produces a canonical search query; MicrobeLog's deterministic engine computes the answer and applies the first-isolate and minimum-30 rules. Provider output never becomes SQL or code. Unsupported clinical requests remain unavailable. If no API is configured, local search continues. The UI identifies whether AI interpretation is enabled.

The Python server is a local development integration, not a public production API. The hosted static Site has no Python server and no configured external model. Deploy an authenticated server-side API before connecting an actual hospital system. External API execution has not been tested with a real key in this session.

Official API references:
https://console.groq.com/docs/api-reference
https://docs.x.ai/developers/rest-api-reference/inference/chat-completions
