from django.shortcuts import render

# Create your views here.
from  apps.documents.models import Field,DocumentGroup,Document,Recipient,DocumentField,DocumentSharedLink

from rest_framework import viewsets
from rest_framework import generics
from apps.documents.serializers import FieldsSerializer,DocumentGroupSerializer,DocumentsRecipientSerializer,RecipientSerializer,ResponseDocumentGroupSerializer,CreateDocumentFieldBulkSerializer,SingleDocumentSerializerResponse,UpdateDocumentsFieldsSerilalizer,SendDocumentSerializer
from django.db.models import Q
from typing import List
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import base64
import os
from django.utils.timezone import now

import re
from apps.utils.utils import modify_pdf
from rest_framework.exceptions import NotFound
class DocumentFieldAPI(viewsets.ModelViewSet):
    serializer_class = FieldsSerializer
    http_method_names: List[str] = ["get", "post"]

    def get_queryset(self):
        return Field.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user, updated_by=user)
        
    
class DocumentGroupViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentGroupSerializer

    def get_serializer(self, *args, **kwargs):
        if self.request.method in ["POST"]:
            serializer_class = self.get_serializer_class()
        else:
            serializer_class = ResponseDocumentGroupSerializer

        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)
    
    
    def create(self, request, *args, **kwargs):
        # Extract the data from the request
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            document_group = serializer.save()
            response_serializer = self.get_serializer(document_group)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        return  DocumentGroup.objects.all()
    
    
class DocumentsAssignRecipientAPI(viewsets.ModelViewSet):
    serializer_class = DocumentsRecipientSerializer
    queryset = ""
    def create(self, request, *args, **kwargs):
        # Extract the data from the request
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            created_recipients = serializer.save()  
            recipient_serializer = RecipientSerializer(created_recipients, many=True)
            context = {
                "recipints":recipient_serializer.data,
                "message": "Recipient add sucessfully"      
            }
            return Response(context, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

        
class RemoveRecipientsAPI(APIView):
    def delete(self, request, grp_id, rec_id, *args, **kwargs):
        print("Received DELETE request for group ID:", grp_id, "and recipient ID:", rec_id)

        # Example logic: Delete the recipient
        try:
            recipient = Recipient.objects.get(id=rec_id, document_group_id=grp_id)
            recipient.delete()
            return Response({"message": f"Recipient {rec_id} in group {grp_id} deleted successfully."}, status=200)
        except Recipient.DoesNotExist:
            return Response({"error": "Recipient not found."}, status=404)


        
class DocumentFieldCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CreateDocumentFieldBulkSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Document fields created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def put(self, request, *args, **kwargs):
        field_id = request.query_params.get('field_id')
        document_id = request.query_params.get('document_id')  #
        recipient_id = request.query_params.get('recipient_id') 
        document_group = request.query_params.get('document_group_id')
        try:
            document_field = DocumentField.objects.get(id=field_id, document=document_id, recipient=recipient_id,document_group=document_group)
        except DocumentField.DoesNotExist:
            return Response({"message": "Document field not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UpdateDocumentsFieldsSerilalizer(document_field, data=request.data, context={'request': request})
    
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "Document field updated successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
               
                return Response({"message": "An error occurred while updating the document field."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, *args, **kwargs):
        document_group = request.query_params.get('document_group_id')
        field_id = request.query_params.get('field_id')
        document_id = request.query_params.get('document_id')  # document_id from query params
        recipient_id = request.query_params.get('recipient_id')

        try:
            document_field = DocumentField.objects.get(id=field_id, document=document_id, recipient=recipient_id,document_group=document_group)
        except DocumentField.DoesNotExist:
            return Response({"message": "Document field not found."}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Delete the document field
            document_field.delete()
            return Response({"message": "Document field deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"message": "An error occurred while deleting the document field."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    
class GetRecipientsDocuments(APIView):
    def get(self, request, document_group_id, *args, **kwargs):
        try:
            document_group = DocumentGroup.objects.get(id=document_group_id)
            serializer = ResponseDocumentGroupSerializer(document_group)     
            return Response(serializer.data)

        except DocumentGroup.DoesNotExist:
            raise NotFound(detail="DocumentGroup not found")
        
        
 
class SendDocumentToRecipient(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SendDocumentSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Document fields created and emails sent successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    
    

class RecipientSignGetProgressDocumentAPI(APIView):
    def get(self, request, token, *args, **kwargs):
        try:
            document_group = DocumentSharedLink.objects.get(token=token)
            # Check OTP status
            otp_status = None
            if document_group.otp_expiry and document_group.otp_expiry < now():
                otp_status = "expired"  # OTP expired, prompt user to regenerate it

            # Return the document and OTP status
            serializer = ResponseDocumentGroupSerializer(document_group.document_group)
            return Response({
                "document": serializer.data,
                "otp_status": otp_status,
                "otp_expiry": document_group.otp_expiry,  # Return expiry time for frontend
            })
        
        except DocumentSharedLink.DoesNotExist:
            raise NotFound(detail="DocumentSharedLink not found")
    
    def post(self, request, token, *args, **kwargs):
        """Generate or refresh OTP if expired."""
        try:
            document_group = DocumentSharedLink.objects.get(token=token)

            # If OTP expired, regenerate it
            if document_group.otp_expiry and document_group.otp_expiry < now():
                document_group.generate_otp()
                # Optionally, send the OTP to the user via email/SMS
                return Response({"message": "OTP has expired. A new OTP has been sent."})

            # If OTP is still valid, do not regenerate
            return Response({"message": "OTP is still valid."})
        
        except DocumentSharedLink.DoesNotExist:
            raise NotFound(detail="DocumentSharedLink not found")

        
    

class RecipientUpdatedDocumentAPI(APIView):
    def is_base64(self, string):
        try:
            # Try decoding the string
            base64.b64decode(string)
            # Also, check if it matches the general base64 pattern (optional)
            return bool(re.match(r'^[A-Za-z0-9+/=]+$', string))
        except Exception:
            return False
        
    def get(self, request, *args, **kwargs):
        try:
            document_group = Document.objects.get(id=9)
            pdf_bytes = base64.b64decode(document_group.file_data) 

            # Fetch the signed document (image) from the database
            sign = Document.objects.get(id=10)
            value = sign.file_data
            positionX = 60
            positionY = 60
            page_number =1
            
            if self.is_base64(value):
                value = base64.b64decode(value)
                is_image = True
                modify_pdf(positionX,positionY,page_number,pdf_bytes,is_image,value)
                # pass
            else:
                is_image = False
                modify_pdf(positionX,positionY,page_number,pdf_bytes,is_image,value)

            context = {
                "message": "Your document has been updated successfully."
            }
            return Response(context)

        except Document.DoesNotExist:
            raise Response("Document not found")



