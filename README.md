# Student Activity Review

A minimal Streamlit prototype that sends an uploaded image to Gemini and returns
a structured, safety-constrained observation. Images remain in memory and this
application does not save them.

## Run locally

Requires Python 3.10 or newer.

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:GEMINI_API_KEY = "your-key"
streamlit run app.py
```

Get a demo API key from Google AI Studio. To use another currently supported
multimodal model, set `GEMINI_MODEL`; the default is `gemini-3.6-flash`.

## Streamlit Community Cloud

1. Push these files to a private GitHub repository.
2. Create a Streamlit app with `app.py` as the entry point.
3. Add `GEMINI_API_KEY = "your-key"` under the app's **Secrets** settings.

Use staged or synthetic images for this demo setup. Do not commit
`.streamlit/secrets.toml`.

## Cloud Run

The included `Dockerfile` listens on Cloud Run's `PORT` environment variable.
For an organizational pilot involving identifiable student images, replace the
AI Studio API-key client with organization-approved Vertex AI authentication,
then confirm retention, regional processing, access, consent, and privacy
requirements before deployment.

## Safeguards

- No identity or facial-recognition request
- No emotion, health, disability, intent, guilt, or protected-trait inference
- Conservative `uncertain` result when one image lacks context
- Structured Pydantic response schema
- 10 MB and JPG/PNG/WebP upload restrictions
- API key remains server-side
- Explicit human-review notice

This prototype does not log or persist uploaded image bytes. Hosting and model
providers may have their own processing policies, which must be reviewed before
using real student data.
