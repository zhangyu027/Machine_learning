FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app/forecasting
ENV PORT=8080

COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY forecasting ./forecasting
COPY serving ./serving
COPY models ./models

RUN mkdir -p /app/outputs/forecasts /app/outputs/figures /app/outputs/metrics

EXPOSE 8080
CMD ["uvicorn", "serving.api.main:app", "--host", "0.0.0.0", "--port", "8080"]
