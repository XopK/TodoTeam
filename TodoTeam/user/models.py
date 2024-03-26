from django.db import models

class Command(models.Model):
    name_command = models.CharField(max_length=255)