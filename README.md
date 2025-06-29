# House Pricing API

## Background
This is a FastAPI application that hosts machine learning models for inference.  It is not a production application and is intended as an exploratory project to research vibe-coding, GitHub Copilot, and architectural improvements.

Executing the application:

```bash
# Assumes virtualenv under .venv, initialized by uv
source .venv/bin/activate
# Directory must exist, future improvement is create if it doesn't exist.
PROMETHEUS_MULTIPROC_DIR=/tmp/prom_metrics uvicorn app.main:app --reload
```

Testing the application

```bash
curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8000/v1/predict -d @tests/data/sample-data.json
```

Executing unit tests:

```bash
uv run pytest
```