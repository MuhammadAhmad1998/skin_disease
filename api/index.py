import os
from http.server import BaseHTTPRequestHandler


HTML = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Skin Disease Classification</title>
    <style>
      html, body { height: 100%; margin: 0; }
      .bar {
        font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial;
        padding: 10px 14px;
        border-bottom: 1px solid #e5e7eb;
        background: #fff;
      }
      .bar code { background: #f3f4f6; padding: 2px 6px; border-radius: 6px; }
      iframe { width: 100%; height: calc(100% - 44px); border: 0; display: block; }
    </style>
  </head>
  <body>
    <div class="bar">
      This page is served by Vercel. The Streamlit app is embedded from: <code>{url}</code>
    </div>
    <iframe src="{url}" allow="clipboard-read; clipboard-write"></iframe>
  </body>
</html>
"""


MISSING = """<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Missing config</title>
    <style>
      body { font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial; padding: 24px; }
      code { background: #f3f4f6; padding: 2px 6px; border-radius: 6px; }
      pre { background: #0b1020; color: #e5e7eb; padding: 12px; border-radius: 10px; overflow: auto; }
    </style>
  </head>
  <body>
    <h2>Vercel wrapper is deployed, but the Streamlit URL is not configured.</h2>
    <p>Set the environment variable <code>STREAMLIT_APP_URL</code> in your Vercel project settings.</p>
    <p>Example:</p>
    <pre>STREAMLIT_APP_URL=https://your-app-name.streamlit.app</pre>
  </body>
</html>
"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = os.environ.get("STREAMLIT_APP_URL", "").strip()
        body = (HTML.format(url=url) if url else MISSING).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

