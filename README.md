## Skin disease classification (Streamlit)

This is a Streamlit app (`app.py`) that analyzes an uploaded skin image + user symptoms and uses the OpenAI API to generate a likely condition, causes, precautions, and suggested medications.

### Run locally

- **Install**

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

- **Start**

```bash
streamlit run app.py
```

### Deploy (recommended): Streamlit Community Cloud

- **Deploy Streamlit**: Streamlit Community Cloud
  - App file: `app.py`
  - Python deps: `requirements.txt`
  - Secret: set `OPENAI_API_KEY` in the Streamlit Cloud app settings

After deploy you’ll get a URL like:
- `https://your-app-name.streamlit.app`
