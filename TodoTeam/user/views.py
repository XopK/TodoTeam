from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            return redirect('/user/sign_in')
    else:
        form = RegistrationForm()
    return render(request, 'user/Registration.html', {'form': form})


def entrance(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admin:index')
                else:
                    return redirect('/')
            else:
                form.add_error(None, 'Проверьте введеные данные!')
    else:
        form = LoginForm()
    return render(request, 'user/entrance.html', {'form': form})

def personalArea(request):
    return render(request, 'user/personalArea.html')