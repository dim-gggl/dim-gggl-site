# core/migrations/0002_add_indexes_and_ip.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        # Add db_index to existing fields
        migrations.AlterField(
            model_name="contactmessage",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="contactmessage",
            name="is_read",
            field=models.BooleanField(default=False, db_index=True),
        ),
        # Add IP field
        migrations.AddField(
            model_name="contactmessage",
            name="ip_address",
            field=models.GenericIPAddressField(null=True, blank=True),
        ),
        # Add composite index
        migrations.AddIndex(
            model_name="contactmessage",
            index=models.Index(
                fields=["-created_at", "is_read"], name="contact_created_read_idx"
            ),
        ),
    ]
