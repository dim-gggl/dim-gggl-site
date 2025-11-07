# Agent Configuration File

> **Optimized for**: Cursor AI, Claude Code, and GitHub Codex
> **Project**: Portfolio Dimitri Gaggioli - dim-gggl.com
> **Tech Stack**: Django 5.2.7 + Tailwind CSS 4 + PostgreSQL + Redis

---

## 🎯 Project Overview

This is a production-ready **Django portfolio website** showcasing projects, technologies, and professional experience for **Dimitri Gaggioli**, a Python Backend Developer. The site emphasizes:

- **Visual Identity**: Per-project custom colors, gradients, and styling
- **Performance**: Redis caching, query optimization, WhiteNoise static files
- **Security**: CSRF, CSP, HSTS, rate limiting, Sentry monitoring
- **Developer Experience**: pytest, black, flake8, docker-compose, component-based templates

**Live Site**: https://dim-gggl.com
**Language**: French (fr-fr)
**Time Zone**: Europe/Paris

---

## 📁 Project Structure

```
dim-gggl-site/
├── core/                          # Core app (homepage, contact, base templates)
│   ├── templates/core/
│   │   ├── base.html             # Base template with header/footer
│   │   ├── home.html             # Homepage with featured projects
│   │   └── components/           # Reusable template components
│   ├── models.py                 # ContactMessage model
│   ├── views.py                  # HomeView, ContactView
│   ├── middleware.py             # MaintenanceMode, SecurityHeaders, QueryCount
│   └── context_processors.py    # Global context (site_info, global_settings)
│
├── projects/                      # Projects app (portfolio showcase)
│   ├── templates/projects/
│   │   ├── project_list.html    # Grid of projects with filtering
│   │   ├── project_detail.html  # Single project detail page
│   │   └── components/          # Project cards, badges
│   ├── models.py                 # Project, Technology, Category, ProjectImage
│   ├── views.py                  # ProjectListView, ProjectDetailView
│   ├── admin.py                  # Rich admin interface
│   ├── sitemaps.py              # SEO sitemaps
│   └── management/commands/     # load_projects, update_proficiency
│
├── portfolio_dimitri/            # Django project settings
│   ├── settings.py              # Environment-based configuration
│   ├── urls.py                  # URL routing
│   ├── wsgi.py                  # WSGI app for Gunicorn
│   └── asgi.py                  # ASGI configuration
│
├── theme/                        # Tailwind CSS theme
│   ├── static_src/
│   │   ├── src/styles.css       # Tailwind source
│   │   ├── package.json         # Node dependencies
│   │   └── postcss.config.js    # PostCSS configuration
│   └── static/css/dist/         # Compiled CSS output
│
├── static/                       # Global static files
├── media/                        # User-uploaded media (images)
├── requirements/                 # Split requirements (base, dev, prod)
├── docs/                         # Project documentation
├── Dockerfile                    # Production Docker image
├── docker-compose.yaml          # Local dev environment
├── gunicorn_config.py           # Gunicorn production config
└── pytest.ini                   # Test configuration
```

---

## 🛠️ Technology Stack

### Backend
- **Django 5.2.7** (Python 3.14.0) - Web framework
- **PostgreSQL** (production) / **SQLite** (development) - Database
- **Redis** + django-redis - Caching layer
- **Gunicorn 23.0.0** - WSGI server
- **psycopg 3.2.12** - PostgreSQL adapter
- **WhiteNoise 6.11.0** - Static file serving with compression
- **Sentry SDK 2.43.0** - Error monitoring and performance tracking

### Frontend
- **Tailwind CSS 4.1.16** - Utility-first CSS framework
- **PostCSS 8.5.6** - CSS processing pipeline
- **Django Templates** - Server-side rendering with Jinja-style syntax
- **Fonts**: Saira (sans), IBM Plex Mono (monospace)

### DevOps & Tools
- **Docker** + docker-compose - Containerization
- **pytest 8.4.2** + pytest-django 4.11.1 - Testing framework
- **black 25.9.0** - Code formatting (PEP 8)
- **flake8 7.3.0** - Linting
- **django-debug-toolbar** - Development debugging
- **django-compressor 4.5.1** - Asset compression

