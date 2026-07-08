#!/bin/bash

set -euo pipefail

echo "🚀 Démarrage du déploiement..."

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

BRANCH=$(git branch --show-current)
if [ "${BRANCH}" != "main" ]; then
  echo -e "${RED}❌ Vous devez être sur la branche main${NC}"
  exit 1
fi

echo "📥 Pull des derniers changements..."
git pull origin main

if [ ! -d ".venv" ]; then
  echo -e "${RED}❌ L'environnement virtuel .venv est introuvable${NC}"
  exit 1
fi

echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

echo "📦 Installation des dépendances..."
pip install -r requirements/prod.txt

echo "🗄️  Application des migrations..."
python manage.py migrate --settings=portfolio_dimitri.settings

echo "⚛️  Build du frontend React..."
npm ci --prefix frontend
npm run build --prefix frontend

echo "📁 Collecte des fichiers statiques..."
python manage.py collectstatic --noinput --settings=portfolio_dimitri.settings

echo "🔄 Redémarrage de Gunicorn..."
sudo systemctl restart gunicorn

echo "🌐 Redémarrage de Nginx..."
sudo systemctl restart nginx

echo -e "${GREEN}✅ Déploiement terminé avec succès !${NC}"

