# app/main.py

import os
from app import create_app
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)