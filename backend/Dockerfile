FROM python:3.12-slim

WORKDIR /app

# Install system deps for psycopg2-binary
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# FAISS index: copy from local build context if present,
# otherwise must be mounted or built at runtime.
# To build: place index_kms/ in backend/ before `docker build`.

EXPOSE ${PORT:-5050}

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5050", "--workers", "2", "--timeout", "120"]
