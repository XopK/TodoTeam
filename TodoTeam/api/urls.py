from django.urls import path
from . import views

urlpatterns = [
    path('get/task', views.getTask),
    path('create/task', views.createTask)
]