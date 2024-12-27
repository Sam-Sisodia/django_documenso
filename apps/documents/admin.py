from django.contrib import admin
from  apps.documents.models import DocumentField,DocumentGroup,Document

# Register your models here.

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()


@admin.register(DocumentField)
class DocumentFieldadmin(admin.ModelAdmin):
    list_display = ["id", "name","created_by","updated_by","created_by_date","updated_by_date"]
    search_fields =["name"]


@admin.register(DocumentGroup)
class DocumentGroup(admin.ModelAdmin):
    list_display = ["id","title","created_by","updated_by","created_by_date","updated_by_date"]
    search_fields =["title"]


@admin.register(Document)
class Documentadmin(admin.ModelAdmin):
    list_display = ["id", "title","document_group","created_by","updated_by","created_by_date","updated_by_date"]
    search_fields =["title"]
