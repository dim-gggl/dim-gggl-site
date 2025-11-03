# Dockerfile
FROM python:3.11-slim

# Runtime environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBUG=0 \
    ALLOWED_HOSTS=127.0.0.1,localhost,dim-gggl.com,www.dim-gggl.com

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
# Use a dummy SECRET_KEY for collectstatic (it doesn't need the real one)
RUN python manage.py tailwind build && \
    SECRET_KEY=build-time-secret \ 
    python manage.py collectstatic --noinput && \
    python manage.py compress

# Expose default port (Railway will provide $PORT)
EXPOSE 8000



# Start: run migrations then Gunicorn binding on $PORT (fallback 8000)
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py load_projects ./projects.json && gunicorn --bind 0.0.0.0:${PORT:-8000} portfolio_dimitri.wsgi:application"]