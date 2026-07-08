# Dockerfile
FROM python:3.11-slim

# Runtime environment
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DEBUG=0 \
    ALLOWED_HOSTS=127.0.0.1,localhost,dim-gggl.com,www.dim-gggl.com

WORKDIR /app

# System dependencies (Node is only needed to build the React frontend)
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# Copy all requirement files to leverage Docker layer caching
COPY requirements/ ./requirements/
RUN python -m pip install --upgrade pip && \
    python -m pip install --no-cache-dir -r requirements/prod.txt

# Install frontend dependencies (cached layer as long as the lockfile is stable)
COPY frontend/package.json frontend/package-lock.json ./frontend/
RUN npm ci --prefix frontend

# Copy project code
COPY . .

# Build the React frontend into static/frontend/
RUN npm run build --prefix frontend

# Collect static files at build time (does not require DB)
# Use a dummy SECRET_KEY for collectstatic (it doesn't need the real one)
RUN SECRET_KEY=build-time-secret python manage.py collectstatic --noinput

# Expose default port (Railway will provide $PORT)
EXPOSE 8000



# Start: run migrations then Gunicorn binding on $PORT (fallback 8000)
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py load_projects ./projects.json && gunicorn --bind 0.0.0.0:${PORT:-8000} portfolio_dimitri.wsgi:application"]
