from rest_framework import serializers
from apps.documents.models import Field ,Document,DocumentGroup,Recipient,DocumentField,DocumentSharedLink # Import the DocumentField model
from rest_framework.exceptions import ValidationError
import base64
class FieldsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)  # Define the 'name' field
    class Meta:
        model = Field  
        fields = ["id", "name"]  


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id','name', 'email', 'role', 'order','note','auth_type',]
        

class Gropupdocumentfieldsresponse(serializers.ModelSerializer):
    recipient = RecipientSerializer(read_only=True) 
    class Meta:
        model = DocumentField
        fields = ['id', 'document',"value","positionX","positionY","width","height","page_no","field","recipient"] 
        
        
        
class DocumentSerializer(serializers.ModelSerializer):
    documentfield_document = Gropupdocumentfieldsresponse(many=True, read_only=True) 
    class Meta:
        model = Document
        fields = ['id', 'title','documentfield_document']




        
       

class ResponseDocumentGroupSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True) 
    group_recipients = RecipientSerializer(many=True,read_only=True) 
    class Meta:
        model = DocumentGroup
        fields = ['title','documents', 'status', 'note',  'signing_type', 'subject', 'message','document_type',"group_recipients",
                  "validity","days_to_complete","reminder_duration",   "auto_reminder",  'created_by', 'updated_by', 'created_by_date', 'updated_by_date' ]
        
        
        

          
class DocumentGroupSerializer(serializers.ModelSerializer):
    upload_documents = serializers.ListField(
        child=serializers.FileField(), required=False, write_only=True
    )
    documents = DocumentSerializer(many=True, read_only=True)  
    class Meta:
        model = DocumentGroup
        fields = ['id','title', 'status', 'note', 'documents', 'signing_type', 'subject', 'message', 'upload_documents',
                   "validity","days_to_complete","reminder_duration",   "auto_reminder",]
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
            file_content = file.read() 
            encoded_content = base64.b64encode(file_content).decode('utf-8')  
            document = Document.objects.create(
                title=file.name,
                # file_data=file.read(),  # Decode file as text
                # file_data=base64.b64encode(file.read()).decode('utf-8'),
                file_data = encoded_content,
                created_by=user,
                updated_by=user,
            )
            document_instances.append(document)

      
        document_group.documents.set(document_instances)

        return document_group

class DocumentsRecipientSerializer(serializers.ModelSerializer):
    document_group_id = serializers.IntegerField(write_only=True)
    recipients = RecipientSerializer(many=True, required=False, write_only=True)
    class Meta:
        model = Recipient 
        fields = ['id','document_group_id', 'recipients']
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
        
    def get_parent_instance(self,document_group_id):
        document_group_instance = DocumentGroup.objects.filter(id=document_group_id).first()
        return document_group_instance
    
    
    def validate(self, attrs):
        document_group_id = attrs.get("document_group_id")
        instance = self.get_parent_instance(document_group_id)

        if not instance:
            raise ValidationError("Invaild document group  id ")
        
        return super().validate(attrs)
        
    def create(self, validated_data):
        """
        Create recipients related to a document group.
        """
        recipients_data = validated_data.get('recipients', [])
        user = self.context['request'].user 
        document_group_id = validated_data.get("document_group_id")
        document_group_instance = self.get_parent_instance(document_group_id)

        created_recipients = []

        for recipient_data in recipients_data:
            recipient_data["created_by"] = user
            recipient_data["updated_by"] = user
            recipient_data["document_group"] = document_group_instance  # Associate with DocumentGroup

            # Create each recipient
            recipient = Recipient.objects.create(**recipient_data)
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
    document_group_id = serializers.IntegerField()
    fields = DocumentFieldSerializer(many=True)
    
    
    
    
    def get_realted_instance(self,document_group_id,document_id):
        document_group_instance = DocumentGroup.objects.filter(id=document_group_id).first()
        return document_group_instance
    
    
    
    def check_post_data(self,recipient_id,filed_id):
        recipient_instance = Recipient.objects.filter(id=recipient_id).first()

        if not recipient_instance:
            raise ValidationError("Invaild recipient Id")
        
        
        filed_instance = Field.objects.filter(id=filed_id).first()
        if not filed_instance:
            raise ValidationError("Invaild Field Id")
        
       

   
    def create(self, validated_data):
        document_group_id = validated_data['document_group_id']
        document_id = validated_data['document_id']
        fields_data = validated_data['fields']
        user = self.context['request'].user 
         
        document_fields = []
        for field_data in fields_data:
            check_post_data = self.check_post_data( field_data['recipient']['id'],field_data['field']['id'])
            if DocumentField.objects.filter(document_id=document_id,
                                            document_group = self.get_realted_instance(document_group_id,document_group_id),
                                            recipient_id=field_data['recipient']['id'],
                                            field_id=field_data['field']['id'],
                                           positionX=field_data['positionX'],
                                           positionY=field_data['positionY']).exists():
                
                raise ValidationError("Recipient with this document and field id is already exits")
            
            document_field = DocumentField(
                document_group = self.get_realted_instance(document_group_id,document_group_id),
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
        
####################################
class DocumentRecipients(serializers.ModelSerializer):
    class Meta:
        model = Recipient
        fields = ['id','name', 'email', 'role']
   
   
class SingleDoc(serializers.ModelSerializer):
    recipients = DocumentRecipients(many=True)
    class Meta:
        model = DocumentGroup
        fields = ['title', 'status', 'note',  'signing_type', 'subject', 'message','document_type','recipients']
           
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


################################
class DocumentSharedLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentSharedLink
        fields = '__all__'