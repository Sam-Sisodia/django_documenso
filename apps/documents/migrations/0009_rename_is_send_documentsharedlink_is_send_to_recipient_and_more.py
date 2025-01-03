# Generated by Django 5.1.4 on 2025-01-03 09:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("documents", "0008_documentsharedlink_otp_documentsharedlink_otp_expiry"),
    ]

    operations = [
        migrations.RenameField(
            model_name="documentsharedlink",
            old_name="is_send",
            new_name="is_send_to_recipient",
        ),
        migrations.RemoveField(
            model_name="documentsharedlink",
            name="otp_expiry",
        ),
        migrations.AddField(
            model_name="documentsharedlink",
            name="otp_verified",
            field=models.BooleanField(default=False),
        ),
    ]