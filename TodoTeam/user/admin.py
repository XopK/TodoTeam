from django.contrib import admin
from .models import Command, CommandUser, favorite

admin.site.register(CommandUser)
admin.site.register(Command)
admin.site.register(favorite)