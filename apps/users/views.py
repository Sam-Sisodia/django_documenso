from django.shortcuts import render
from apps.users.serializers import (
    RegisterAPISerializer,
    LoginSerializer)

# Create your views here.

from rest_framework import viewsets
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response


from rest_framework_simplejwt.views import TokenObtainPairView



class LoginAPIView(TokenObtainPairView):
    """
    API view for user login.
    """

    serializer_class = LoginSerializer
    permission_classes = []


class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterAPISerializer
    permission_classes = ()
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        refresh = LoginSerializer.get_token(serializer.instance)
        data = {**serializer.data}
        data["id"] = serializer.instance.id
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    # def get_tokens_for_use(self, user):
    #     refresh = RefreshToken.for_user(user)
    #     return {
    #         "refresh": str(refresh),
    #         "access": str(refresh.access_token),
    #     }

