from django.contrib.auth.models import AbstractUser
from django.db import models


NULLABLE = {'blank': True, 'null': True}


class ShopUser(AbstractUser):
    avatar = models.ImageField(
        upload_to='users',
        blank=True,
        verbose_name='Аватар'
    )
    age = models.PositiveSmallIntegerField(default=18, verbose_name='Возраст')
    activation_key = models.CharField(max_length=128, **NULLABLE)
    activation_key_expired = models.DateTimeField(**NULLABLE)


class ShopUserProfile(models.Model):
    UNKNOWN = 'U'

    MALE = 'M'
    FEMALE = 'F'

    GENDERS = (
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
        (UNKNOWN, 'Неизвестно'),
    )

    RUS = 'Rus'
    ENG = 'Eng'
    ESP = 'Esp'

    LANGUAGE = (
        (RUS, 'Русский'),
        (ENG, 'English'),
        (ESP, 'Espaniol'),
        (UNKNOWN, 'Неизвестно'),
    )

    user = models.OneToOneField(
        ShopUser,
        unique=True,
        null=False,
        db_index=True,
        on_delete=models.CASCADE
    )
    tagline = models.CharField(
        max_length=128,
        verbose_name='Тэги',
        **NULLABLE
    )
    about_me = models.TextField(
        max_length=512,
        verbose_name='Обо мне',
        **NULLABLE,
    )
    gender = models.CharField(
        choices=GENDERS,
        default=UNKNOWN,
        max_length=1,
        verbose_name='Пол'
    )
    # language = models.CharField(max_length=20)




