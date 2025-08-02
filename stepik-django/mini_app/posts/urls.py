from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("edit/<int:id>/", views.edit, name="edit"),
    path("delete/<int:id>/", views.delete, name="delete"),
    path("user/", views.user_profile, name="user_profile"),
    path("add_user/", views.add_user, name="add_user"),
    path("delete_user/<int:id>/", views.delete_profile, name="delete_user"),
    path("edit_user/<int:id>/", views.edit_profile, name="edit_user"),
    path("sort_users/", views.sort_users, name="sort_users")
]