### Security & Performance
- **django-ratelimit 4.1.0** - Rate limiting
- **CSRF protection**, **CSP headers**, **HSTS**
- **Query optimization** with select_related/prefetch_related
- **Image optimization** on upload (Pillow)

---

## 🏗️ Architecture & Design Patterns

### Database Models

#### **Project Model** (`projects/models.py:111-314`)
The core portfolio item with:
- **Visual Identity**: `primary_color`, `secondary_color`, `background_style`, `gradient_css`
- **Media**: `featured_image`, `logo`
- **Relations**: ManyToMany with `Technology`, ForeignKey to `Category`
- **Metadata**: `is_featured`, `is_published`, `order`, `completed_at`
- **Methods**: `get_similar_projects()` for recommendations
- **Manager**: `published` (custom manager for filtering published projects)

#### **Technology Model** (`projects/models.py:30-81`)
Technologies/frameworks used:
- Fields: `name`, `slug`, `category`, `icon`, `color`, `proficiency`, `order`
- Categories: backend, frontend, database, tool, language
- Proficiency: 1-5 scale

#### **Category Model** (`projects/models.py:83-109`)
Project categories (Backend CLI, Fullstack, etc.)

#### **ProjectImage Model** (`projects/models.py:316-350`)
Gallery images for projects with auto-optimization

### Key Features

#### **Per-Project Visual Identity**
Each project has unique colors and gradients:
```python
project.gradient_css  # Returns CSS string: linear-gradient(135deg, #95ff17 0%, #f7931e 100%)
```

#### **Smart Filtering**
Projects can be filtered by:
- Category (Backend CLI, Fullstack, etc.)
- Technology (Python, Django, PostgreSQL, etc.)
- Featured status

#### **Image Optimization**
All uploaded images are automatically optimized via `core.utils.optimize_image()`.

#### **Caching Strategy**
- **Redis cache** in production (15-minute TTL)
- **LocMemCache** in development
- Cached items: sidebar data, navigation, homepage featured projects
- Cache key prefix: `portfolio`

---

## 🚀 Development Workflow

### Initial Setup

```bash
# 1. Install Python dependencies
pip install -r requirements/dev.txt

# 2. Install Node dependencies for Tailwind
cd theme/static_src
npm install
cd ../..

# 3. Set up environment variables
cp .env.example .env  # If available
# Edit .env with your settings (DEBUG=True, DATABASE_URL, etc.)

# 4. Run migrations
python manage.py migrate

# 5. Load initial data (optional)
python manage.py load_projects ./projects.json
python manage.py loaddata projects/fixtures/technologies.json

# 6. Create superuser
python manage.py createsuperuser
```

### Running Development Servers

```bash
# Terminal 1: Django development server
python manage.py runserver

# Terminal 2: Tailwind CSS watch mode
cd theme/static_src
npm run dev
```

Access the site at: http://127.0.0.1:8000
Admin panel: http://127.0.0.1:8000/admin

### Using Docker (Alternative)

```bash
# Build and run with docker-compose
docker-compose up --build

# Run migrations in container
docker-compose exec web python manage.py migrate

# Create superuser in container
docker-compose exec web python manage.py createsuperuser
```

### Common Development Tasks

```bash
# Run tests
pytest
pytest -v                     # Verbose output
pytest --reuse-db            # Reuse test database (faster)
pytest core/tests/           # Test specific app

# Code formatting
black .                      # Format all Python files
black core/ projects/        # Format specific directories

# Linting
flake8                       # Lint entire project
flake8 --max-line-length=88  # Match Black's line length

# Database
python manage.py makemigrations
python manage.py migrate
python manage.py dbshell     # Open database shell

# Cache management
python manage.py clear_cache # Custom command to flush cache

# Static files
python manage.py collectstatic --noinput
python manage.py compress    # Compress CSS/JS

# Data management
python manage.py load_projects ./projects.json
python manage.py update_proficiency ./tech_stack.json
```

---

## 📝 Coding Standards & Conventions

