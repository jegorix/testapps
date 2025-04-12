from django.urls import path
from . import views


urlpatterns = [
    # path('', views.TaskCreateView.as_view(), name='create_task'),
    path('create/', views.create, name='create_task'),
    path('show/', views.show, name='show_tasks'),
]
