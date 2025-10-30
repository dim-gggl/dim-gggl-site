from django.contrib import admin

from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'subject',
        'created_at',
        'is_read',
    ]
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['created_at']
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
                'fields': ('created_at', 'is_read', 'replied_at'),
                'classes': ('collapse',),
            },
        ),
    )

    actions = ['mark_as_read', 'mark_as_unread']

    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = 'Mark as read'

    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
    mark_as_unread.short_description = 'Mark as unread'
