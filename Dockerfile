# Dockerfile
FROM python:3.11-slim

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Dépendances système (si besoin de pillow, psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY requirements/base.txt .
RUN pip install --no-cache-dir -r requirements/base.txt

# Copie du code
COPY . .

# Collecte des fichiers statiques
RUN python manage.py collectstatic --noinput

# Port d'écoute
EXPOSE 8000

# Commande de démarrage
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "portfolio_dimitri.wsgi:application"]