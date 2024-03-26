from django.db import models
class Task(models.Model):
    title_task = models.CharField(max_length=100)
    description_task = models.TextField()
    date_task = models.DateField()
    task_time_start = models.TimeField()
    task_time_end = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.ForeignKey('TaskStatus', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title_task

    class Meta:
        verbose_name_plural = "Задачи"
        verbose_name = "Задача"

class TaskStatus(models.Model):
    name_task = models.CharField(max_length=100, db_index=True)

    def __str__(self):
        return self.name_task