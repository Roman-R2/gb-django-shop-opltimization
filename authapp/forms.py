from datetime import timedelta

from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    UserChangeForm
from django.forms import forms, HiddenInput
from django.utils import timezone

from authapp.models import ShopUser
from authapp.services import get_user_activation_key


class ShopUserLoginForm(AuthenticationForm):
    class Meta:
        model = ShopUser
        fields = ('username', 'password',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class ShopUserRegisterForm(UserCreationForm):
    class Meta:
        model = ShopUser
        fields = (
            'username',
            'first_name',
            'email',
            'age',
            'avatar',
            'password1',
            'password2',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, *args, **kwargs) -> ShopUser:
        user = super().save(*args, **kwargs)
        user.is_active = False
        user.activation_key = get_user_activation_key(user.email)
        user.activation_key_expired = timezone.localtime() + timedelta(
            hours=settings.HOURS_BEFORE_ACTIVATION_KEY_EXPIRED
        )
        user.save()
        return user

    def clean_age(self):
        data_age = self.cleaned_data['age']
        if data_age < 18:
            raise forms.ValidationError('Вам мало лет.')
        return data_age

    def clean_email(self):
        data_email = self.cleaned_data['email']
        if ShopUser.objects.filter(email=data_email):
            raise forms.ValidationError(
                'Пользователь с таким email уже существует.'
            )
        return data_email


class ShopUserEditForm(UserChangeForm):
    class Meta:
        model = ShopUser
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'age',
            'avatar',
            'password',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if field_name == 'password':
                field.widget = HiddenInput()

    # def clean_email(self):
    #     data_email = self.changed_data['email']
    #     return data_email

    def clean_age(self):
        data_age = self.cleaned_data['age']
        if data_age < 18:
            raise forms.ValidationError('Вам мало лет')
        return data_age
