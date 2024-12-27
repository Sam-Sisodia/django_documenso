
from  apps.users.models import User

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError




class LoginSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token


class RegisterAPISerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        label=_("Password"), style={"input_type": "password"}, write_only=True
    )
    
    signature = serializers.CharField(required=False, allow_blank=True)

  
    class Meta:
        model = User
        fields = ["username","email", "password", "signature"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email is already in use")
        return value
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user