# projects/migrations/0003_add_indexes.py

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0002_category_technology_alter_project_options_and_more"),
    ]

    operations = [
        # Add db_index to existing fields
        migrations.AlterField(
            model_name="project",
            name="slug",
            field=models.SlugField(unique=True, max_length=200, db_index=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="is_featured",
            field=models.BooleanField(default=False, db_index=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="is_published",
            field=models.BooleanField(default=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="order",
            field=models.IntegerField(default=0, db_index=True),
        ),
        migrations.AlterField(
            model_name="project",
            name="completed_at",
            field=models.DateField(null=True, blank=True, db_index=True),
        ),
        # Add composite indexes
        migrations.AddIndex(
            model_name="project",
            index=models.Index(
                fields=["is_published", "is_featured", "order"],
                name="proj_pub_feat_order_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="project",
            index=models.Index(
                fields=["is_published", "order", "-completed_at"],
                name="proj_pub_ord_comp_idx",
            ),
        ),
        migrations.AddIndex(
            model_name="project",
            index=models.Index(
                fields=["category", "is_published"], name="proj_cat_pub_idx"
            ),
        ),
        # Technology indexes
        migrations.AlterField(
            model_name="technology",
            name="slug",
            field=models.SlugField(unique=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="technology",
            name="category",
            field=models.CharField(
                max_length=20,
                db_index=True,
                choices=[
                    ("backend", "Backend"),
                    ("frontend", "Frontend"),
                    ("database", "Database"),
                    ("tool", "Tool"),
                    ("language", "Language"),
                ],
            ),
        ),
        migrations.AddIndex(
            model_name="technology",
            index=models.Index(
                fields=["category", "proficiency"], name="tech_cat_prof_idx"
            ),
        ),
        # Category indexes
        migrations.AlterField(
            model_name="category",
            name="slug",
            field=models.SlugField(unique=True, db_index=True),
        ),
        migrations.AlterField(
            model_name="category",
            name="order",
            field=models.IntegerField(default=0, db_index=True),
        ),
    ]
