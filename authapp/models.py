from django.contrib.auth.models import AbstractUser
from django.db import models


class ShopUser(AbstractUser):
    avatar = models.ImageField(upload_to='users', blank=True)
    age = models.PositiveSmallIntegerField(default=18, verbose_name='Возраст')
    activation_key = models.CharField(max_length=128, blank=True, null=True)
    activation_key_expired = models.DateTimeField(blank=True, null=True)
