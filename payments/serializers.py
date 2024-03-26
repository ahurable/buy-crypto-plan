from rest_framework import serializers
from users.plans.serializers import PlanSerializer
from .models import Order

class PaymentSerializer(serializers.Serializer):

    plan = PlanSerializer()
    username = serializers.CharField()
    

class InvoiceDataSerializer(serializers.Serializer):
    address = serializers.CharField()
    app_id = serializers.UUIDField()
    confirm_speed = serializers.CharField()
    create_time = serializers.DateTimeField()
    error_status = serializers.CharField()
    exchange_rate = serializers.FloatField()
    expiration_time =  serializers.DateTimeField()
    invoice_id = serializers.UUIDField(format='hex')
    invoice_url = serializers.URLField()
    network = serializers.CharField()
    order_id = serializers.CharField()
    paid_amount = serializers.FloatField()
    pay_amount = serializers.FloatField()
    pay_currency = serializers.CharField()
    price_amount = serializers.FloatField()
    price_currency = serializers.CharField()
    status = serializers.CharField()




class InvoiceResponseSerializer(serializers.Serializer):
    code = serializers.CharField()
    data = InvoiceDataSerializer()
    msg = serializers.CharField()

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order()
        fields = serializers.ALL_FIELDS

class PlanIdSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class OrderIdSerializer(serializers.Serializer):
    order_id = serializers.CharField(max_length=6)