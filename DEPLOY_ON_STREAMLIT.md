# Deploy RegOps Odyssey on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload every file and folder in this package to the repository root.
3. Go to https://share.streamlit.io and sign in with GitHub.
4. Click **Create app**.
5. Choose your repository and the `main` branch.
6. Set **Main file path** to `app.py`.
7. Click **Deploy**.

Optional environment variables can be entered in Advanced settings / Secrets:

```toml
CAREER_PASS_URL = "https://..."
CONSULTANT_LAB_URL = "https://..."
COHORT_URL = "https://..."
AI_API_URL = "https://..."
AI_API_KEY = "..."
AI_MODEL = "..."
```

Do not commit real API keys or payment credentials to GitHub.
