# Generated by Django 5.1.4 on 2025-01-06 11:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0002_document_updated_file_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="documentfield",
            name="value",
            field=models.TextField(blank=True, null=True),
        ),
    ]
