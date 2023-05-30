import os

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect

from main.forms import UserlogoChangeForm, EmailChangeForm, UsernameChangeForm


@login_required(login_url='/login/')
def profile_page(request):
    context = {'username_change_form': UsernameChangeForm(instance=request.user),
               'email_change_form': EmailChangeForm(instance=request.user),
               'password_change_from': PasswordChangeForm(request.user),
               'logo_change_form': UserlogoChangeForm(),
              }
    return render(request, "profile.html", context)


@login_required(login_url='/login/')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Success!')
        else:
            messages.error(request, 'Error!')
    return redirect('/profile')


@login_required(login_url='/login/')
def change_logo(request):
    if request.method == 'POST':
        form = UserlogoChangeForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            if os.path.exists(request.user.logo_image.path):
                os.remove(request.user.logo_image.path)
            form.save()
            messages.success(request, 'Success!')
        else:
            messages.error(request, 'Error!')
    return redirect('/profile')


@login_required(login_url='/login/')
def change_email(request):
    if request.method == 'POST':
        user = request.user
        form = EmailChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success!')
        else:
            messages.error(request, 'Error!')
    return redirect('/profile')


@login_required(login_url='/login/')
def change_username(request):
    if request.method == 'POST':
        user = request.user
        form = UsernameChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Success!')
        else:
            messages.error(request, 'Error!')
    return redirect('/profile')
