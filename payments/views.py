from django.shortcuts import render
from rest_framework.views import APIView
from unipayment import UniPaymentClient, CreateInvoiceRequest
from rest_framework.permissions import IsAuthenticated
from .serializers import OrderIdSerializer, PlanIdSerializer
from rest_framework import serializers
from .models import Order
import os
from dotenv import load_dotenv
from django.urls import reverse
import random
import string
from users.models import CustomUserModel as User
from .models import PlanModel
from rest_framework.response import Response
# Create your views here.

load_dotenv('../../.env')

class CreateOrder(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        plan_id = PlanIdSerializer(data=request.data)
        if plan_id.is_valid():

            order = Order()
            order.order_id = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))
            order.user = User.objects.get(id = request.user.id)
            order.plan = PlanModel.objects.get(id=plan_id.data['id'])
            order.save()
            return Response({'msg':'order created with successfully'}, status=201)

class IPNView(APIView):
    def post(self, request):
        return Response({'ok':'got it'})

class CreateInvoiceView(APIView):
    permission_classes = [IsAuthenticated]
    client = UniPaymentClient(client_id=os.getenv('CLIENT_ID'), client_secret=os.getenv('CLIENT_SECRET'))
    def post(self, request):
        order_serializer = OrderIdSerializer(data=request.data)
        if order_serializer.is_valid():
            instance = Order.objects.get(order_id=order_serializer.data['order_id'])
            print('app id is : ' + str(os.getenv('APP_ID')))
            plan = PlanModel.objects.get(id=instance.plan.pk)
            w_request = CreateInvoiceRequest()
            w_request.app_id = os.getenv('APP_ID')
            w_request.price_amount = plan.price
            w_request.price_currency = 'USD'
            w_request.order_id = order_serializer.data['order_id']
            w_request.title = plan.title
            w_request.pay_currency = 'USDT'
            res = self.client.create_invoice(w_request)
            print("response is: " + str(res))

            return Response({"data":"OK"})
        return Response({'error':'something went wrong'})
    
