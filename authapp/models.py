from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

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
    MALE = 'M'
    FEMALE = 'F'
    UNKNOWN = 'U'

    GENDERS = (
        (MALE, 'Мужчина'),
        (FEMALE, 'Женщина'),
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

    @receiver(post_save, sender=ShopUser)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            ShopUserProfile.objects.create(user=instance)

    @receiver(post_save, sender=ShopUser)
    def save_user_profile(sender, instance, **kwargs):
        instance.shopuserprofile.save()