### Python Code Style

- **Formatter**: Black (line length: 88)
- **Linter**: Flake8
- **Type Hints**: Encouraged for public APIs
- **Docstrings**: Google-style for classes and complex functions
- **Imports**: Sorted (stdlib, third-party, local)

Example:
```python
from django.db import models
from django.urls import reverse

from core.utils import optimize_image  # Local import


class Project(models.Model):
    """Represents a portfolio project with a unique visual identity.

    Attributes:
        title: The project title.
        slug: URL-friendly identifier.
        primary_color: HEX color for gradient start.
    """
    title = models.CharField(max_length=200)
    # ...
```

### Django Best Practices

#### **Query Optimization**
ALWAYS use `select_related()` and `prefetch_related()` to avoid N+1 queries:

```python
# GOOD ✅
projects = Project.published.select_related('category').prefetch_related('technologies')

# BAD ❌
projects = Project.published.all()  # Will cause N+1 queries
```

#### **Custom Managers**
Use custom managers for common filters:
```python
# GOOD ✅
projects = Project.published.all()  # Uses custom manager

# LESS CLEAR ❌
projects = Project.objects.filter(is_published=True)
```

#### **Database Indexes**
Models use strategic indexes on frequently queried fields:
- `is_published`, `is_featured`, `order`
- `category`, `slug`
- Composite indexes for common query patterns

#### **Validation**
Use model validators:
```python
from django.core.exceptions import ValidationError

def validate_hex_color(value):
    if not value.startswith("#") or len(value) != 7:
        raise ValidationError(f"{value} is not a valid HEX color")
```

### Template Conventions

- **Component-based**: Reusable components in `templates/*/components/`
- **Context processors**: Use for global data (site_info, settings)
- **Template inheritance**: All pages extend `core/base.html`
- **Naming**: Lowercase with underscores (e.g., `project_list.html`)

### URL Patterns

- **Namespaced**: `projects:list`, `projects:detail`
- **Slugs**: Use slugs for detail views, not IDs
- **Trailing slashes**: Always include (Django convention)

---

## 🧪 Testing Guidelines

### Test Structure
```
core/tests/
  ├── test_models.py
  ├── test_views.py
  └── test_middleware.py

projects/tests/
  ├── test_models.py
  ├── test_views.py
  └── test_managers.py
```

### Writing Tests

```python
import pytest
from django.urls import reverse
from projects.models import Project, Technology

@pytest.mark.django_db
class TestProjectModel:
    def test_gradient_css_generation(self):
        """Test that gradient_css property generates valid CSS."""
        project = Project.objects.create(
            title="Test Project",
            primary_color="#95ff17",
            secondary_color="#f7931e"
        )
        expected = "linear-gradient(135deg, #95ff17 0%, #f7931e 100%)"
        assert project.gradient_css == expected
```

### Test Configuration
- **Database**: Reuses test database (`--reuse-db`)
- **Migrations**: Skipped for speed (`--nomigrations`)
- **Fixtures**: Use JSON fixtures in `projects/fixtures/`

---

## 🔐 Security Considerations

### Environment Variables
NEVER commit sensitive data. Use `.env` file:
```env
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:pass@host:5432/dbname
REDIS_URL=redis://localhost:6379/1
SENTRY_DSN=https://...
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
```

### CSRF Protection
All forms must include `{% csrf_token %}`.

### Rate Limiting
Contact form uses django-ratelimit:
```python
@ratelimit(key='ip', rate='5/h', method='POST')
def contact_view(request):
    # ...
```

### Content Security Policy
Configured in `settings.py:359-371`. Adjust when adding third-party scripts.

### Production Security Checklist
- ✅ `DEBUG = False`
- ✅ Secure `SECRET_KEY` from environment
- ✅ HTTPS enforced (`SECURE_SSL_REDIRECT = True`)
- ✅ Secure cookies (`SESSION_COOKIE_SECURE = True`)
- ✅ HSTS headers (1 year)
- ✅ CSP headers configured
- ✅ Rate limiting on forms

---

## 🚢 Deployment

### Environment Setup

