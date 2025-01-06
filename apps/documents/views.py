from django.shortcuts import render

# Create your views here.
from  apps.documents.models import Field,DocumentGroup,Document,Recipient,DocumentField,DocumentSharedLink

from rest_framework import viewsets
from rest_framework import generics
from apps.documents.serializers import FieldsSerializer,DocumentGroupSerializer,DocumentsRecipientSerializer,RecipientSerializer,ResponseDocumentGroupSerializer,CreateDocumentFieldBulkSerializer,UpdateDocumentsFieldsSerilalizer,SendDocumentSerializer,GenerateOtpTokenSerializer,VerifyOtpSerializer,GetSignRecipientDocumentFields,SignRecipientsFieldValueSerializer
from django.db.models import Q
from typing import List
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import base64
import os


import re
from apps.utils.utils import modify_pdf
from rest_framework.exceptions import NotFound
from django.contrib.auth import get_user_model
from apps.documents.email import send_otp_to_mail
from apps.documents.enum import DocumentValidity
from datetime import date, timedelta
from rest_framework.exceptions import NotFound, APIException
from apps.documents.utils import recipients_response

User = get_user_model() 
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
        
    
    

class GenerateOTPAPI(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializer = GenerateOtpTokenSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            token = serializer.validated_data.get('token')
            try:
                document_group = DocumentSharedLink.objects.get(token=token)
                print(document_group,"ksjkdjkdjdkjdskjdskjdsjdsjdjk")
                email = document_group.recipient.email
                otp = document_group.generate_otp()
                send_otp_to_mail(email,otp)
                return Response({"message": "OTP generated and sent successfully on your email."}, status=status.HTTP_201_CREATED)
            
            except DocumentSharedLink.DoesNotExist:
                raise NotFound(detail="Invalid token or document not found.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    
class VerifyOTPAPI(APIView):
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializer = VerifyOtpSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get('token')
            otp = serializer.validated_data.get('otp')
            try:
                document_shared_link = DocumentSharedLink.objects.get(token=token)               
                if document_shared_link.verify_otp(otp):
                    return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)

            except DocumentSharedLink.DoesNotExist:
                raise NotFound(detail="Invalid token or document not found.")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





    

class RecipientSignGetProgressDocumentAPI(APIView):
    permission_classes = []

    def get(self, request, token, *args, **kwargs):
        try:
            document_shared_link = DocumentSharedLink.objects.get(token=token)
            document_group = document_shared_link.document_group
            recipient = document_shared_link.recipient
            
            response = recipients_response(document_shared_link)
            if response["status"] != 200:
                return Response(response, status=400)

            recipient_obj = Recipient.objects.filter(document_group=document_group, id=recipient.id ).first()

            if not recipient_obj:
                raise NotFound(detail="Recipient not found in the specified document group.")

          

            serializer = GetSignRecipientDocumentFields(
                recipient_obj, 
                context={'document_group': document_group.id, 'recipient_id': recipient.id}
            )

            # Prepare response data
            response_data = {
                "status": 200,
                "message": "Recipient and document group fetched successfully.",
                "data": {
                
                    "recipient": serializer.data,
                },
            }
            return Response(response_data, status=200)

        except DocumentSharedLink.DoesNotExist:
            raise NotFound(detail="Invalid token or document group not found.")
        except Exception as e:
            raise APIException(detail=f"An unexpected error occurred: {str(e)}")

        
    




class SignUpdateRecipientsFieldValueAPI(APIView):
    """
    Updates the value of a field and checks if all fields assigned to the recipient are completed.
    """

    def post(self, request):
        serializer = SignRecipientsFieldValueSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
      
        data = serializer.validated_data
        document_field = data['document_field']
        recipient = data['recipient']
        document_group = data["document_group"]
        print("++++++++++++++",recipient.email)
        
        

        # Update the field value
        document_field.value = data['value']
        document_field.save()

        incomplete_fields = recipient.documentfield_recipient.filter(value__isnull=True,document_group=document_group)
        if not incomplete_fields.exists():
            document_group = recipient.document_group
            print(document_group)
            document_group.status = "COMPLETED"  
            document_group.save()
            completed_fields = recipient.documentfield_recipient.filter(value__isnull=False, document_group=document_group)
            completed_field_details = [
                {
                
                    "value": field.value,
                    "position_x": field.positionX,
                    "position_y": field.positionY,
                    "width": field.width,
                    "height": field.height
                }
                for field in completed_fields
            ]
            print(completed_field_details)
            recipient.is_recipient_sign =True
            recipient.save()
            
            
            return Response({
                "status": "success",
                "message": "All fields are completed. Document is marked as completed."
            }, status=status.HTTP_200_OK)

        return Response({
            "status": "incomplete",
            "message": "Fileds update Sucessfully , Some fields are still incomplete.",
            "incomplete_fields": [{"field_id": f.id, "field_name": f.field.name} for f in incomplete_fields]
        }, status=status.HTTP_200_OK)
        
        
        
        
        

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



