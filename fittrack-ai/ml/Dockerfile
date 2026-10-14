FROM python:3.12-slim
WORKDIR /app
COPY runtime-requirements.txt .
RUN pip install --no-cache-dir -r runtime-requirements.txt
COPY . ./ml
RUN python -m ml.download_baseline
RUN useradd --system --uid 10002 app
USER app
ENV MODEL_HOST=0.0.0.0
ENV MODEL_DIR=/app/ml/models/food101
EXPOSE 8090
CMD ["python", "-m", "ml.serve"]
