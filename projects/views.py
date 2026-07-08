"""
Frontend routes for the projects section.

The list and detail pages are rendered by the React single-page
application; their data comes from the JSON API (see the ``api`` app).
These views only serve the SPA shell while keeping the historical URL
names used by sitemaps and ``Project.get_absolute_url``.
"""

from core.views import SpaView


class ProjectListView(SpaView):
    pass


class ProjectDetailView(SpaView):
    pass
