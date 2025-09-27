from rest_framework import serializers
from decimal import Decimal
from .models import Payment, PaymentAttempt, Refund, WebhookEvent


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer for payments"""
    user_info = serializers.SerializerMethodField()
    subscription_info = serializers.SerializerMethodField()
    is_successul = serializers.ReadOnlyField()
    is_pending = serializers.ReadOnlyField()
    can_be_refunded = serializers.ReadOnlyField()
    
    class Meta:
        model = Payment
        
        fields = [
            'id', 'user', 'user_info', 'subscription', 'subscription_info',
            'amount', 'currency', 'status', 'payment_method', 'description',
            'is_successful', 'is_pending', 'can_be_refunded',
            'created_at', 'updated_at', 'processed_at'
        ]
        
        read_only_fields = [
            'id', 'user', 'status', 'created_at', 'updated_at', 'processed_at'
        ]
        
    def get_user_info(self, obj):
        """Return info about user"""
        return {
            'id': obj.user.id,
            'username': obj.user.username,
            'email': obj.user.email
        }
        
    def get_subscription_info(self, obj):
        """Return info about subscription"""
        if obj.subscription:
            return {
                'id': obj.subscription.id,
                'plan_name': obj.subscription.plan.name,
                'start_date': obj.subscription.start_date,
                'end_date': obj.subscription.end_date,
                'status': obj.subscription.status
            }
            
    
class PaymentCreateSerializer(serializers.Serializer):
    """Serializer for Payment Creation"""
    subscription_plan_id = serializers.IntegerField()
    payment_method = serializers.ChoiceField(
        choices=Payment.PAYMENT_METHOD_CHOICES,
        default='stripe'
    )
    
    success_url = serializers.URLField(required=False)
    cancel_url = serializers.URLField(required=False)
    
    def validate_subscription_plan_id(self, value):
        """Tarrif plan validation"""
        from apps.subscribe.models import SubscriptionPlan
        
        try:
            plan = SubscriptionPlan.objects.get(id=value, is_active=True)
        except SubscriptionPlan.DoesNotExist:
            raise serializers.ValidationError("Subscription plan not found or inactive.")
        
        return value
    
    def validate(self, attrs):
        """General Validation"""
        user = self.context['request'].user
       
        if hasattr(user, 'subscription') and user.subscription.is_active:
           raise serializers.ValidationError({
               'non_field_errors': ['User already has an active subscription.']
           })
           
        # check if there is Pending Payments
        pending_payments = Payment.objects.filter(
            user=user,
            status__in=['pending', 'processing']
        ).exists()
        
        if pending_payments:
            raise serializers.ValidationError({
                'non_field_errors': ['User has pending payments. Please complete or cancel them first']
            })
            
        return attrs
    

class PaymentAttemptSerializer(serializers.ModelSerializer):
    """Serializer for Payment Attempts"""
    
    class Meta:
        model = PaymentAttempt
        fields = [
            'id', 'stripe_charge_id', 'status', 'error_message',
            'metadata', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
        
        
        
class RefundSerializer(serializers.ModelSerializer):
    """Serializer for Refund"""
    payment_info = serializers.SerializerMethodField()
    created_by_info = serializers.SerializerMethodField()
    is_partial = serializers.ReadOnlyField()
    
    class Meta:
        model = Refund
        fields = [
            'id', 'payment', 'payment_info', 'amount', 'reason', 'status',
            'is_partial', 'created_by', 'created_by_info', 'created_at', 'processed_at'
        ]
        
        read_only_fields = [
            'id', 'created_at', 'status', 'created_by', 'processed_at'
        ]
    
    def get_payment_info(self, obj):
        """Return info about payment"""
        return {
            'id': obj.payment.id,
            'amount': obj.payment.amount,
            'currency': obj.payment.currency,
            'status': obj.payment.status,
            'user': obj.payment.user
        }
        
    def get_created_by_info(self, obj):
        """Return info about person which created Refund"""
        if obj.created_by:
            return {
                'id': obj.created_by.id,
                'username': obj.created_by.username 
            }
        return 
    
    
    def validate_amount(self, value):
        """Validate Refund amount"""
        if value <= 0:
            raise serializers.ValidationError("Refund amount must be positive.")
        return value
    
    
    def validate(self, attrs):
        """General Refund Validation"""
        payment_id = self.context.get('payment_id')
        
        if payment_id:
            try:
                payment = Payment.objects.get(id=payment_id)
            except Payment.DoesNotExist:
                raise serializers.ValidationError("Payment not found.")
            
            if not payment.can_be_refunded:
                raise serializers.ValidationError("This payment cannot be refunded.")
            
            # Check that refund amount less than payment amount
            total_refunded = payment.refunds.filter(
                status='succeeded'
            ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0')

            if attrs['amount'] > (payment.amount - total_refunded):
                raise serializers.ValidationError(
                    "Refund amount exceeds remaining payment amount."
                )
                
            return attrs
        
        
class RefundCreateSerializer(serializers.ModelSerializer):
    """Serializer for Refund creation"""
    
    class Meta:
        model = Refund
        fields = ['amount', 'reason']
        
    def validate_amount(self, value):
        """Validation Refund amount"""
        if value <= 0:
            raise serializers.ValidationError("Refund amount must be positive.")
        return value
    
    
class WebhookSerializer(serializers.ModelSerializer):
    """Serializer for Webhook events"""
    
    class Meta:
        model = WebhookEvent
        fields = [
            'id', 'provider', 'event_id', 'event_type', 'status',
            'processed_at', 'error_message', 'created_at'
        ]
        
        read_only_fields = ['id', 'created_at']
        
        
class StripeCheckoutSessionSerializer(serializers.Serializer):
    """Serializer for creation Stripe Checkout Session"""
    checkout_url = serializers.URLField(read_only=True)
    session_id = serializers.CharField(read_only=True)
    payment_id = serializers.IntegerField(read_only=True)
    
    
class PaymentStatusSerializer(serializers.Serializer):
    """Serializer for payment status"""
    payment_id = serializers.IntegerField()
    status = serializers.CharField()
    message = serializers.CharField()
    subscription_activated = serializers.BooleanField(default=False) 