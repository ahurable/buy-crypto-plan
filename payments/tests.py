from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import CustomUserModel as User
from users.plans.models import PlanModel
from .serializers import OrderSerializer
from .models import Order
# Create your tests here.


class PaymentTest(APITestCase):

    def testCreateOrder(self):

        User.objects.create(username='test', email='test@mail.com', password='test')
        PlanModel.objects.create(title="test plan", description='test description', price=1.0)
        
        #  login 

        token = self.client.post(reverse('token-obtain'), data={
            'username':'test',
            'password':'test'
        })

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data['access'])
        order_res = self.client.post(reverse('create-order'), {
            'id':1
        }, format='json')
        print(order_res.json())

        self.assertEqual(order_res.status_code, status.HTTP_201_CREATED)

        

    def testPay(self):
        # create instances
        User.objects.create(username='test', email='test@mail.com', password='test')
        PlanModel.objects.create(title="test", description='test', price=0.6)
        Order.objects.create(order_id='df23k3', user=User.objects.get(id=1), plan=PlanModel.objects.get(id=1))
        
        # login

        token = self.client.post(reverse('token-obtain'), data={
            'username':'test',
            'password':'test'
        })

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token.data['access'])
        
        # test payment
        orde = Order.objects.get(id=1)
        res = self.client.post(reverse('create-invoice'), {
                'order_id':orde.order_id,
        }, format='json')

        print(res.json())