from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from .models import CustomUserModel
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework_simplejwt.tokens import Token

class CreateUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'password']



class UserLoginSerializer(Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class GetOtpSerializer(Serializer):
    otp_code = serializers.CharField(max_length=6)


class CusTokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user) -> Token:
        token = super().get_token(user)
        token['is_email_verified'] = user.is_email_verified
        token['username'] = user.username
        return token
    

class UserRetrieveUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        fields = ['username', 'email', 'join_date', 'is_email_verified', 'register_method']