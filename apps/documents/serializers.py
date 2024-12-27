from rest_framework import serializers
from apps.documents.models import DocumentField ,Document,DocumentGroup # Import the DocumentField model

class DocumentsFieldsSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)  # Define the 'name' field
    
    class Meta:
        model = DocumentField  # Specify the model
        fields = ["id", "name"]  # Define which fields to include in the serializer




class ResponseDocumentGroupSerializer(serializers.ModelSerializer):
    # qr_category = serializers.CharField(source="category")

    class Meta:
        model = DocumentGroup
        fields = ['title', 'status', 'note',  'signing_type', 'subject', 'message',]
       



class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'title', 'file_data']


# class DocumentGroupSerializer(serializers.ModelSerializer):
#     upload_documents = serializers.ListField(
#         child=serializers.FileField(), required=False, write_only=True
#     )
    


#     class Meta:
#         model = DocumentGroup
#         fields = ['title', 'status', 'note', 'documents', 'signing_type', 'subject', 'message','upload_documents']
#         extra_kwargs = {
#             'created_by': {'read_only': True},
#             'updated_by': {'read_only': True},
#             'created_at': {'read_only': True},
#             'updated_at': {'read_only': True},
#         }

#     def create(self, validated_data):
#         uploaded_files = validated_data.pop('upload_documents', [])
#         user = self.context['request'].user
     
#         document_group = DocumentGroup.objects.create(
#             created_by=user,
#             updated_by=user,
#             **validated_data
#         )
#         document_instances = []
    
#         # for file in uploaded_files:
#         #    document = Document.objects.create(
#         #         title=file.name,
#         #         file_data=file.read(),
#         #         created_by=user,
#         #         updated_by=user,
#         #     )
#         #    document_instances.append(document)
            
#         # document_group.documents.set(document_instances)
#         # return document_group
    
    
    
    
#     # def to_representation(self, instance):
#     #     """Customize the serialized output."""
#     #     representation = super().to_representation(instance)
#     #     representation['hello'] = "Hello, thanks!"
#     #     return representation



class DocumentGroupSerializer(serializers.ModelSerializer):
    upload_documents = serializers.ListField(
        child=serializers.FileField(), required=False, write_only=True
    )
    documents = DocumentSerializer(many=True, read_only=True)  

    class Meta:
        model = DocumentGroup
        fields = ['title', 'status', 'note', 'documents', 'signing_type', 'subject', 'message', 'upload_documents']
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        # Extract files from validated_data and remove 'upload_documents'
        uploaded_files = validated_data.pop('upload_documents', [])
        user = self.context['request'].user

        # Manually handle the fields one by one
        title = validated_data.get('title', '')
        status = validated_data.get('status', 'draft')  # Default to 'draft'
        note = validated_data.get('note', '')
        signing_type = validated_data.get('signing_type', 'parallel')  # Default to 'parallel'
        subject = validated_data.get('subject', '')
        message = validated_data.get('message', '')

        # Step 1: Create the DocumentGroup instance
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
