from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from users.utils import get_user_from_request


# Create your views here.

def login_view(request):
    if request.method == 'GET':
        context = {
            'form': LoginForm,
            'user': get_user_from_request(request)
        }

        return render(request, 'user/login.html', context=context)

    if request.method == 'POST':
        form = LoginForm(data=request.POST)

        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data.get('username'),
                password=form.cleaned_data.get('password')
            )

            if user:
                login(request, user=user)
                return redirect('/products/')
            else:
                form.add_error('username', 'bad request!')

        return render(request, 'user/login.html', context={
            'form': form,
            'user': get_user_from_request(request)
        })


def logout_view(request):
    logout(request)
    return redirect('/products/')


def register_view(request):
    if request.method == 'GET':
        context = {
            'form': RegisterForm,
            'user': get_user_from_request(request)
        }
        return render(request, 'user/register.html', context=context)

    if request.method == 'POST':
        form = RegisterForm(data=request.POST)

        if form.is_valid():
            if User.objects.filter(username__exact=form.cleaned_data.get('username')).exists():
                form.add_error('username', 'username already taken!')
            elif form.cleaned_data.get('password1') == form.cleaned_data.get('password2'):
                user = User.objects.create_user(
                    username=form.cleaned_data.get('username'),
                    password=form.cleaned_data.get('password2')
                )
                login(request, user)
                return redirect('/products/')
            else:
                form.add_error('password2', 'bad request!')

        return render(request, 'user/register.html', context={
            'form': form,
            'user': get_user_from_request(request)
        })