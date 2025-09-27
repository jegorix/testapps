from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Sum
from .models import Payment, PaymentAttempt, Refund, WebhookEvent

# Register your models here.

class PaymentAttemptInline(admin.TabularInline):
    model = PaymentAttempt
    extra = 0
    readonly_fields = ('stripe_charge_id', 'status', 'error_message', 'metadata', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


class RefundInline(admin.TabularInline):
    model = Refund
    extra = 0
    readonly_fields = ('amount', 'status', 'stripe_refund_id', 'created_at', 'processed_at')
    fields = ('amount', 'reason', 'status', 'created_by')
    can_delete = False


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user_link', 'amount_display', 'status_display', 
        'payment_method', 'subscription_link', 'created_at'
    )
    list_filter = ('status', 'payment_method', 'currency', 'created_at')
    search_fields = (
        'user__username', 'user__email', 'stripe_payment_intent_id', 
        'stripe_session_id', 'description'
    )
    readonly_fields = (
        'created_at', 'updated_at', 'processed_at', 'is_successful', 
        'is_pending', 'can_be_refunded'
    )
    raw_id_fields = ('user', 'subscription')
    inlines = [PaymentAttemptInline, RefundInline]
    
    fieldsets = (
        (None, {
            'fields': ('user', 'subscription', 'amount', 'currency', 'status', 'payment_method')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Stripe Data', {
            'fields': (
                'stripe_payment_intent_id', 'stripe_session_id', 
                'stripe_customer_id'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Status Info', {
            'fields': ('is_successful', 'is_pending', 'can_be_refunded'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'processed_at'),
            'classes': ('collapse',)
        }),
    )

    def user_link(self, obj):
        """Ссылка на пользователя"""
        url = reverse('admin:accounts_user_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = 'User'

    def subscription_link(self, obj):
        """Ссылка на подписку"""
        if obj.subscription:
            url = reverse('admin:subscribe_subscription_change', args=[obj.subscription.pk])
            return format_html('<a href="{}">{}</a>', url, obj.subscription.plan.name)
        return '-'
    subscription_link.short_description = 'Subscription'

    def amount_display(self, obj):
        """Отображение суммы"""
        return f"${obj.amount} {obj.currency}"
    amount_display.short_description = 'Amount'

    def status_display(self, obj):
        """Отображение статуса с цветом"""
        colors = {
            'succeeded': 'green',
            'failed': 'red',
            'pending': 'orange',
            'processing': 'blue',
            'cancelled': 'gray',
            'refunded': 'purple'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.status.upper()
        )
    status_display.short_description = 'Status'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'user', 'subscription', 'subscription__plan'
        )

    actions = ['mark_as_succeeded', 'mark_as_failed', 'export_payments']

    def mark_as_succeeded(self, request, queryset):
        """Помечает платежи как успешные"""
        count = queryset.filter(status__in=['pending', 'processing']).update(status='succeeded')
        self.message_user(request, f'{count} payments marked as succeeded.')
    mark_as_succeeded.short_description = "Mark selected payments as succeeded"

    def mark_as_failed(self, request, queryset):
        """Помечает платежи как неудачные"""
        count = queryset.filter(status__in=['pending', 'processing']).update(status='failed')
        self.message_user(request, f'{count} payments marked as failed.')
    mark_as_failed.short_description = "Mark selected payments as failed"

    def export_payments(self, request, queryset):
        """Экспорт платежей в CSV"""
        # Здесь можно добавить логику экспорта
        self.message_user(request, f'Export functionality will be implemented soon.')
    export_payments.short_description = "Export selected payments"


@admin.register(PaymentAttempt)
class PaymentAttemptAdmin(admin.ModelAdmin):
    list_display = (
        'payment_link', 'stripe_charge_id', 'status', 'error_message_short', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('payment__id', 'stripe_charge_id', 'error_message')
    readonly_fields = ('payment', 'stripe_charge_id', 'status', 'error_message', 'metadata', 'created_at')

    def payment_link(self, obj):
        """Ссылка на платеж"""
        url = reverse('admin:payment_payment_change', args=[obj.payment.pk])
        return format_html('<a href="{}">Payment #{}</a>', url, obj.payment.id)
    payment_link.short_description = 'Payment'

    def error_message_short(self, obj):
        """Краткое сообщение об ошибке"""
        if obj.error_message:
            return obj.error_message[:100] + '...' if len(obj.error_message) > 100 else obj.error_message
        return '-'
    error_message_short.short_description = 'Error'

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Refund)
class RefundAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'payment_link', 'amount_display', 'status_display', 
        'is_partial_display', 'created_by', 'created_at'
    )
    list_filter = ('status', 'created_at')
    search_fields = ('payment__id', 'stripe_refund_id', 'reason')
    readonly_fields = ('created_at', 'processed_at', 'is_partial')
    raw_id_fields = ('payment', 'created_by')

    fieldsets = (
        (None, {
            'fields': ('payment', 'amount', 'reason', 'status')
        }),
        ('Stripe', {
            'fields': ('stripe_refund_id',),
            'classes': ('collapse',)
        }),
        ('Management', {
            'fields': ('created_by',)
        }),
        ('Status', {
            'fields': ('is_partial',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at'),
            'classes': ('collapse',)
        }),
    )

    def payment_link(self, obj):
        """Ссылка на платеж"""
        url = reverse('admin:payment_payment_change', args=[obj.payment.pk])
        return format_html('<a href="{}">Payment #{}</a>', url, obj.payment.id)
    payment_link.short_description = 'Payment'

    def amount_display(self, obj):
        """Отображение суммы"""
        return f"${obj.amount}"
    amount_display.short_description = 'Amount'

    def status_display(self, obj):
        """Отображение статуса с цветом"""
        colors = {
            'succeeded': 'green',
            'failed': 'red',
            'pending': 'orange',
            'cancelled': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.status.upper()
        )
    status_display.short_description = 'Status'

    def is_partial_display(self, obj):
        """Отображение частичного возврата"""
        if obj.is_partial:
            return format_html('<span style="color: orange;">Partial</span>')
        else:
            return format_html('<span style="color: green;">Full</span>')
    is_partial_display.short_description = 'Type'

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('payment', 'created_by')


@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'provider', 'event_type', 'status_display', 
        'error_message_short', 'created_at'
    )
    list_filter = ('provider', 'status', 'event_type', 'created_at')
    search_fields = ('event_id', 'event_type', 'error_message')
    readonly_fields = ('provider', 'event_id', 'event_type', 'data', 'created_at', 'processed_at')

    fieldsets = (
        (None, {
            'fields': ('provider', 'event_id', 'event_type', 'status')
        }),
        ('Processing', {
            'fields': ('error_message',)
        }),
        ('Data', {
            'fields': ('data',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'processed_at'),
            'classes': ('collapse',)
        }),
    )

    def status_display(self, obj):
        """Отображение статуса с цветом"""
        colors = {
            'processed': 'green',
            'failed': 'red',
            'pending': 'orange',
            'ignored': 'gray'
        }
        color = colors.get(obj.status, 'black')
        return format_html(
            '<span style="color: {}; font-weight: bold;">{}</span>',
            color, obj.status.upper()
        )
    status_display.short_description = 'Status'

    def error_message_short(self, obj):
        """Краткое сообщение об ошибке"""
        if obj.error_message:
            return obj.error_message[:100] + '...' if len(obj.error_message) > 100 else obj.error_message
        return '-'
    error_message_short.short_description = 'Error'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        # Разрешаем удаление только старых записей
        return request.user.is_superuser

    actions = ['mark_as_processed', 'retry_failed_events']

    def mark_as_processed(self, request, queryset):
        """Помечает события как обработанные"""
        count = queryset.filter(status='pending').update(status='processed')
        self.message_user(request, f'{count} events marked as processed.')
    mark_as_processed.short_description = "Mark selected events as processed"

    def retry_failed_events(self, request, queryset):
        """Повторная обработка неудачных событий"""
        from .services import WebhookService
        
        count = 0
        for event in queryset.filter(status='failed'):
            success = WebhookService.process_stripe_webhook(event.data)
            if success:
                event.mark_as_processed()
                count += 1
        
        self.message_user(request, f'{count} events reprocessed successfully.')
    retry_failed_events.short_description = "Retry failed events"