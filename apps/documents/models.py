
from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

from apps.utils.models import TimeStampModel
from apps.documents.enum import SigningType,DocumentStatus ,DocumentType,RecipientRole
from django.utils.timezone import now

class Field(TimeStampModel):
    name = models.CharField(max_length=30)  

    def __str__(self):
        return self.name

class Document(TimeStampModel):
    title = models.CharField(max_length=255)  
    file_data = models.TextField(null=True, blank=True) 
  
    def __str__(self):
        return self.title
    class Meta:
        db_table = 'documentsfields'
    
    
    
class DocumentGroupRecipient(TimeStampModel):
    document_group = models.ForeignKey('DocumentGroup', on_delete=models.CASCADE, related_name='group_recipients')
    recipient = models.ForeignKey('Recipient', on_delete=models.CASCADE, related_name='recipient_groups')
    note = models.TextField(null=True, blank=True)  
    order = models.IntegerField(default=0)  

    class Meta:
        db_table = 'document_group_recipient'
        unique_together = ('document_group', 'recipient')  # Ensure no duplicate entries

class DocumentGroup(TimeStampModel):
    title = models.CharField(max_length=255)
    status = models.CharField(  max_length=50,  choices=DocumentStatus.choices(), default=DocumentStatus.DRAFT )
    signing_type = models.CharField(max_length=50,     choices=SigningType.choices(),
        default=SigningType.PARALLEL
    )
    note = models.TextField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    subject = models.CharField(max_length=255, null=True, blank=True)
    document_type =  models.CharField(
        max_length=50,
        choices=DocumentType.choices(),
        default=DocumentType.DOCUMENT
    )
    documents = models.ManyToManyField( 'Document', related_name='groups_documents',   blank=True  )
 
    orderrecipients = models.ManyToManyField(
        'Recipient', through='DocumentGroupRecipient', related_name='document_groups'
    ) 
    
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'documents_group'  
    

class Recipient(TimeStampModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.CharField( max_length=50,  choices=RecipientRole.choices(),     default=RecipientRole.SIGNER  )
  
    
    class Meta:
        db_table = 'recipients'
        indexes = [
            models.Index(fields=['id']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    
    
class DocumentField(TimeStampModel):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='documentfield_document',null=True)
    field = models.ForeignKey('Field', on_delete=models.CASCADE, related_name='documentfield_fields',null=True)
    recipient = models.ForeignKey('Recipient',on_delete=models.CASCADE, related_name='documentfield_recipient',null=True)
    value = models.CharField(max_length=255, null=True, blank=True)
    positionX = models.CharField(max_length=255, null=True, blank=True)
    positionY = models.CharField(max_length=255, null=True, blank=True)
    width = models.CharField(max_length=255, null=True, blank=True)
    height = models.CharField(max_length=255, null=True, blank=True)
    page_no = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'document_field'

    def __str__(self):
        return f"Field {self.field.name} on Page {self.page_no} of Document {self.document.title}"





class DocumentSharedLink(TimeStampModel):
    document = models.ForeignKey(
        'Document',
        on_delete=models.CASCADE,
        related_name='shared_links',
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

    def __str__(self):
        return f"Shared Link: {self.token}"





