import hashlib
from random import random

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils import timezone

from authapp.models import ShopUser


def check_next_in_request(request):
    """
    Проверяет наличие слова 'next' в объекте запроса request методе POST
    :param request:
    :return:
    """
    return True if 'next' in request.POST else False


def get_user_activation_key(user_email):
    """
    Вернет ключ активации для регистрации пользователя
    """
    salt = hashlib.sha1(str(random())
                        .encode('utf8')).hexdigest()[:6]
    return hashlib.sha1((user_email + salt)
                        .encode('utf8')).hexdigest()


def is_activation_key_expired(expired_date):
    """
    Проверит, истекло ли время ключа активации пользователя при
    регистрации
    """
    if not expired_date:
        return True
    return timezone.now() > expired_date


def send_verify_mail(user: ShopUser):
    """
    Формирует письмо и отправляет его с кодом активации
    """
    verify_link = reverse(
        'authapp:verify',
        args=[user.email, user.activation_key]
    )
    subject = 'Активация аккаунта'
    message = f'{settings.BASE_URL}{verify_link}'
    return send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )
