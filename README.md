## Skin disease classification (Streamlit)

This is a Streamlit app (`app.py`) that analyzes an uploaded skin image + user symptoms and uses the OpenAI API to generate a likely condition, causes, precautions, and suggested medications.

### Run locally

- **Install**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- **Set env**

Copy `env.template` to `.env` and fill in your key:

```bash
cp env.template .env
```

- **Start**

```bash
streamlit run app.py
```

### Deploy (recommended): Streamlit Community Cloud

Vercel is not a good fit for hosting Streamlit itself (Streamlit needs a long-running server). The simplest deployment is:

- **Deploy Streamlit**: Streamlit Community Cloud
  - App file: `app.py`
  - Python deps: `requirements.txt`
  - Secret: set `OPENAI_API_KEY` in the Streamlit Cloud app settings

After deploy you’ll get a URL like:
- `https://your-app-name.streamlit.app`

### Deploy on Vercel (as a wrapper)

This repo includes a tiny Vercel serverless endpoint that serves an HTML page and **embeds your Streamlit app in an iframe**.

- **What Vercel runs**: `api/index.py` (simple HTML)
- **What Vercel does NOT run**: Streamlit

Steps:

- **Import to Vercel**: create a new Vercel project from this repo
- **Set env var in Vercel**:
  - `STREAMLIT_APP_URL=https://your-app-name.streamlit.app`
- **Deploy**

When you open your Vercel URL, it will show the Streamlit app inside the page.
