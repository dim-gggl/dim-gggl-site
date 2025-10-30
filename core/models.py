from django.db import models
from django.utils import timezone


class ContactMessage(models.Model):
    """Contact messages received via the website contact form."""

    name = models.CharField(max_length=200, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=300, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    replied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"

    def __str__(self) -> str:
        return f"{self.name} - {self.subject}"

