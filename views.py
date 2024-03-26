from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CreateUserSerializer, GetOtpSerializer, UserRetrieveUpdateSerializer
from rest_framework.permissions import IsAuthenticated
from .models import CustomUserModel as User
from rest_framework import serializers
from urllib.parse import urlencode
from django.shortcuts import redirect
from django.conf import settings
from .utils import google_get_access_token, google_get_user_info, generate_otp
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import send_mail
from rest_framework.generics import RetrieveUpdateAPIView
# Create your views here.


class UserRetrieveUpdateView(APIView):

    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = UserRetrieveUpdateSerializer(user)
        return Response(data=serializer.data, status=200)


class CreateUserView(APIView):

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'Success':"You've been created account with successfully"}, status=201)
        else:
            return Response({'Error':'something went wrong check your username or email maybe it\'s already in use'}, status=409)

class ChangeUsernameView(APIView):
    permission_classes = [IsAuthenticated]

    class ChangeUserSerializer(serializers.Serializer):
        username = serializers.CharField()

    def post(self, request):
        serializer = self.ChangeUserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            user.username = serializer.data['username']
            user.save()
            return Response({"Success": "your username has been updated"}, status=201)
        else:
            return Response({"err":"Unexpected data kind"}, status=406)

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    class NewPasswordSerializer(serializers.Serializer):
        password = serializers.CharField()
        newpassword = serializers.CharField()
        confirmpassword = serializers.CharField()

        def validate(self, attrs):
            if attrs['newpassword'] != attrs['confirmpassword']:
                raise serializers.ValidationError("password and it's repeat is not same")
            return attrs

    def post(self, request):
        user = User.objects.get(id=request.user.id)
        serializer = self.NewPasswordSerializer(data=request.data)
        
        if serializer.is_valid():
            print(serializer.data)
            if user.check_password(serializer.data['password']):
                user.set_password(serializer.data['newpassword'])
                user.save()
                return Response({"Success": "Your password changed successfully"}, status=201)
            else:
                return Response({"Error":"The password you entered is not same as the password you have currently!"}, status=401)
        else:
            return Response({"Error": "The new password and it's reqeat is not same!"}, status=406)


class SendOtpEmailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if not request.user.is_email_verified:
            user = User.objects.get(id=request.user.id)
            otp_code = generate_otp(user)
            send_mail(subject='OTP Code', message=f"Your otp code is {otp_code}", from_email='settings.EMAIL_HOST_USER', recipient_list=[request.user.email])
            return Response({'success':'The otp code sent to your email address'}, status=200)
        return Response({'error':'Your email verified already!'}, status=403)


class VerifyOtpView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = GetOtpSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.get(id=request.user.id)
            db_otp = user.otp_tab.otp_code

            if serializer.data['otp_code'] == db_otp:
                user.is_email_verified = True
                user.save()
                
                return Response({"activated":"user have been activated"}, status=202)
            else:
                return Response({"error":"your otp code is not same"}, status=403)
            


def generate_token_for_user(user):
    serializer = TokenObtainPairSerializer()
    token_data = serializer.get_token(user)
    access_token = token_data.access_token
    refresh_token = token_data
    return access_token, refresh_token


class GoogleLoginApiView(APIView):
    class InputSerializer(serializers.Serializer):
        access_token = serializers.CharField(required=False)

    def get(self, request, *args, **kwargs):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        access_token = validated_data.get('access_token')
        print("your access token is : " + access_token)

        login_url = f'{settings.FRONTEND_URL}/login'

        if not access_token:
            params = urlencode({'error':'something went wrong in google authentication'})
            return redirect(f'{login_url}?{params}')
        

        user_data = google_get_user_info(access_token=access_token)

        try:
            user = User.objects.get(email=user_data['email'])
            access_token, refresh_token = generate_token_for_user(user)
            response_data = {
                'access': str(access_token),
                'refresh': str(refresh_token)
            }
            return Response(response_data)
        except User.DoesNotExist:
            username = user_data['email'].split('@')[0]
            email = user_data['email']

            user = User.objects.create(
                username=username,
                email=email,
                register_method = 'google'
            )

            access_token, refresh_token = generate_token_for_user(user)
            
            return Response({'access':str(access_token), 'refresh':str(refresh_token)})
        
