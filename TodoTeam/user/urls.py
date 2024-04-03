from django.urls import path
from . import views
from .views import updateTaskView

urlpatterns = [
    path('sign_up', views.registration, name='sing_up'),
    path('sign_in', views.entrance, name='sign_in'),
    path('personalArea', views.personalArea, name='personal_area'),
    path('addtask', views.addtask, name='add_task'),
    path('logout', views.logout_view, name='logout'),
    path('status/<int:pk>', views.change_status, name='status'),
    path('personalArea/<int:pk>/edit', updateTaskView.as_view(), name='updateTask'),
    path('personalArea/<int:pk>/delete', views.delete_task, name='deleteTask'),
    path('personalArea/<int:pk>/favorite', views.addFavorite, name='favorite'),
]
