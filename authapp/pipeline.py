from datetime import datetime

import requests
from django.conf import settings
from social_core.exceptions import AuthForbidden

from authapp.utils import ChoiceFor


def get_json_response_from_vk_api(response, base_url, fields_for_request, ):
    params = {
        'fields': ','.join(fields_for_request),
        'access_token': response['access_token'],
        'v': settings.API_VERSION
    }

    api_response = requests.get(base_url, params=params)

    if api_response.status_code != 200:
        return False

    return api_response.json()


def save_user_profile(backend, user, response, *args, **kwargs):
    # Ели это не сеть vk, то данный pipeline нам не подходтит
    if backend.name != 'vk-oauth2':
        return

    api_data = get_json_response_from_vk_api(
        response,
        'https://api.vk.com/method/users.get/',
        ['bdate', 'sex', 'about', 'photo_200']
    )['response'][0]

    if 'sex' in api_data:
        if api_data['sex'] == 1:
            user.shopuserprofile.gender = ChoiceFor.FEMALE
        elif api_data['sex'] == 2:
            user.shopuserprofile.gender = ChoiceFor.MALE
        else:
            user.shopuserprofile.gender = ChoiceFor.UNKNOWN

    if 'about' in api_data:
        user.shopuserprofile.about_me = api_data['about']

    if 'bdate' in api_data:
        bdate = datetime.strptime(api_data['bdate'], '%d.%m.%Y').date()
        age = datetime.now().year - bdate.year
        if age < 18:
            user.delete()
            raise AuthForbidden('social_core.backends.vk.VKOAuth2')

        user.age = age

    if 'photo_200' in api_data:
        user.shopuserprofile.vk_avatar = api_data['photo_200']

    user.save()
