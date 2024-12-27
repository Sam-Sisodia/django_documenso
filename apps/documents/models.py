
from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

from apps.utils.models import TimeStampModel
from apps.documents.enum import SigningType,DocumentStatus ,DocumentType,RecipientRole
from django.utils.timezone import now

class DocumentField(TimeStampModel):
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
    def __str__(self):
        return self.title

    class Meta:
        db_table = 'documents_group'  # To match the original table name
    

  

class Recipient(TimeStampModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    role = models.CharField( max_length=50,  choices=RecipientRole.choices(),     default=RecipientRole.SIGNER  )
    created_at = models.DateTimeField(default=now)
    order = models.IntegerField(default=0)
    recipient_documents = models.ManyToManyField(
        DocumentGroup, 
        related_name='recipients_groups_documents', 
        blank=True,
        through='DocumentsRecipient'  # Use the correct model name here
    )
    
    class Meta:
        db_table = 'recipients'
        indexes = [
            models.Index(fields=['id']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.email})"
    
    
    
class DocumentsRecipient(TimeStampModel):
    note = models.TextField(null=True)
    recipient = models.ForeignKey(Recipient, on_delete=models.CASCADE)
    document_group = models.ForeignKey(DocumentGroup, on_delete=models.CASCADE)
    class Meta:
        db_table = 'documents_recipient'  # To match your naming convention
        unique_together = ('recipient', 'document_group')  # Ensures a recipient can only be associated with a group once

    def __str__(self):
        return f"{self.recipient.name} - {self.document_group.title}"
     
     
    













   
#     # Relationships
#     # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='document_groups')
#     # documentsharedlinks = models.ManyToManyField('DocumentSharedLink', related_name='document_groups', blank=True)
#     # documnet_fields = models.ManyToManyField('CheckFields', related_name='document_groups', blank=True)
#     # recipients = models.ManyToManyField('Recipient', through='DocumentRecipient', related_name='document_groups')
#     # signing_document = models.ForeignKey('DocumentSigningProcess', on_delete=models.CASCADE, related_name='document_groups', null=True)
  