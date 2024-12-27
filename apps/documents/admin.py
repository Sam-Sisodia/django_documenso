from django.contrib import admin
from  apps.documents.models import DocumentField,DocumentGroup,Document,Recipient,DocumentsRecipient

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
    list_display = ["id", "title","created_by","updated_by","created_by_date","updated_by_date"]
    search_fields =["title"]


# @admin.register(Recipient)
# class RecipientAdmin(admin.ModelAdmin):
#     list_display = ('name', 'email', 'role', 'created_by','created_at', 'order')
#     search_fields = ('name', 'email', 'role')
#     list_filter = ('role',)
    
# @admin.register(DocumentsRecipient)
# class DocumentsRecipientAdmin(admin.ModelAdmin):
#     list_display = ('recipient', 'document_group', 'note')
#     search_fields = ('recipient__name', 'document_group__title')
#     list_filter = ('document_group',)



