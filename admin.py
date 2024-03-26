from django.contrib import admin
from .models import CustomUserModel, OtpEmail
from .plans.models import PlanForUser, PlanModel
# Register your models here.


admin.site.register(CustomUserModel)
admin.site.register(OtpEmail)
admin.site.register(PlanModel)
admin.site.register(PlanForUser)