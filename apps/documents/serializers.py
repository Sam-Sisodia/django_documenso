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


class DocumentGroupSerializer(serializers.ModelSerializer):
    documents = serializers.ListField(
        child=serializers.FileField(), required=False, write_only=True
    )
    groups_documents = DocumentSerializer(many=True, read_only=True)


    class Meta:
        model = DocumentGroup
        fields = ['title', 'status', 'note', 'documents', 'signing_type', 'subject', 'message','groups_documents']
        extra_kwargs = {
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }

    def create(self, validated_data):
        uploaded_files = validated_data.pop('documents', [])
        user = self.context['request'].user

        document_group = DocumentGroup.objects.create(
            created_by=user,
            updated_by=user,
            **validated_data
        )

        for file in uploaded_files:
            Document.objects.create(
                document_group=document_group,
                title=file.name,
                file_data=file.read(),
                created_by=user,
                updated_by=user,
            )

        return document_group
    
    # def to_representation(self, instance):
    #     """Customize the serialized output."""
    #     representation = super().to_representation(instance)
    #     representation['hello'] = "Hello, thanks!"
    #     return representation



        
