# Generated by Django 5.1.4 on 2024-12-26 12:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0003_documentgroup_document"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="document",
            name="document_group",
        ),
    ]
