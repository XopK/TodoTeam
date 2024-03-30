from django.urls import path
from . import views

urlpatterns = [
    path('sign_up', views.registration, name='sing_up'),
    path('sign_in', views.entrance, name='sign_in'),
    path('personalArea', views.personalArea, name='personal_area'),
    path('addtask', views.addtask, name='add_task'),
    ]