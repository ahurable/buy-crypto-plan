from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save
from random import randint
# Create your models here.



class CustomUserManager(BaseUserManager):

    def create_user(self, username, email, password=None, **extra_fields):
        user = self.model(
            username= username,
            email=email,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username, email, password=None, **extra_fields):
        user = self.create_user(username=username, email=email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user
    
    def create(self, username, email, password=None, **extra_fields):
        user = self.create_user(username=username, email=email, password=password)
        return user



class CustomUserModel(AbstractBaseUser):

    username = models.CharField(max_length=250, unique=True)
    email = models.CharField(max_length=250)
    join_date = models.DateTimeField(auto_now_add=True)
    
    REGISTERATION_CHOICES = [
        ('email', 'Email'),
        ('gmail', 'Gmail'),
    ]
    register_method = models.CharField(max_length=10, choices=REGISTERATION_CHOICES, default='email')

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.username
    
    def has_perm(self, perm, obj=None) :
        return self.is_admin
    
    def has_module_perms(self, perm):
        return self.is_admin
    
    @property
    def is_staff(self):
        return self.is_admin
    
    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'



class OtpEmail(models.Model):
    otp_code = models.CharField(max_length=6)
    user = models.OneToOneField(CustomUserModel, on_delete=models.CASCADE, related_name="otp_tab")

    def __str__(self) -> str:
        return self.user.username + " " + self.otp_code
    
    @receiver(post_save, sender=CustomUserModel)
    def create_otp(sender, instance, created, **kwargs):
        if created:
            OtpEmail.objects.create(user=instance, otp_code=randint(100000, 999999))

    @receiver(post_save, sender=CustomUserModel)
    def save_otp(sender, instance, created, **kwargs):
        if created:
            instance.otp_tab.save()

