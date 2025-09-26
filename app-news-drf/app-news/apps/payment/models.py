from django.db import models
from django.conf import settings
from decimal import Decimal
# Create your models here.

class Payment(models.Model):
    """Payment Model"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('succeeded', 'Succeded'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded')
    )
    
    PAYMENT_METHOD_CHOICES = [
        ('stripe', 'Stripe'),
        ('paypal', 'Paypal'),
        ('manual', 'Manual')
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments'
    )
    
    subscription = models.ForeignKey(
        'subscribe.Subscription',
        on_delete=models.CASCADE,
        related_name='payments',
        null=True,
        blank=True
    )
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='stripe')
    
    # Stripe-specific fields
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    
    # Metadata
    description = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['stripe_payment_intent_id']),
            models.Index(fields=['stripe_session_id']),
            models.Index(fields=['created_at'])
        ]
    
    def __str__(self) -> str:
        return f"Payment {self.id} - {self.user.username} - ${self.amount} ({self.status})"
    
    @property
    def is_successful(self):
        """Check if payment is successfull"""
        return self.status == 'succeeded'
    
    @property
    def is_pending(self):
        """Check if payment waiting process"""
        return self.status in ['pending', 'processing']
    
    @property
    def can_be_refunded(self):
        """Check if payment can be refounded"""
        return self.status == 'succeeded' and self.payment_method == 'stripe'
    
    def mark_as_succeeded(self):
        """Mark payments as succeeded"""
        from django.utils import timezone
        self.status = 'succeeded'
        self.processed_at = timezone.now()
        self.save()
        
    
    def mark_as_failed(self, reason=None):
        """Mark payments as failed"""
        from django.utils import timezone
        self.status = 'failed'
        self.processed_at = timezone.now()
        if reason:
            self.metadata['failure_reason'] = reason
        self.save()
        
        
class PaymentAttempt(models.Model):
    """Payment attempt"""
    
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='attempts'
    )
    
    stripe_charge_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=50)
    error_message = models.TextField(blank=True, null=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'payment_attempts'
        verbose_name = 'Payment Attempt'
        verbose_name_plural = 'Payment Attempts'
        ordering = ['-created_at']

    def __str__(self):
        return f"Attempt for Payment {self.payment.id} - {self.status}"
    

class Refund(models.Model):
    """Refund Model"""
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('succeeded', 'Succeded'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    )
    
    payment = models.ForeignKey(
        Payment,
        on_delete=models.CASCADE,
        related_name='refunds'
    )
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stripe_refund_id = models.CharField(max_length=50, blank=True, null=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_refunds'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'refunds'
        verbose_name = 'Refund'
        verbose_name_plural = 'Refunds'
        ordering = ['-created_at']

    def __str__(self):
        return f"Refund {self.id} - ${self.amount} for Payment {self.payment.id}"
    
    @property
    def is_partial(self):
        """Check if refund is partial"""
        return self.amount < self.payment.amount
    
    def process_refund(self):
        """Process refund"""
        from django.utils import timezone
        self.status = 'succeeded'
        self.processed_at = timezone.now()
        self.save()
        
        
class WebhookEvent(models.Model):
    """Events from payments"""
    
    PROVIDER_CHOICES = [
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processed', 'Processed'),
        ('failed', 'Failed'),
        ('ignored', 'Ignored'),
    ]
    
    provider = models.CharField(max_length=20, choices=PROVIDER_CHOICES)
    event_id = models.CharField(max_length=255, unique=True)
    event_type = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    data = models.JSONField()
    processed_at = models.DateTimeField(null=True, blank=True)
    error_message = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'webhook_events'
        verbose_name = 'Webhook Event'
        verbose_name_plural = 'Webhook Events'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['provider', 'event_type']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.provider} - {self.event_type} ({self.status})"
    
    
    def mark_as_processed(self):
        """Mark event as processed"""
        from django.utils import timezone
        self.status = 'processed'
        self.processed_at = timezone.now()
        self.save()
        
    def mark_as_failed(self, error_message):
        """Mark event as failed"""
        from django.utils import timezone
        self.status = 'failed'
        self.error_message = error_message
        self.processed_at = timezone.now()
        self.save()