**Production environment variables**:
```env
ENVIRONMENT=production
DEBUG=False
SECRET_KEY=<generate-secure-key>
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
ALLOWED_HOSTS=dim-gggl.com,www.dim-gggl.com
CSRF_TRUSTED_ORIGINS=https://dim-gggl.com,https://www.dim-gggl.com
SENTRY_DSN=https://...
```

### Build Process

```bash
# 1. Build Tailwind CSS
cd theme/static_src
npm run build

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Compress assets
python manage.py compress

# 4. Run migrations
python manage.py migrate

# 5. Start Gunicorn
gunicorn --config gunicorn_config.py portfolio_dimitri.wsgi:application
```

### Docker Deployment

```bash
# Build image
docker build -t dim-gggl-portfolio .

# Run container
docker run -d \
  -p 8000:8000 \
  --env-file .env.production \
  dim-gggl-portfolio
```

### Maintenance Mode

Set `MAINTENANCE_MODE=True` in environment to show maintenance page.

---

## 📚 Key Files Reference

### Configuration Files

| File | Purpose |
|------|---------|
| `portfolio_dimitri/settings.py` | Django settings (env-based config) |
| `portfolio_dimitri/urls.py` | URL routing |
| `gunicorn_config.py` | Gunicorn production config |
| `pytest.ini` | Test configuration |
| `.flake8` | Linting rules |
| `Dockerfile` | Production Docker image |
| `docker-compose.yaml` | Local development environment |
| `tailwind.config.js` | Tailwind CSS configuration |

### Data Files

| File | Purpose |
|------|---------|
| `projects.json` | Project data for bulk import |
| `tech_stack.json` | Technology proficiency data |
| `projects/fixtures/*.json` | Fixture data for categories/technologies |

### Entry Points

| File | Purpose |
|------|---------|
| `manage.py` | Django CLI |
| `portfolio_dimitri/wsgi.py` | WSGI application (Gunicorn) |
| `portfolio_dimitri/asgi.py` | ASGI application |

---

## 🎨 Frontend Development

### Tailwind CSS Workflow

**Source**: `theme/static_src/src/styles.css`
**Output**: `theme/static/css/dist/styles.css`

```bash
# Development (watch mode)
cd theme/static_src
npm run dev

# Production build (minified)
cd theme/static_src
npm run build
```

### Custom Tailwind Configuration

See `tailwind.config.js` for:
- Custom colors (primary, secondary, accent)
- Font family definitions
- Extended spacing/sizing
- Custom plugins

### Template Components

Located in `core/templates/core/components/` and `projects/templates/projects/components/`:
- `header.html` - Site header/navigation
- `footer.html` - Site footer
- `project_card.html` - Project grid item
- `tech_badge.html` - Technology badge

---

## 🎯 AI Assistant Guidelines

When working on this project, please:

### DO ✅
- **Query optimization**: Always use `select_related()` and `prefetch_related()`
- **Consistency**: Follow existing naming conventions and file structure
- **Type hints**: Add type hints to new functions
- **Docstrings**: Document complex logic with Google-style docstrings
- **Tests**: Write tests for new features using pytest
- **Validation**: Use Django validators for model fields
- **Security**: Never hardcode secrets; use environment variables
- **Caching**: Consider cache invalidation when modifying data
- **Migrations**: Create migrations after model changes
- **Indexes**: Add database indexes for frequently queried fields

### DON'T ❌
- **N+1 queries**: Avoid iterating over querysets without optimization
- **Hardcoded values**: Don't hardcode URLs, paths, or configuration
- **Direct SQL**: Prefer Django ORM over raw SQL
- **Blocking operations**: Don't perform slow operations in views (use signals/Celery)
- **Inline styles**: Use Tailwind classes, not inline CSS
- **Production secrets**: Never commit `.env` or sensitive data
- **Debug in prod**: Ensure `DEBUG=False` in production
- **Skipping tests**: Always run tests before committing

