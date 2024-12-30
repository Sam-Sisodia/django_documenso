from django.db import models

# Create your models here.

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class TimeStampModel(models.Model):
    created_by = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        "users.User", on_delete=models.CASCADE, related_name="%(class)s_updated_by"
    )
    created_by_date = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_by_date = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        abstract = True


