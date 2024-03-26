from django.db import models
from ..models import CustomUserModel
# Create your models here.


class PlanModel(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.FloatField()
    
    def __str__(self):
        return self.title + " " + str(self.price)

class PlanForUser(models.Model):
    plan = models.OneToOneField(PlanModel, on_delete=models.CASCADE)
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE)
    # expiration_date = models.DateTimeField()
    def __str__(self):
        return self.plan.title + " " + self.user.username