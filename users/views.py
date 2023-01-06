from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from users.forms import LoginForm, RegisterForm
from django.contrib.auth.models import User
from users.utils import get_user_from_request
from django.views.generic import CreateView, ListView


# Create your views here.


class LoginViewCBV(CreateView):
    template_name = 'user/login.html'
    form_class = LoginForm
    success_url = '/products/'

    def get_context_data(self, **kwargs):
        return {
            'form': self.form_class
        }

    def post(self, request, *args, **kwargs):

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


class LogoutCBV(ListView):
    def get(self, request, **kwargs):
        logout(request)
        return redirect('/products/')


class RegisterCBV(CreateView):
    template_name = 'user/register.html'
    form_class = RegisterForm

    def get_context_data(self, **kwargs):
        return {
            'form': self.form_class
        }

    def post(self, request, *args, **kwargs):
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

        return render(request, self.template_name, context={
            'form': form,
            'user': get_user_from_request(request)
        })
