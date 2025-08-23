from django.contrib import admin
from .models import Profile
# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Админ-панель модели профиля
    """
    list_display = ('user', 'birth_date', 'slug')
    list_display_links = ('user', 'slug')    