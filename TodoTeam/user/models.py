from django.db import models
from django.contrib.auth import settings
from django.dispatch import receiver


class Command(models.Model):
    name_command = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name_command

    class Meta:
        verbose_name_plural = "Команды"
        verbose_name = "Команда"


class CommandUser(models.Model):
    command = models.ForeignKey('Command', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    is_leader = models.BooleanField(default=False)

    def __str__(self):
        command_name = self.command.name_command if self.command else 'Нет команды'
        user_name = f'{self.user.first_name} {self.user.last_name}' if self.user else 'Нет участника'
        return f'{command_name} - {user_name}'

    class Meta:
        verbose_name_plural = "Список команд"
        verbose_name = "Список"


@receiver(models.signals.post_save, sender=Command)
def create_command_user(sender, instance, created, **kwargs):
    if created:
        CommandUser.objects.create(command=instance, user=instance.user, is_leader=True)

class favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    task = models.ForeignKey('task.Task', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        task_title = self.task.title_task if self.task else 'Нет задачи'
        user_name = self.user.username if self.user else 'Нет пользователя'
        return f'{task_title} - {user_name}'

    class Meta:
        verbose_name_plural = "Избранные"
        verbose_name = "Избранное"
