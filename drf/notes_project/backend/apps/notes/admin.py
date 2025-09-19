# Sets up admin panel to work with models
from django.contrib import admin
from .models import Note
# Register your models here.

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    # Set up admin panel for Note model
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        # Group fields in admin panel
        ('Основная информация', {
            'fields': ('title', 'content')
        }),
        
         ('Временные метки', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        
    )