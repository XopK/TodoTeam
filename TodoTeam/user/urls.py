from django.urls import path
from . import views

urlpatterns = [
    path('sign_up', views.registration, name='registration'),
    path('sign_in', views.entrance, name='entrance'),
    ]