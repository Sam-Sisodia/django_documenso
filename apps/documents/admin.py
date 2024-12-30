from django.contrib import admin
from  apps.documents.models import Field,DocumentGroup,Document,Recipient,DocumentField,DocumentGroupRecipient

# Register your models here.

from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
User = get_user_model()
@admin.register(Document)
class Documentadmin(admin.ModelAdmin):
    list_display = ["id", "title","created_by","updated_by","created_by_date","updated_by_date"]
    search_fields =["title"]



@admin.register(Field)
class Fieldadmin(admin.ModelAdmin):
    list_display = ["id", "name","created_by","updated_by","created_by_date","updated_by_date"]
    search_fields =["name"]


@admin.register(DocumentGroup)
class DocumentGroup(admin.ModelAdmin):
    list_display = ["id",
                "title",
                "status",
                "signing_type",
                "note",
                "message",
                "subject",
                "document_type",
                "get_documents",
                "get_recipients",
                "created_by",

                ]
    search_fields =["title"]
    
    def get_documents(self, obj):
        return ", ".join([doc.title for doc in obj.documents.all()])

    def get_recipients(self,obj):
        return ", ".join([rec.email for rec in obj.recipients.all()])
       





@admin.register(Recipient)
class Recipientadmin(admin.ModelAdmin):
    list_display = ["id",
                    "name",
                    "email",
                    "role",
                    
                    "created_by",
                    ]
    search_fields =["email"]



@admin.register(DocumentGroupRecipient)
class DocumentGroupRecipientadmin(admin.ModelAdmin):
    list_display = ["id",
                    "document_group",
                    "recipient",
                    "order",
                    "note",
                    "created_by",
                    ]
    search_fields =["order"]





@admin.register(DocumentField)
class DocumentFieldadmin(admin.ModelAdmin):
    list_display = ["id",
                    "document",
                    "field",
                    "recipient",
                    "value",
                    "positionX",
                    "positionY",
                    "width",
                    "height",
                    "page_no",
                                        
                    "created_by",
                    ]




    