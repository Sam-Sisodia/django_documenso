
from django.db import models

from django.contrib.auth import get_user_model
User = get_user_model()

from apps.utils.models import TimeStampModel
from apps.documents.enum import SigningType,DocumentStatus ,DocumentType

class DocumentField(TimeStampModel):
    name = models.CharField(max_length=30)  

    def __str__(self):
        return self.name





    
class DocumentGroup(TimeStampModel):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='documents')
 
    status = models.CharField(
        max_length=50,
        choices=DocumentStatus.choices(),
        default=DocumentStatus.DRAFT
    )
    signing_type = models.CharField(
        max_length=50,
        choices=SigningType.choices(),
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
  



    def __str__(self):
        return self.title

    class Meta:
        db_table = 'documents'  # To match the original table name
    
    
    

class Document(TimeStampModel):
    title = models.CharField(max_length=255)  
    file_data = models.TextField(null=True, blank=True) 
    document_group = models.ForeignKey(
        DocumentGroup,
        on_delete=models.CASCADE,
        related_name='groups_documents',
        null=True,
        blank=True,
    )


    def __str__(self):
        return self.title
    
    
     # created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='documents_user')  
     
     
     
     
     
    # Relationships
    # user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='document_groups')
    # documentsharedlinks = models.ManyToManyField('DocumentSharedLink', related_name='document_groups', blank=True)
    # documnet_fields = models.ManyToManyField('CheckFields', related_name='document_groups', blank=True)
    # recipients = models.ManyToManyField('Recipient', through='DocumentRecipient', related_name='document_groups')
    # signing_document = models.ForeignKey('DocumentSigningProcess', on_delete=models.CASCADE, related_name='document_groups', null=True)
