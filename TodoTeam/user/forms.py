from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm, TextInput, Textarea, DateInput, TimeInput
from task.models import Task


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30,
        required=True
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=100,
        required=True
    )
    email = forms.EmailField(
        label='Почта',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        max_length=254,
        required=True,
    )
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    password2 = forms.CharField(
        label='Подтверждение пароля',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )

    password = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )


class addTaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ('title_task', 'description_task', 'date_task', 'task_time_start', 'task_time_end')

        widgets = {
            "title_task": TextInput(
                attrs={
                    "class": "form-control",
                    "id": "title_task",
                }
            ),
            "description_task": Textarea(
                attrs={
                    "class": "form-control",
                    "id": "description_task",
                }
            ),
            "date_task": DateInput(
                attrs={
                    "class": "form-control",
                    "id": "date_task",
                    'type': 'date'
                }
            ),
            "task_time_start": TimeInput(
                attrs={
                    "class": "form-control",
                    "id": "task_time_start",
                    'type': 'time'
                }
            ),
            "task_time_end": TimeInput(
                attrs={
                    "class": "form-control",
                    "id": "task_time_end",
                    'type': 'time'
                }
            ),
        }


class editTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title_task', 'description_task', 'date_task', 'task_time_start', 'task_time_end')

        widgets = {
            "title_task": TextInput(
                attrs={
                    "class": "form-control",
                    "id": "title_task",
                }
            ),
            "description_task": Textarea(
                attrs={
                    "class": "form-control",
                    "id": "description_task",
                }
            ),
            "date_task": DateInput(
                attrs={
                    "class": "form-control",
                    "id": "date_task",
                    'type': 'date'
                }

            ),
            "task_time_start": TimeInput(
                attrs={
                    "class": "form-control",
                    "id": "task_time_start",
                    'type': 'time'
                }
            ),
            "task_time_end": TimeInput(
                attrs={
                    "class": "form-control",
                    "id": "task_time_end",
                    'type': 'time'
                }
            ),
        }
