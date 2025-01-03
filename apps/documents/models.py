
from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

from apps.utils.models import TimeStampModel
from apps.documents.enum import SigningType,DocumentStatus ,DocumentType,RecipientRole,DocumentValidity,RecipientAuthType
from django.utils.timezone import now

class Field(models.Model):
    name = models.CharField(max_length=30)  

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'fields'
    

class Document(TimeStampModel):
    title = models.CharField(max_length=255)  
    file_data = models.TextField(null=True, blank=True) 
  
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'documentsfields'
    
    

class DocumentGroup(TimeStampModel):
    title = models.CharField(max_length=255)
    status = models.CharField(  max_length=50,  choices=DocumentStatus.choices(), default=DocumentStatus.DRAFT )
    signing_type = models.CharField(max_length=50,     choices=SigningType.choices(),  default=SigningType.PARALLEL )
    note = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    document_type =  models.CharField(  max_length=50, choices=DocumentType.choices(), default=DocumentType.DOCUMENT )
    validity = models.CharField(  max_length=50, choices=DocumentValidity.choices(), default=DocumentValidity.NO_EXPIRY,
                    help_text="The validity type of the document (DOCUMENT or Date)."    )
    days_to_complete = models.PositiveIntegerField( null=True, blank=True,
                    help_text="Number of days allowed to complete the document (optional)."    )
    reminder_duration = models.PositiveIntegerField( null=True,   blank=True, help_text="Number of days between reminders (optional)."  )
    auto_reminder = models.BooleanField(default=False,  help_text="Whether to automatically send reminders (True/False)." )
    
    documents = models.ManyToManyField( 'Document', related_name='groups_documents',   blank=True  )

    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'documents_group'  
    




class Recipient(TimeStampModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.CharField( max_length=50,  choices=RecipientRole.choices(),     default=RecipientRole.SIGNER  )
    document_group = models.ForeignKey('DocumentGroup', on_delete=models.CASCADE, related_name='group_recipients')
    note = models.TextField(null=True, blank=True)  
    order = models.IntegerField(default=0)  
    auth_type = models.CharField( max_length=50,  choices=RecipientAuthType.choices(),     default=RecipientAuthType.EMAIL  )
    
  
    
    class Meta:
        db_table = 'recipients'
        indexes = [
            models.Index(fields=['id']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    
    
class DocumentField(TimeStampModel):

    value = models.CharField(max_length=255, null=True, blank=True)
    positionX = models.CharField(max_length=255, null=True, blank=True)
    positionY = models.CharField(max_length=255, null=True, blank=True)
    width = models.CharField(max_length=255, null=True, blank=True)
    height = models.CharField(max_length=255, null=True, blank=True)
    page_no = models.CharField(max_length=255, null=True, blank=True)
    document_group = models.ForeignKey('DocumentGroup', on_delete=models.CASCADE, related_name='documentfield_documentgroup',null=True)
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='documentfield_document',null=True)
    field = models.ForeignKey('Field', on_delete=models.CASCADE, related_name='documentfield_fields',null=True)
    recipient = models.ForeignKey('Recipient',on_delete=models.CASCADE, related_name='documentfield_recipient',null=True)

    class Meta:
        db_table = 'document_field'

    def __str__(self):
        return f"Field {self.field.name} on Page {self.page_no} of Document {self.document.title}"





class DocumentSharedLink(TimeStampModel):
    document_group = models.ForeignKey(
        'DocumentGroup',
        on_delete=models.CASCADE,
        related_name='documentgroup_shared_links',
        null=True,
        blank=True
    )
    recipient = models.ForeignKey(
        'Recipient',
        on_delete=models.CASCADE,
        related_name='recipient_links',
        null=True,
        blank=True
    )
    token = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(default=now)
    is_send = models.BooleanField(default=False)

    def __str__(self):
        return f"Shared Link: {self.token}"
    
    






