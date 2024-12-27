from django.shortcuts import render

# Create your views here.
from  apps.documents.models import DocumentField,DocumentGroup,Document

from rest_framework import viewsets
from rest_framework import generics
from apps.documents.serializers import DocumentsFieldsSerializer,DocumentGroupSerializer
from django.db.models import Q
from typing import List
from rest_framework.response import Response
from rest_framework import status

class DocumentFieldAPI(viewsets.ModelViewSet):
    serializer_class = DocumentsFieldsSerializer
    http_method_names: List[str] = ["get", "post"]

    def get_queryset(self):
        return DocumentField.objects.all()
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(created_by=user, updated_by=user)
        
        


class DocumentGroupViewSet(viewsets.ModelViewSet):
    queryset = DocumentGroup.objects.all()
    serializer_class = DocumentGroupSerializer
    def create(self, request, *args, **kwargs):
        # Extract the data from the request
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            document_group = serializer.save()
            response_serializer = self.get_serializer(document_group)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)