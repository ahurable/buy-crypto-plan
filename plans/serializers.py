from .models import PlanModel
from rest_framework import serializers


class PlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanModel()
        fields = '__all__'

