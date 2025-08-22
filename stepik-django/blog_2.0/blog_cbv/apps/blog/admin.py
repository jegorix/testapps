from django.contrib import admin
from .models import Post, Category
from django_mptt_admin.admin import DjangoMpttAdmin #DraggableMPTTAdmin
# Register your models here.

admin.site.register(Post)

@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin): # instead of DjangoMPTTAdmin
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}