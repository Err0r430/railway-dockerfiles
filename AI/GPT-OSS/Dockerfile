FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir vllm

CMD ["vllm", "serve", "openai/gpt-oss-20b", "--host", "0.0.0.0", "--port", "8000", "--api-key", "${API_KEY}"]
