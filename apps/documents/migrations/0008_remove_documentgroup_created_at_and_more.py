# Generated by Django 5.1.4 on 2024-12-26 17:35

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0007_document_document_group"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="documentgroup",
            name="created_at",
        ),
        migrations.RemoveField(
            model_name="documentgroup",
            name="updated_at",
        ),
    ]
