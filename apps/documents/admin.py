from django.contrib import admin
from  apps.documents.models import Field,DocumentGroup,Document,Recipient,DocumentField,DocumentSharedLink

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
    list_display = ["id", "name"]
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
                "validity",
                "days_to_complete",
                "reminder_duration",
                "auto_reminder",
                "created_by",
                ]
    search_fields =["title"]
    def get_documents(self, obj):
        return ", ".join([doc.title for doc in obj.documents.all()])

    def get_recipients(self,obj):
        recipient = Recipient.objects.filter(document_group=obj)
        return ", ".join([rec.email for rec in recipient])
       





@admin.register(Recipient)
class Recipientadmin(admin.ModelAdmin):
    list_display = ["id",
                    "name",
                    "email",
                    "role",
                    "document_group",
                    "note",
                    "order",
                    "auth_type",
                    "created_by",]
    search_fields =["email"]




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

@admin.register(DocumentSharedLink)
class DocumentSharedLinkadmin(admin.ModelAdmin):
    list_display = ["id",
                    "document_group",
                    "recipient",
                    "token",
                    "is_send",
                    "otp",
                    "otp_expiry",
                    "created_at",                
                    "created_by",
                    ]


    
    
    
 
