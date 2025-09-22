from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from .models import Comment
# Register your models here.

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'post_title', 'author', 'content_preview',
        'parent_comment', 'is_active', 'created_at'
    )
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('content', 'author__username', 'post__title')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('author', 'post', 'parent')
    list_editable = ('is_active', )
    
    fieldsets = (
        (None, {
            'fields': ('post', 'author', 'parent', 'content')
        }),
        
        ('Status', {
            'fields': ('is_active', )
        }),
        
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse', ),
        })
    )
    
    def post_title(self, obj):
        return obj.post.title
    post_title.short_description = 'Post'
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def parent_comment(self, obj):
        if obj.parent:
            return f"Reply to {obj.parent.content[:30]}..."
        return 'Main comment'
    parent_comment.short_description = 'Parent'
    
    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).select_related('author', 'post', 'parent')
    
    actions = ['make_active', 'make_inactive']
    
    def make_active(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} comments were marked as active.')
    make_active.short_description = "Mark selected comments as active"
    
    def make_inactive(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} comments were marked as inactive.')
    make_inactive.short_description = "Mark selected comments as inactive"