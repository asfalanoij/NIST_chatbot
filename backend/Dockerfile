FROM python:3.12-slim

WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Download FAISS index from GitHub Release
RUN mkdir -p index_kms && \
    curl -sL https://github.com/asfalanoij/NIST_chatbot/releases/download/v2.0.0/index.faiss -o index_kms/index.faiss && \
    curl -sL https://github.com/asfalanoij/NIST_chatbot/releases/download/v2.0.0/index.pkl -o index_kms/index.pkl

EXPOSE ${PORT:-5050}

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5050", "--workers", "2", "--timeout", "120"]
