FROM python:3.11-slim-bookworm
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser
COPY requirements.txt requirements-api.txt pyproject.toml ./
COPY src ./src
RUN python -m pip install --upgrade pip && pip install -r requirements.txt -r requirements-api.txt && pip install --no-deps .
COPY --chown=appuser:appgroup . .
USER appuser
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health')"
CMD ["uvicorn","enterprise_ai_agent.api.main:app","--host","0.0.0.0","--port","8000"]
