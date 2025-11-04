# Project Management System

## Architecture

### Models
- Project: Represents a portfolio project with its unique visual identity
- Technology: Technologies, frameworks, or tools used
- Category: Project categories
- ProjectImage: Gallery images for a project

### Relations
- Project -> Category (ForeignKey)
- Project <-> Technology (ManyToMany)
- Project -> ProjectImage (OneToMany)

## Per-Project Visual Identity

Each project defines its identity with:
- primary_color: Primary HEX color
- secondary_color: Secondary HEX color
- background_style: Background type (solid, gradient, pattern, image)

These values drive:
- Hero section background on the detail page
- Badges and accents
- Hover effects and gradients

Use the following CSS variables in templates:

```html
<style>
  :root {
    --project-primary: {{ project.primary_color }};
    --project-secondary: {{ project.secondary_color }};
    --project-gradient: {{ project.gradient_css }};
  }
  .project-hero { background: var(--project-gradient); }
  .project-link:hover { color: var(--project-primary); }
  .project-badge { background: linear-gradient(135deg, var(--project-primary), var(--project-secondary)); }
</style>
```

## Adding a New Project

1. Go to Django admin
2. Create a new project and fill base info
3. Select the category and add technologies
4. Upload the featured image (optional) and gallery images (optional)
5. Define primary/secondary colors and background style
6. Publish the project

## Filtering and Search

Project list supports:
- Filter by technology via ?tech=slug
- Filter by category via ?category=slug
- Text search via ?q=term
- Pagination (12 per page)

URLs examples:
- /projects/?tech=python
- /projects/?category=backend-cli
- /projects/?q=api

## Performance and SEO

- Views use prefetch_related to avoid N+1 queries
- Add dynamic meta tags per project detail (title/description/OG) if needed
- Ensure images have alt attributes for accessibility

## Fixtures

Load initial data:

```bash
python manage.py loaddata initial_data
```

The fixtures include base technologies, categories, and ~15 demo projects.

