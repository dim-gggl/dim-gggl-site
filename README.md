# Portfolio Django – Dimitri Gaggioli

Projet Django avec frontend Tailwind (CDN pour démarrer) et structure prête pour intégration UI/animations.

## Prérequis
- Python 3.11+ (fonctionne avec 3.14)
- macOS/Linux (zsh/bash)

## Installation rapide
```
# 1) Créer et activer l'environnement (dans le repo)
python3 -m venv .venv
source .venv/bin/activate

# 2) Installer les dépendances de base
pip install -r requirements/base.txt

# (Optionnel) Dépendances de dev
pip install -r requirements/dev.txt

# 3) Variables d'environnement (exemple)
# Créez un fichier .env à la racine avec:
# SECRET_KEY=change-me
# DEBUG=True
# ALLOWED_HOSTS=
# # BDD PostgreSQL (pour prod)
# # DB_ENGINE=django.db.backends.postgresql
# # DB_NAME=portfolio
# # DB_USER=postgres
# # DB_PASSWORD=secure-password
# # DB_HOST=localhost
# # DB_PORT=5432

# 4) Migrations
python manage.py migrate

# 5) Lancer le serveur
python manage.py runserver
```

## Structure principale
```
portfolio_dimitri/
├── core/            # Pages, base templates, overlay intro
├── projects/        # Modèle Project (featured)
├── requirements/    # base/dev/prod
└── tailwind.config.js
```

## Frontend
- Tailwind via CDN (bootstrap rapide). Fichier core/static/css/design-system.css pour la palette/variables.
- Composants de la home: navbar, hero, summary, featured, tech, footer.
- Overlay d'intro animé: core/templates/core/components/intro_overlay.html + core/static/js/main.js.

## Prochaines étapes
- Intégrer un build Tailwind (CLI ou PostCSS) pour la prod
- Ajouter tests (pytest-django) et debug toolbar en dev
- Configurer PostgreSQL et déploiement (Heroku/containers)

## License
MIT
