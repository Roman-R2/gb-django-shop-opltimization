from django.dispatch import receiver
from django.db.models.signals import post_save

from authapp.models import ShopUser, ShopUserProfile


@receiver(post_save, sender=ShopUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ShopUserProfile.objects.create(user=instance)


@receiver(post_save, sender=ShopUser)
def save_user_profile(sender, instance, **kwargs):
    instance.shopuserprofile.save()
