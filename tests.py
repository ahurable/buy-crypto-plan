from django.test import TestCase
from rest_framework.test import APITestCase, force_authenticate
from rest_framework import status

from django.urls import reverse

from .models import *
# Create your tests here.


class UsersTest(APITestCase):

    def testCreateUser(self):
        # create user
        url = reverse('create-user-url')
        data = {
            'username':'test',
            'email':'test@gmail.com',
            'password':'test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    def testLoginUser(self):
        user = CustomUserModel()
        user.username = 'test'
        user.email = 'test@gmail.com'
        user.set_password('test')
        user.save()
        
        
        url = reverse('token-obtain')
        data = {
            'username': 'test',
            'password': 'test'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def testEmailOtpVerification(self):
        user = CustomUserModel()
        user.username = 'test'
        user.email = 'test@gmail.com'
        user.set_password('test')
        user.save()

        url = reverse('verify-otp')
        login_url = reverse('token-obtain')
        login_response = self.client.post(login_url, data={'username':'test', 'password':'test'}, format='json')
        print(login_response.data)
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + login_response.data["access"])
        
        otp = OtpEmail.objects.get(user__id=user.id).otp_code
        
        res = self.client.post(url, {'otp_code': int(otp)}, format='json')
        print(res.data)
        self.assertEqual(res.status_code, status.HTTP_202_ACCEPTED)

    
