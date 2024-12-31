from rest_framework import serializers
from apps.documents.models import Field ,Document,DocumentGroup,Recipient,DocumentField,DocumentGroupRecipient,DocumentSharedLink # Import the DocumentField model
from rest_framework.exceptions import ValidationError
class DocumentsFieldsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)  # Define the 'name' field
    
    class Meta:
        model = Field  
        fields = ["id", "name"]  


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file_data']


class DocumentGroupSerializer(serializers.ModelSerializer):
    upload_documents = serializers.ListField(
        child=serializers.FileField(), required=False, write_only=True
    )
    documents = DocumentSerializer(many=True, read_only=True)  
    class Meta:
        model = DocumentGroup
        fields = ['id','title', 'status', 'note', 'documents', 'signing_type', 'subject', 'message', 'upload_documents']
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        uploaded_files = validated_data.pop('upload_documents', [])
        user = self.context['request'].user
        title = validated_data.get('title', '')
        status = validated_data.get('status', 'draft') 
        note = validated_data.get('note', '')
        signing_type = validated_data.get('signing_type', 'parallel')  
        subject = validated_data.get('subject', '')
        message = validated_data.get('message', '')

        document_group = DocumentGroup.objects.create(
            created_by=user,
            updated_by=user,
            title=title,
            status=status,
            note=note,
            signing_type=signing_type,
            subject=subject,
            message=message
        )
      
        document_instances = []
        for file in uploaded_files:
            document = Document.objects.create(
                title=file.name,
                file_data=file.read(),  # Decode file as text
                created_by=user,
                updated_by=user,
            )
            document_instances.append(document)

      
        document_group.documents.set(document_instances)

        return document_group

class RecipientSerializer(serializers.ModelSerializer):
    order = serializers.CharField(required = False)
    note = serializers.CharField(required = False)
    class Meta:
        model = Recipient
        fields = ['id','name', 'email', 'role', 'order','note']

class DocumentRecipientSerializer(serializers.Serializer):
    document_id = serializers.IntegerField()
    recipients = RecipientSerializer(many=True)

class DocumentsRecipientSerializer(serializers.ModelSerializer):
    document_group_id = serializers.IntegerField(write_only=True)
    documents = DocumentRecipientSerializer(many=True, required=False, write_only=True)

    class Meta:
        model = Recipient 
        fields = ['id','document_group_id', 'documents']
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
         
    def get_parent_instace(self,document_group_id):
        
        document_group_instance = DocumentGroup.objects.filter(id=document_group_id).first()
        return document_group_instance
    
    
  
         
    def validate(self, attrs):
        document_group_id = attrs.get("document_group_id")
        instance = self.get_parent_instace(document_group_id)

        if not instance:
            raise ValidationError("Invaild document id ")
        
        return super().validate(attrs)
    
    def add_throught_table_data (self,instance,recipient,order,note,user):
        # if DocumentGroupRecipient.objects.filter(document_group,)
        DocumentGroupRecipient.objects.create(
                document_group = instance,
                recipient=recipient,
                note =note,
                order = order,
                created_by = user,updated_by =user
            )
        

    def create(self, validated_data):
        documents_data = validated_data.get('documents', [])
        user = self.context['request'].user 
        document_group_id = validated_data.get("document_group_id")
        instance = self.get_parent_instace(document_group_id)
        
        created_recipients = [] 
        for document_data in documents_data:
            document_id = document_data.get('document_id')
            recipients_data = document_data.get('recipients', [])
            
            for recipient_data in recipients_data:
                recipient_data["created_by"] =user
                recipient_data["updated_by"] =user
                order = recipient_data.pop('order', [])
                note = recipient_data.pop('note', [])
                recipient, created = Recipient.objects.get_or_create(email=recipient_data['email'], defaults=recipient_data)
                response = self.add_throught_table_data(instance,recipient,order,note,user)
                
                created_recipients.append(recipient)

    
        return created_recipients
    
    
class DocumentFieldSerializer(serializers.ModelSerializer):
    recipient = serializers.IntegerField(source='recipient.id')
    field_id = serializers.IntegerField(source='field.id')
    class Meta:
        model = DocumentField
        fields = ['recipient', 'value', 'positionX', 'positionY', 'width', 'height', 'field_id', 'page_no']
        


class CreateDocumentFieldBulkSerializer(serializers.Serializer):
    document_id = serializers.IntegerField()
    fields = DocumentFieldSerializer(many=True)
    def create(self, validated_data):
        document_id = validated_data['document_id']
        fields_data = validated_data['fields']
        user = self.context['request'].user 
         
        document_fields = []
        for field_data in fields_data:
            if DocumentField.objects.filter(document_id=document_id,
                                            recipient_id=field_data['recipient']['id'],
                                            field_id=field_data['field']['id'],
                                           positionX=field_data['positionX'],
                                           positionY=field_data['positionY']).exists():
                
                raise ValidationError("Recipient with this document and field id is already exits")
            
            document_field = DocumentField(
                document_id=document_id,
                recipient_id=field_data['recipient']['id'],
                field_id=field_data['field']['id'],
                value=field_data['value'],
                positionX=field_data['positionX'],
                positionY=field_data['positionY'],
                width=field_data['width'],
                height=field_data['height'],
                page_no=field_data['page_no'],
                created_by=user,
                updated_by=user,
            )
            document_fields.append(document_field)

        return DocumentField.objects.bulk_create(document_fields)

class UpdateDocumentsFieldsSerilalizer(serializers.ModelSerializer):
    class Meta:
        model = DocumentField
        fields = "__all__"
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
    
    
class ResponseDocumentGroupSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True) 
    class Meta:
        model = DocumentGroup
        fields = ['title','documents', 'status', 'note',  'signing_type', 'subject', 'message','document_type']
       
       
   


####################################
class DocumentRecipients(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id','name', 'email', 'role']
   
    

class SingleDoc(serializers.ModelSerializer):
    orderrecipients = DocumentRecipients(many=True)
    class Meta:
        model = DocumentGroup
        fields = ['title', 'status', 'note',  'signing_type', 'subject', 'message','document_type','orderrecipients']
           
    
    
    
class FieldData(serializers.ModelSerializer):
  class Meta:
        model = Field
        fields = ['id', 'name',]
           
    
    
    
class DocumentFieldSerializer(serializers.ModelSerializer):
    field = FieldData(read_only=True) 
    class Meta:
        model = DocumentField
        fields = ['id', 'document',"value","positionX","positionY","width","height","page_no","field"] 

class SingleDocumentSerializerResponse(serializers.ModelSerializer):
    documentfield_document = DocumentFieldSerializer(many=True, read_only=True)  
    groups_documents = SingleDoc(many=True)
    class Meta:
        model = Document
        fields = ['id', 'title', 'file_data', 'documentfield_document',"groups_documents"]

# groups_documents = SingleDoc(many=True)
# document
# documentfield_document
# field
# documentfield_fields
     
################################

  
class DocumentSharedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSharedLink
        fields = '__all__'