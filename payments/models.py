from django.db import models
from users.plans.models import PlanModel
from users.models import CustomUserModel as User

# Create your models here.


# class Withdrawal(models.Model):
#     plan = models.OneToOneField(PlanModel)
#     user = models.OneToOneField(User)

class Order(models.Model):
    order_id = models.CharField(unique=True, max_length=10)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(PlanModel, on_delete=models.CASCADE)
    confirmed = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.order_id