from django.conf import settings
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.db import models
from django.utils import timezone


class ContactMessage(models.Model):
    """Contact messages received via the website contact form."""

    name = models.CharField(max_length=200, verbose_name="Nom")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=300, verbose_name="Sujet")
    message = models.TextField(
        verbose_name="Message",
        validators=[
            MinLengthValidator(20, "Le message doit contenir au moins 20 caractères."),
            MaxLengthValidator(5000, "Le message ne peut pas dépasser 5000 caractères."),
        ]
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Téléphone")

    # Metadata
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_read = models.BooleanField(default=False, db_index=True)
    replied_at = models.DateTimeField(null=True, blank=True)
    
    # IP tracking for security/analytics
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Message de contact"
        verbose_name_plural = "Messages de contact"
        indexes = [
            models.Index(fields=['-created_at', 'is_read']),
        ]

    def __str__(self) -> str:
        return f"{self.name} - {self.subject}"

    def mark_as_read(self):
        """Mark message as read."""
        if not self.is_read:
            self.is_read = True
            self.save(update_fields=['is_read'])

    def mark_as_replied(self):
        """Mark message as replied."""
        if not self.replied_at:
            self.replied_at = timezone.now()
            self.is_read = True
            self.save(update_fields=['replied_at', 'is_read'])