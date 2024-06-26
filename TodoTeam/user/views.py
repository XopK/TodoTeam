from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.generic import UpdateView, DeleteView

from .forms import RegistrationForm, LoginForm, addTaskForm, editTaskForm
from django.contrib.auth import logout
from .models import Command, CommandUser
from .models import favorite as FavoriteModel
from task.models import Task, TaskStatus
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db.models import Q


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
            team_name = command.name_command
            q = request.GET.get('q')
            if q:
                tasks = Task.objects.filter(Q(title_task__startswith=q) | Q(description_task__startswith=q),
                                            command=command).order_by('-created_at')

            else:
                tasks = Task.objects.filter(command=command).order_by('-created_at')
            user_is_leader = command_user.is_leader
            team_members = CommandUser.objects.filter(command=command).values_list('user_id', flat=True)
            team_members = User.objects.filter(id__in=team_members)
            favorite_tasks = FavoriteModel.objects.filter(user=request.user)
            for task in tasks:
                if task in favorite_tasks:
                    task.is_favorite = True
                else:
                    task.is_favorite = False

                if task.status.name_task != 'Выполнено':
                    if task.date_task < datetime.now().date() or (
                            task.date_task == datetime.now().date() and task.task_time_end < datetime.now().time()):
                        task.status = TaskStatus.objects.get(name_task='Просрочено')
                        task.save()

                        if task.user_take is not None:
                            user_email = task.user_take.email

                            subject = 'Задача просрочена'
                            message = f'Задача "{task.title_task}" просрочена. Пожалуйста, выполните ее в ближайшее время.'

                            # Отправляем письмо
                            send_mail(
                                subject=subject,
                                message=message,
                                from_email=settings.EMAIL_HOST_USER,
                                recipient_list=[user_email],
                                fail_silently=False,
                            )
                        else:
                            print("task.user_take is None")

        else:
            tasks = []
            team_name = None
            user_is_leader = False
            team_members = []

        current_date = datetime.now()
        context = {
            'user_is_leader': user_is_leader,
            'tasks': tasks,
            'current_date': current_date,
            'team_name': team_name,
            'team_members': team_members,
        }
        return render(request, 'user/personalArea.html', context)
    else:
        return redirect('sign_in')


def favorite(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        if CommandUser.objects.filter(user_id=user_id).exists():
            command_user = CommandUser.objects.get(user_id=user_id)
            command = command_user.command
            team_name = command.name_command
            q = request.GET.get('q')
            favorite_tasks = FavoriteModel.objects.filter(user=request.user)
            if q:
                tasks = Task.objects.filter(Q(title_task__startswith=q) | Q(description_task__startswith=q),
                                            id__in=[f.task_id for f in favorite_tasks]).order_by('-created_at')

            else:
                tasks = Task.objects.filter(id__in=[f.task_id for f in favorite_tasks]).order_by('-created_at')
            user_is_leader = command_user.is_leader
            team_members = CommandUser.objects.filter(command=command).values_list('user_id', flat=True)
            team_members = User.objects.filter(id__in=team_members)
            for task in tasks:
                if task in favorite_tasks:
                    task.is_favorite = True
                else:
                    task.is_favorite = False

                if task.status.name_task != 'Выполнено':
                    if task.date_task < datetime.now().date() or (
                            task.date_task == datetime.now().date() and task.task_time_end < datetime.now().time()):
                        task.status = TaskStatus.objects.get(name_task='Просрочено')
                        task.save()

                        user_email = task.user_take.email

                        subject = 'Задача просрочена'
                        message = f'Задача "{task.title_task}" просрочена. Пожалуйста, выполните ее в ближайшее время.'

                        # Отправляем письмо
                        send_mail(
                            subject=subject,
                            message=message,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[user_email],
                            fail_silently=False,
                        )

        else:
            tasks = []
            team_name = None
            user_is_leader = False
            team_members = []

        current_date = datetime.now()
        context = {
            'user_is_leader': user_is_leader,
            'tasks': tasks,
            'current_date': current_date,
            'team_name': team_name,
            'team_members': team_members,
        }
        return render(request, 'user/favorite.html', context)
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
    if task.user_take is None:
        task.user_take = request.user
        task.status_id = 2
        task.save()
        success_message = "Вы успешно взяли задачу."
        messages.success(request, success_message)
        return redirect('personal_area')
    elif task.user_take == request.user or request.user.is_superuser:
        if task.status_id == 1:
            task.status_id = 2
            task.user_take = request.user
        elif task.status_id == 2:
            task.status_id = 3
        elif task.status_id == 3:
            task.status_id = 4
        else:
            task.status_id = 1
            task.user_take = None
        task.save()
        success_message = "Статус задачи успешно изменен."
        messages.success(request, success_message)
        return redirect('personal_area')
    else:
        error_message = "Вы не можете изменить статус этой задачи, так как она не была вами взята."
        messages.error(request, error_message)
        return redirect('personal_area')


class updateTaskView(UpdateView):
    model = Task
    form_class = editTaskForm
    template_name = 'user/edittask.html'
    success_url = 'personal_area'

    def form_valid(self, form):
        form.save()
        return redirect(self.success_url)


def delete_task(request, pk):
    task = Task.objects.get(id=pk)
    task.delete()
    return redirect('personal_area')


def addFavorite(request, pk):
    if request.user.is_authenticated:
        task = Task.objects.get(id=pk)
        favorite_exists = FavoriteModel.objects.filter(user=request.user, task=task).exists()
        if favorite_exists:
            FavoriteModel.objects.filter(user=request.user, task=task).delete()
        else:
            favorite = FavoriteModel()
            favorite.task = task
            favorite.user = request.user
            favorite.save()
        return redirect('personal_area')
    else:
        return redirect('sign_in')
