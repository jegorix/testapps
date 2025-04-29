from django.urls import path
from . import views


urlpatterns = [
    path('', views.TaskCreateView.as_view(), name='create_task'),
    # path('create/', views.create, name='create_task'),
    path('show/', views.TasksListView.as_view(), name='show_tasks'),
    path('<int:pk>/update', views.TaskUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', views.TaskDeleteView.as_view(), name='delete'),
    path('<int:task_id>/set', views.set_status, name ='set_status'),
]