### Code Review Checklist
Before suggesting code changes, verify:
- [ ] No N+1 query issues
- [ ] Database indexes on filtered/ordered fields
- [ ] Type hints for function signatures
- [ ] Proper error handling and logging
- [ ] Security: CSRF tokens, input validation, rate limiting
- [ ] Tests written and passing
- [ ] Follows PEP 8 (Black formatting)
- [ ] No flake8 warnings
- [ ] Cache invalidation if needed
- [ ] Migration created if models changed

---

## 🔧 Troubleshooting

### Common Issues

#### **Tailwind styles not updating**
```bash
# Rebuild Tailwind CSS
cd theme/static_src
npm run build:clean
npm run build
```

#### **Static files not loading**
```bash
# Collect static files
python manage.py collectstatic --noinput --clear

# Check STATIC_ROOT and STATIC_URL in settings
```

#### **Database connection errors**
```bash
# Check DATABASE_URL format
# PostgreSQL: postgresql://user:pass@host:5432/dbname
# SQLite: sqlite:///path/to/db.sqlite3

# Test connection
python manage.py dbshell
```

#### **Redis cache errors**
```bash
# Check REDIS_URL
# Start Redis: redis-server
# Test connection: redis-cli ping
```

#### **Migration conflicts**
```bash
# Show migration status
python manage.py showmigrations

# Fake a migration if needed (careful!)
python manage.py migrate --fake appname migration_name
```

---

## 📖 Additional Resources

### Documentation
- **Project Docs**: `/docs/PROJECTS.md` - Project management system guide
- **Django Docs**: https://docs.djangoproject.com/en/5.2/
- **Tailwind CSS**: https://tailwindcss.com/docs
- **pytest-django**: https://pytest-django.readthedocs.io/

### Management Commands
```bash
# List all available commands
python manage.py help

# Custom commands
python manage.py load_projects <path>        # Import projects from JSON
python manage.py update_proficiency <path>   # Update tech proficiency
python manage.py clear_cache                 # Flush Redis cache
```

### Useful Queries

```python
# Get featured projects with technologies
Project.published.filter(is_featured=True).prefetch_related('technologies')

# Get projects by category
Project.published.filter(category__slug='backend-cli')

# Get projects using specific technology
Project.published.filter(technologies__slug='django')

# Get similar projects
project.get_similar_projects(limit=3)
```

---

## 🎓 Learning Notes

### Key Design Decisions

1. **Per-project visual identity**: Each project has custom colors/gradients for unique branding
2. **Component-based templates**: Reusable components reduce duplication
3. **Custom managers**: `published` manager simplifies queries
4. **Image optimization**: Auto-optimization on upload reduces bandwidth
5. **Redis caching**: 15-minute cache TTL balances freshness and performance
6. **Environment-based config**: Supports dev/staging/prod with same codebase
7. **Security-first**: Multiple layers (CSRF, CSP, HSTS, rate limiting)

### Performance Optimizations

- **Query optimization**: select_related/prefetch_related everywhere
- **Database indexes**: Strategic indexes on filtered/ordered fields
- **Connection pooling**: `CONN_MAX_AGE = 600` (10 minutes)
- **Static file compression**: WhiteNoise with Brotli/gzip
- **Asset minification**: django-compressor for CSS/JS
- **Image optimization**: Pillow-based resizing/compression
- **CDN-ready**: Static files served with far-future expires headers

---

## 📋 Quick Reference

### Environment Variables
| Variable | Dev Default | Production Required |
|----------|------------|---------------------|
| `DEBUG` | `True` | `False` |
| `SECRET_KEY` | Auto-generated | ✅ Required |
| `DATABASE_URL` | SQLite | PostgreSQL URL |
| `REDIS_URL` | None (LocMem) | Redis URL |
| `ALLOWED_HOSTS` | localhost | Domain list |
| `SENTRY_DSN` | Empty | Optional |

### Port Mappings
- **Django dev server**: 8000
- **PostgreSQL**: 5432
- **Redis**: 6379

### Default Credentials
Admin user must be created manually:
```bash
python manage.py createsuperuser
```

---

**Last Updated**: 2025-01-07
**Maintained By**: Dimitri Gaggioli
**AI Assistant**: Use this file as the primary context for understanding and modifying this codebase.
