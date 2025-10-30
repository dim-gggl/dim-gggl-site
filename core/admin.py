from django.contrib import admin
from django.utils import timezone

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'subject',
        'created_at',
        'is_read',
        'replied_at',
        'ip_address',
    ]
    list_filter = ['is_read', 'created_at', 'replied_at']
    search_fields = ['name', 'email', 'subject', 'message', 'ip_address']
    readonly_fields = ['created_at', 'ip_address']
    date_hierarchy = 'created_at'

    fieldsets = (
        (
            'Contact information',
            {
                'fields': ('name', 'email', 'phone'),
            },
        ),
        (
            'Message',
            {
                'fields': ('subject', 'message'),
            },
        ),
        (
            'Metadata',
            {
                'fields': ('created_at', 'is_read', 'replied_at', 'ip_address'),
                'classes': ('collapse',),
            },
        ),
    )

    actions = ['mark_as_read', 'mark_as_unread', 'mark_as_replied']

    @admin.action(description='Mark as read')
    def mark_as_read(self, request, queryset):
        count = queryset.update(is_read=True)
        self.message_user(request, f'{count} message(s) marked as read.')

    @admin.action(description='Mark as unread')
    def mark_as_unread(self, request, queryset):
        count = queryset.update(is_read=False)
        self.message_user(request, f'{count} message(s) marked as unread.')

    @admin.action(description='Mark as replied')
    def mark_as_replied(self, request, queryset):
        count = queryset.update(replied_at=timezone.now(), is_read=True)
        self.message_user(request, f'{count} message(s) marked as replied.')