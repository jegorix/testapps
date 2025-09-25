from django.contrib import admin
from django.db.models.query import QuerySet
from django.http import HttpRequest
from django.utils.html import format_html
from django.urls import reverse
from django.utils import timezone
from .models import Subscription, SubscriptionPlan, SubscriptionHistory, PinnedPost
# Register your models here.

@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'price', 'duration_days', 'is_active',
        'subscriptions_counts', 'created_at'
    )
    
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'stripe_price_id')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'duration_days', 'stripe_price_id')
        }),
        ('Features', {
            'fields': ('features',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subscriptions_counts(self, obj):
        """Count of subscription in Plan"""
        return obj.subscriptions.count()
    subscriptions_counts.short_description = 'Subscriptions'
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).prefetch_related('subscriptions')
    
    
class SubscriptionHistoryInline(admin.TabularInline):
    model = SubscriptionHistory
    extra = 0
    readonly_fields = ('action', 'description', 'metadata', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request: HttpRequest, obj=None) -> bool:
        return False
        

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        'user_link', 'plan', 'status', 'is_active_display', 
        'days_remaining_display', 'start_date', 'end_date'
    )
    list_filter = ('status', 'plan', 'auto_renew', 'created_at')
    search_fields = ('user__username', 'user__email', 'plan__name')
    readonly_fields = ('created_at', 'updated_at', 'is_active', 'days_remaining')
    raw_id_fields = ('user',)
    inlines = [SubscriptionHistoryInline]
    
    fieldsets = (
        (None, {
            'fields': ('user', 'plan', 'status')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date', 'auto_renew')
        }),
        ('Stripe', {
            'fields': ('stripe_subscription_id',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'days_remaining'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_link(self, obj):
        """User's link"""
        url = reverse('admin:accounts_user_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    
    def is_active_display(self, obj):
        """Display subscribe availability"""
        if obj.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        else:
            return format_html('<span style="color: red;">✗ Inactive</span>')
    is_active_display.short_description = 'Active'
        
    def days_remaining_display(self, obj):
        """Days remaining display"""
        days = obj.days_remaining
        if days > 7:
            color = 'green'
        elif days > 0:
            color = 'orange'
        else:
            color = 'red'
            
        return format_html(
            '<span style="color: {};">{} days</span>',
            color, days
        )
    days_remaining_display.short_description='Days Remaining'
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related('user', 'plan')
    
    actions = ['activate_subscriptions', 'cancel_subscriptions', 'expire_subscriptions']
    
    def activate_subscriptions(self, request, queryset):
        """Activates choosen subscriptions"""
        count = 0
        for subscription in queryset:
            if subscription.status != 'active':
                subscription.activate()
                count += 1
                
        self.message_user(request, f'{count} subscriptions activated.')
    activate_subscriptions.short_description = "Activate selected subscriptions"
    
    
    def cancel_subscriptions(self, request, queryset):
        """Cancels choosen subscriptions"""
        count = 0
        for subscription in queryset:
            if subscription.status == 'active':
                subscription.cancel()
                count += 1
                
        self.message_user(request, f'{count} subscriptions cancelled.')
    cancel_subscriptions.short_description = "Cancel selected subscriptions"
    
    
    def expire_subscriptions(self, request, queryset):
        """Mark choosen subscriptions as expired"""
        count = 0
        for subscription in queryset:
            if subscription.status == 'active':
                subscription.expire()
                count += 1
                
        self.message_user(request, f'{count} subscriptions expired.')
    expire_subscriptions.short_description = "Mark selected subscriptions as expired"
    
    
@admin.register(PinnedPost)
class PinnedPostAdmin(admin.ModelAdmin):
    list_display = (
        'user_link', 'post_link', 'subscription_status', 'pinned_at'
    )
    list_filter = ('pinned_at', 'user__subscription__status')
    search_fields = ('user__username', 'post__title')
    readonly_fields = ('pinned_at',)
    raw_id_fields = ('user', 'post')
    
    def user_link(self, obj):
        """User's link"""
        url = reverse('admin:accounts_user_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'
    
    
    def post_link(self, obj):
        """Post link"""
        url = reverse('admin:main_post_change', args=[obj.post.pk])
        return format_html('<a href="{}">{}</a>', url, obj.post.title[:50])
    post_link.short_description = 'Post'
    
    
    def subscription_status(self, obj):
        """Status user's subscription"""
        if hasattr(obj.user, 'subscription') and obj.user.subscription.is_active:
            return format_html('<span style="color: green;">✓ Active</span>')
        else:
            return format_html('<span style="color: red;">✗ Inactive</span>')
    subscription_status.short_description = 'Subscription'
    
    
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related(
            'user', 'user__subscription', 'post'
        )
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        """Forbid creation due to admin panel"""
        return False
    
    
    
@admin.register(SubscriptionHistory)
class SubscriptionHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'subscription_link', 'action', 'description_short', 'created_at'
    )
    list_filter = ('action', 'created_at')
    search_fields = ('subscription__user__username', 'description')
    readonly_fields = ('subscription', 'action', 'description', 'metadata', 'created_at')
    
    def subscription_link(self, obj):
        """Subscripstion link"""
        url = reverse('admin:subscribe_subscription_change', args=[obj.subscription.pk])
        
        return format_html(
            '<a href="{}">{} - {}</a>',
            url,
            obj.subscription.user.username,
            obj.subscription.plan.name
        )
    subscription_link.short_description = 'Subscription'
    

    def description_short(self, obj):
        """Short description"""
        return obj.description[:100] + '....' if len(obj.description) > 100 else obj.description
    description_short.short_description = 'Description'
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        """Forbid creation due to admin panel"""
        return False
        
        
    def has_delete_permission(self, request: HttpRequest, obj=None) -> bool:
        """Forbid deleting due to admin panel"""
        return False
        
    def get_queryset(self, request: HttpRequest) -> QuerySet:
        return super().get_queryset(request).select_related('subscription', 'subscription__user')
        
        
# additionally settings
admin.site.site_header = "News Site Administration"
admin.site.site_title = "News Site Admin"
admin.site.index_title = "Welcome to News Site Administration"