# Generated by Django 5.1.4 on 2024-12-26 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0004_remove_document_document_group"),
    ]

    operations = [
        migrations.AddField(
            model_name="documentgroup",
            name="document_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="groups_documents",
                to="documents.document",
            ),
        ),
    ]
