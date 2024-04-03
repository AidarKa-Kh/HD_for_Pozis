from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .form import RegisterCustomerForm


def register(request):
    if request.method == 'POST':
        form = RegisterCustomerForm(request.POST)
        if form.is_valid():
            var = form.save(commit=False)
            var.is_customer = True
            var.save()
            messages.info(request, 'Вы успешно зарегистрировались')
            return redirect('login')
        else:
            messages.warning(request, 'Что-то пошло не так... Проверьте правильность заполнения данных!')
            return redirect('register')
    else:
        form = RegisterCustomerForm()
        context = {'form': form}
        return render(request, 'users/register.html', context)


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            messages.info(request, 'Вы успешно авторизованы!')
            return redirect('dashboard')
        else:
            messages.warning(request, 'Что-то пошло не так..')
            return redirect('login')
    else:
        return render(request, 'users/login.html')


def logout_user(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')
