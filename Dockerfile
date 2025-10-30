# Dockerfile
FROM python:3.11-slim

# Runtime environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBUG=0 \
    ENVIRONMENT=production \
    ALLOWED_HOSTS=dim-gggl.com,www.dim-gggl.com

WORKDIR /app

# System dependencies (only what's needed at runtime)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy all requirement files to leverage Docker layer caching
COPY requirements/ ./requirements/
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements/prod.txt

# Copy project code
COPY . .

# Collect static files at build time (does not require DB)
# Ensure source static directory exists to silence W004 in production
RUN mkdir -p static && python manage.py collectstatic --noinput

# Expose default port (Railway will provide $PORT)
EXPOSE 8000

# Start: run migrations then Gunicorn binding on $PORT (fallback 8000)
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py load_projects ./projects.json && gunicorn --bind 0.0.0.0:${PORT:-8000} portfolio_dimitri.wsgi:application"]