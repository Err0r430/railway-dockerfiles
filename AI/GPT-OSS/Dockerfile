FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu torch torchvision torchaudio \
 && pip install --no-cache-dir vllm

# Force CPU backend
ENV VLLM_TARGET_DEVICE=cpu
ENV PORT=8000
CMD ["python3","-m","vllm.entrypoints.openai.api_server", "--model","openai/gpt-oss-20b", "--host","0.0.0.0","--port","8000","--device","cpu"]
