cd invest-easy-webapi
# uv run fastapi dev app/app.py
uv run uvicorn app.app:app --reload --reload-dir app --host 0.0.0.0 --port 8000