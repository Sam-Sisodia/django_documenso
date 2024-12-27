from django.contrib import admin

# Register your models here.

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


@admin.register(User)
class Useradmin(admin.ModelAdmin):
    list_display = ["id", "email", "username"]
    search_fields =["email"]

    def save_model(self, request, obj, form, change):
        if not change or 'password' in form.changed_data:
            # Hash the new password
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)