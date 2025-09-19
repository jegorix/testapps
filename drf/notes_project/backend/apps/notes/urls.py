# DETERMINE URL routers for Note app
# connected with main url
from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('notes/', views.NoteListCreateView.as_view(), name='note-list-create'),
    path('notes/<int:pk>/', views.NoteDetailView.as_view(), name='note-detail'),
]
 