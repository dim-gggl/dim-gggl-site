from django.core.cache import cache
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver

from .models import Project, Technology, Category


@receiver([post_save, post_delete], sender=Project)
def invalidate_project_cache(sender, instance, **kwargs):
    """Invalidate project-related caches when a project is modified."""
    cache.delete("project_list_sidebar_data")
    cache.delete("project_navigation_ids")


@receiver([post_save, post_delete], sender=Technology)
@receiver([post_save, post_delete], sender=Category)
def invalidate_sidebar_cache(sender, instance, **kwargs):
    """Invalidate sidebar cache when technologies or categories change."""
    cache.delete("project_list_sidebar_data")


@receiver(m2m_changed, sender=Project.technologies.through)
def invalidate_on_tech_change(sender, instance, **kwargs):
    """Invalidate cache when project technologies are modified."""
    cache.delete("project_list_sidebar_data")
    cache.delete("project_navigation_ids")
