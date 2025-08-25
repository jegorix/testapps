from django.contrib import admin
from .models import Post, Category, Comment
from django_mptt_admin.admin import DjangoMpttAdmin #DraggableMPTTAdmin
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Админ-панель модели записей
    """
    prepopulated_fields = {'slug': ('title',)}
    

@admin.register(Category)
class CategoryAdmin(DjangoMpttAdmin): # instead of DraggableMPTTAdmin
    """
    Админ-панель модели категорий
    """
    prepopulated_fields = {'slug': ('title',)}
    
@admin.register(Comment)
class CommentAdminPage(DjangoMpttAdmin):
    """
    Админ-панель модели комментариев
    """
    pass