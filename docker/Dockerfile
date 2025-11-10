# =============================
# 1) Build stage
# =============================
FROM python:3.11-slim as builder

WORKDIR /app
RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =============================
# 2) Final runtime stage
# =============================
FROM python:3.11-slim
WORKDIR /app

# bring in installed packages from builder
COPY --from=builder /usr/local /usr/local

# copy your source code
COPY . .

# create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

