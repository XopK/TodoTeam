import datetime
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import RegistrationForm, LoginForm, addTaskForm
from django.contrib.auth import logout
from .models import Command, CommandUser
from task.models import Task
from django.contrib.auth.decorators import login_required


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
                    return redirect('personal_area')
            else:
                form.add_error(None, 'Проверьте введеные данные!')
    else:
        form = LoginForm()
    return render(request, 'user/entrance.html', {'form': form})


def personalArea(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        if CommandUser.objects.filter(user_id=user_id).exists():
            command_user = CommandUser.objects.get(user_id=user_id)
            command = command_user.command
            tasks = Task.objects.filter(command=command)
            user_is_leader = command_user.is_leader
        else:
            tasks = []
            user_is_leader = False

        current_date = datetime.datetime.now()
        return render(request, 'user/personalArea.html',
                      {'user_is_leader': user_is_leader, 'tasks': tasks, 'current_date': current_date})
    else:
        return redirect('sign_in')


@login_required
def addtask(request):
    if request.method == 'POST':
        form = addTaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.command = Command.objects.get(user=request.user)
            task.status_id = 1
            task.save()
            return redirect('personal_area')
    else:
        form = addTaskForm()

    return render(request, 'user/addtask.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def change_status(request, pk):
    task = Task.objects.get(id=pk)
    if task.status_id == 1:
        task.status_id = 2
    elif task.status_id == 2:
        task.status_id = 3
    elif task.status_id == 3:
        task.status_id = 4
    else:
        task.status_id = 1
    task.save()
    return redirect('personal_area')
