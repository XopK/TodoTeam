from django.db import models
from user.models import Command
from user.models import favorite


class Task(models.Model):
    title_task = models.CharField(max_length=100)
    description_task = models.TextField()
    date_task = models.DateField()
    task_time_start = models.TimeField()
    task_time_end = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('TaskStatus', on_delete=models.CASCADE, null=True, blank=True)
    command = models.ForeignKey(Command, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        task_title = self.title_task
        command_name = self.command.name_command if self.command else 'Нет команды'
        return f'{task_title} - {command_name}'

    class Meta:
        verbose_name_plural = "Задачи"
        verbose_name = "Задача"

class TaskStatus(models.Model):
    name_task = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name_task


