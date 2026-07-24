FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt pyproject.toml README.md ./
COPY pharma_genai ./pharma_genai
COPY app ./app
RUN pip install --no-cache-dir -r requirements.txt && pip install --no-cache-dir -e .
EXPOSE 8501 8000
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.address=0.0.0.0"]
