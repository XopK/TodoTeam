from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm


# Create your views here.
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
    form = RegistrationForm()
    return render(request, 'user/entrance.html', {'form':form})
