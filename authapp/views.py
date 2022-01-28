from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, \
    ShopUserEditForm, EditProfileForm
from authapp.models import ShopUser
from authapp.services import check_next_in_request, send_verify_mail, \
    is_activation_key_expired


def login(request):
    login_form = ShopUserLoginForm(data=request.POST)
    next_url = request.GET.get('next', '')

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)

            if check_next_in_request(request):
                return HttpResponseRedirect(request.POST['next'])
            return redirect('mainapp:index')

    context = {
        'login_form': login_form,
        'next': next_url,
    }

    return render(request, 'authapp/login.html', context=context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('mainapp:index'))


@login_required
def edit(request):
    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES,
                                     instance=request.user)
        edit_profile_form = EditProfileForm(
            request.POST,
            instance=request.user.shopuserprofile
        )
        if edit_form.is_valid() and edit_profile_form.is_valid():
            edit_form.save()
            return redirect('mainapp:index')
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        edit_profile_form = EditProfileForm(
            instance=request.user.shopuserprofile
        )
    context = {
        "edit_form": edit_form,
        "edit_profile_form": edit_profile_form,
    }

    return render(request, 'authapp/edit.html', context=context)


def register(request):
    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)
        if register_form.is_valid():
            user = register_form.save()
            send_verify_mail(user)
            return redirect('mainapp:index')
    else:
        register_form = ShopUserRegisterForm()
    context = {
        "register_form": register_form,
    }

    return render(request, 'authapp/register.html', context=context)


def verify(request, email, activation_key):
    user = ShopUser.objects.filter(email=email).first()
    print("user.activation_key_expired ---> ", user.activation_key_expired)
    if user.activation_key is None:
        return render(request, 'authapp/verify.html', context={
            'already_activate': True})

    if user:
        if user.activation_key == activation_key and \
                not is_activation_key_expired(user.activation_key_expired):
            user.is_active = True
            user.activation_key = None
            user.activation_key_expired = None
            user.save()
            auth.login(
                request,
                user,
                backend='django.contrib.auth.backends.ModelBackend'
            )
    return render(request, 'authapp/verify.html')
