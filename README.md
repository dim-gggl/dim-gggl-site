# Portfolio Django – Dimitri Gaggioli

Portfolio professionnel construit avec Django 5 et une interface moderne inspirée de shadcn UI. Le projet met en avant les réalisations backend Python, avec une attention particulière portée aux performances, au SEO et à la préparation du déploiement.

## ✨ Fonctionnalités principales

- SEO avancé : meta tags dynamiques, Open Graph, Twitter Cards, structured data JSON‑LD, sitemap et robots.txt générés dynamiquement.
- Performances : compression CSS/JS via `django-compressor`, lazy-loading des images, optimisation automatique des visuels uploadés, cache applicatif et middleware de surveillance des requêtes SQL.
- Sécurité : en-têtes renforcés (HSTS, CSP, Referrer-Policy), rate limiting du formulaire de contact, honeypot anti-spam, mode maintenance configurable.
- Monitoring : intégration Sentry, Google Analytics 4 avec anonymisation IP, logs structurés en rotation.
- Déploiement : script d’automatisation, configuration Gunicorn/Nginx prête à l’emploi, paramètres production-friendly.

## 🧰 Stack technique

- **Backend** : Django 5, Python 3.11+
- **Frontend** : Templates Django, design system maison compatible shadcn, Tailwind CDN pour prototypage
- **Base de données** : PostgreSQL en production (SQLite possible en local)
- **Outils** : django-compressor, Pillow, Sentry SDK, pytest-django

## 🚀 Démarrage rapide

```bash
# 1. Cloner le dépôt
git clone https://github.com/dim-ggg1/portfolio.git
cd portfolio

# 2. Créer et activer l’environnement virtuel
python3 -m venv .venv
source .venv/bin/activate

# 3. Installer les dépendances
pip install -r requirements/dev.txt

# 4. Configurer les variables d’environnement (voir section dédiée)

# 5. Appliquer les migrations et lancer le serveur
python manage.py migrate
python manage.py runserver

# 6. Build the Tailwind assets after any design change
python manage.py tailwind build
# or start the watcher during development
# python manage.py tailwind start
```

## 🔐 Variables d’environnement

Créer un fichier `.env` à la racine en vous basant sur les clés ci-dessous :

```
DEBUG=True
SECRET_KEY=change-me
ALLOWED_HOSTS=127.0.0.1,localhost
SITE_URL=http://localhost:8000
DATABASE_URL=
CSRF_TRUSTED_ORIGINS=
GOOGLE_ANALYTICS_ID=
SENTRY_DSN=
SENTRY_TRACES_SAMPLE_RATE=0.1
DJANGO_CACHE_LOCATION=
ENVIRONMENT=development
MAINTENANCE_MODE=False
DJANGO_SECRET_KEY_FILE=
```

> `GOOGLE_ANALYTICS_ID`, `SENTRY_DSN` et `DJANGO_CACHE_LOCATION` sont optionnels mais fortement recommandés pour la production.

### Secrets Docker

- Créer `secrets/django_secret_key.txt` (ignoré par Git) et y placer la clé, sans guillemets ni espaces.
- Monter le fichier comme secret dans Docker : via Compose `secrets: [django_secret_key]` ou `docker run --mount type=bind,src=$(pwd)/secrets/django_secret_key.txt,dst=/run/secrets/django_secret_key,ro`.
- Exposer le chemin dans la variable d’environnement `DJANGO_SECRET_KEY_FILE=/run/secrets/django_secret_key`.
- En dehors de Docker, conserver l’approche `.env` en définissant directement `SECRET_KEY`.

## 🧪 Tests

```bash
source .venv/bin/activate
pytest
```

## 📦 Déploiement

### Script automatisé

```bash
./scripts/deploy.sh
```

Le script :

- Vérifie la branche active
- Met à jour le code et installe les dépendances production
- Exécute migrations, collectstatic et compress
- Redémarre Gunicorn et Nginx

### Gunicorn & Nginx

- `gunicorn_config.py` : configuration multi-workers prête à copier sur le serveur
- `deploy/gunicorn.service` : unit file systemd
- `deploy/nginx.conf` : configuration SSL + cache statique + proxy

## 🗂️ Structure du projet

```
portfolio_dimitri/
├── core/
│   ├── templates/core/        # Layout, composants, maintenance
│   ├── templatetags/          # SEO & helpers images
│   ├── middleware.py          # Maintenance, sécurité, debug requêtes
│   └── utils/image_optimizer.py
├── projects/                  # Modèles, vues, sitemaps projets
├── scripts/deploy.sh
├── deploy/                    # Configurations server-side
├── logs/, cache/              # Emplacements gérés par Django
└── portfolio_dimitri/settings.py
```

## ✅ Checklist production

- Renseigner `SITE_URL`, `ALLOWED_HOSTS`, `GOOGLE_ANALYTICS_ID`, `SENTRY_DSN`
- Lancer `python manage.py compress --settings=portfolio_dimitri.settings`
- Activer `MAINTENANCE_MODE=True` pendant les opérations critiques
- Créer les sockets/logs (`/run/gunicorn`, `/var/log/gunicorn`) avec les droits adéquats

## 📄 Licence

MIT
