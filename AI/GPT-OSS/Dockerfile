FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Build deps for vLLM
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential cmake ninja-build python3-dev pkg-config \
 && rm -rf /var/lib/apt/lists/*

# CPU PyTorch
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch torchvision torchaudio

# vLLM (CPU build from source)
RUN git clone --depth=1 https://github.com/vllm-project/vllm.git
WORKDIR /app/vllm
ENV VLLM_TARGET_DEVICE=cpu
RUN pip install --no-cache-dir -v .

# Back to app dir
WORKDIR /app
ENV PORT=8000

# Tip: mount a Railway volume at /root/.cache/huggingface to persist model weights
EXPOSE 8000
CMD ["python","-m","vllm.entrypoints.openai.api_server", "--model","openai/gpt-oss-20b", "--host","0.0.0.0","--port","8000", "--device","cpu","--dtype","auto"]
