from django.conf import settings
from django.utils import timezone
from decimal import Decimal
from typing import Dict, Optional, Tuple
import logging
import stripe

from .models import Payment, PaymentAttempt, WebhookEvent
from apps.subscribe.models import Subscription, SubscriptionHistory, SubscriptionPlan

logger = logging.getLogger(__name__)


# Stripe settings
stripe.api_key = settings.STRIPE_SECRET_KEY

class StripeService:
    """Service for working with stripe"""
    
    @staticmethod
    def create_customer(user) -> Optional[str]:
        """Create client in Stripe"""
        
        try:
            customer = stripe.Customer.create(
                email=user.email,
                name=user.get_full_name() or user.username,
                metadata={
                    'user_id': user.id,
                    'username': user.username
                }
            )
            return customer.id
            
        except stripe.error.StripeError as e:
            logger.error(f"Error creating Stripe customer: {e}")
            return None
        
        
    @staticmethod
    def create_checkout_session(payment: Payment, success_url: str, cancel_url: str) -> Optional[dict]:
        """Create Stripe Checkout session"""
        
        try:
            # get or create customer
            if not payment.stripe_customer_id:
                customer_id = StripeService.create_customer(payment.user)
                if customer_id:
                    payment.stripe_customer_id = customer_id
                    payment.save()

            session = stripe.checkout.Session.create(
                customer=payment.stripe_customer_id,
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': payment.currency.lower(),
                        'product_data': {
                            'name': f'Subscription - {payment.subscription.plan.name}',
                            'description': payment.description,
                        },
                        'unit_amount': int(payment.amount * 100), 
                    },
                    'quantity': 1
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata= {
                    'payment_id': payment.id,
                    'user_id': payment.user.id,
                    'subscription_id': payment.subscription.id if payment.subscription else None
                }
            )
            
            # update payment
            payment.stripe_session_id = session.id
            payment.status = 'processing'
            payment.save()

            return {
                'checkout_url': session.url,
                'session_id': session.id,
                'payment_id': payment.id 
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error creating checkout session: {e}")
            payment.mark_as_failed(str(e))
            return None
        
    @staticmethod
    def create_payment_intent(payment: Payment) -> Optional[str]:
        """Create Payment Intent in Stripe"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(payment.amount * 100),
                currency=payment.currency.lower(),
                customer=payment.stripe_customer_id,
                metadata={
                    'payment_id': payment.id,
                    'user_id': payment.user.id,
                    'subscription_id': payment.subscription.id if payment.subscription else None
                }
            )
            
            payment.stripe_payment_intent_id = intent.id
            payment.save()
            
            return intent.client_secret
        
        except stripe.error.StripeError as e:
            logger.error(f"Error creating payment intent: {e}")
            payment.mark_as_failed(str(e))
            return None
            
            
    @staticmethod
    def refund_payment(payment: Payment, amount: Optional[Decimal] = None, reason: str = "") -> bool:
        """Return Payment with Stripe"""
        try:
            if not payment.stripe_payment_intent_id:
                return False
            
            refund_data = {
                'payment_intent': payment.stripe_payment_intent_id,
                'metadata':{
                    'payment_id': payment.id,
                    'reason': reason
                }
            }
            
            if amount:
                refund_data['amount'] = int(amount * 100)
                
            refund = stripe.Refund.create(**refund_data)
            
            return refund.status == 'succeeded'
        
        except stripe.error.StripeError as e:
            logger.error(f"Error proccessing refund: {e}")
            payment.mark_as_failed(str(e))
            return False
        
    @staticmethod
    def retrive_session(session_id: str) -> Optional[Dict]:
        """Retrieve info about session"""
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            return {
                'status': session.payment_status,
                'payment_intent': session.payment_intent,
                'customer': session.customer,
                'metadata': session.metadata,
            }
            
        except stripe.error.StripeError as e:
            logger.error(f"Error retrieving session: {e}")
            return None
    
    
class PaymentService:
    """Main Service for working with payments"""
    
    @staticmethod
    def create_subscription_payment(user, plan: SubscriptionPlan) -> Tuple[Payment, Subscription]:
        """Create payment for subscription"""
        # Create subscription
        subscription = Subscription.objects.create(
            user=user,
            plan=plan,
            status='pending',
            start_date=timezone.now(),
            end_date=timezone.now() # will be updated after payment
        )
        
        # Create payment
        payment = Payment.objects.create(
            user=user,
            subscription=subscription,
            amount=plan.price,
            currency='USD',
            description=f'Subscription to {plan.name}',
            payment_method='stripe'
        )
        
        # Record to history
        SubscriptionHistory.objects.create(
            subscription=subscription,
            action='created',
            description=f'Subscription created for plan {plan.name}',
        )
        
        return payment, subscription
    
    
    @staticmethod
    def process_successful_payment(payment: Payment) -> bool:
        """Process successful payment"""
        try:
            payment.mark_as_succeeded()
            # Activate subscription
            if payment.subscription:
                payment.subscription.activate()
                
            # Record to history
            SubscriptionHistory.objects.create(
                subscription=payment.subscription,
                action='activated',
                description='Subscription activated after successfull payment',
                metadata={'payment_id': payment.id}
            )
                
            logger.info(f"Payment {payment.id} processed successfully")
            return True
        
        except Exception as e:
            logger.error(f"Error processing successful payment {payment.id}: {e}")
            return False
        
        
    @staticmethod
    def process_failed_payment(payment: Payment, reason: str="") -> bool:
        """Process failed payment"""
        try:
            payment.mark_as_failed(reason)
            
            # Cancel subscription
            if payment.subscription:
                payment.subscription.cancel()
                
            # Record to history
            SubscriptionHistory.objects.create(
                subscription=payment.subscription,
                action='payment_failed',
                description=f'Payment failed: {reason}',
                metadata={'payment_id': payment.id}
            )
                
            logger.info(f"Payment {payment.id} marked as failed")
            return True
        
        except Exception as e:
            logger.error(f"Error processing failed payment {payment.id}: {e}")
            return False
    
    
    @staticmethod
    def cancel_subscription(subscription: Subscription) -> bool:
        """Cancel Subscription"""
        try:
            subscription.cancel()
            
            # Delete pinned post if exists
            if hasattr(subscription.user, 'pinned_post'):
                subscription.user.pinned_post.delete()
                
            # Record to history
            SubscriptionHistory.objects.create(
                subscription=subscription,
                action='cancelled',
                description='Subscription cancelled by user',
            )
                
            logger.info(f"Subscription {subscription.id} cancelled")
            return True
        
        except Exception as e:
            logger.error(f"Error cancelling subscription {subscription.id}: {e}")
            return False
        
        
        
class WebhookService:
    """Service to handle webhook events"""
    
    @staticmethod
    def process_stripe_webhook(event_data: Dict) -> bool:
        """Handle Stripe Webhook"""
        try:
            event_id = event_data.get('id')
            event_type = event_data.get('type')
            
            # Check if already processed this event
            if WebhookEvent.objects.filter(event_id=event_id).exists():
                return True
            
            # Create record about event
            webhook_event = WebhookEvent.objects.create(
                provider='stripe',
                event_id=event_id,
                event_type=event_type,
                data=event_data
            )
            
            # Hadle different types of events
            success = False
            
            if event_type == 'checkout.session.completed':
                success = WebhookService._handle_checkout_completed(event_data)
                
            elif event_type == 'checkout.session.succeeded':
                success = WebhookService._handle_checkout_succeeded(event_data)
                
            elif event_type == 'checkout.session.failed':
                success = WebhookService._handle_checkout_failed(event_data)
                
            elif event_type == 'checkout.dispute.created':
                success = WebhookService._handle_dispute_created(event_data)
            
            else:
                # Unknown event type -  mark as ignore
                webhook_event.status = 'ignored'
                webhook_event.save()
                return True
                
            if success:
                webhook_event.mark_as_processed()
            else:
                webhook_event.mark_as_failed("Processing failed")
            
            return success
        
        except Exception as e:
            logger.error(f"Error processing Stripe webhook: {e}")
            return False
        
        
    @staticmethod
    def _handle_checkout_completed(event_data: Dict) -> bool:
        """Process ending of checkout session"""
        try:
            session = event_data['data']['object']
            metadata = session.get('metadata', {})
            payment_id = metadata.get('payment_id')
            
            if not payment_id:
                logger.warning("No payment_id in checkout session metadata")
                return False
            
            payment = Payment.objects.get(id=payment_id)
            
            return PaymentService.process_successful_payment(payment)
        
        except Payment.DoesNotExist:
            logger.error("Payment not found for checkout session")
            return False
        
        except Exception as e:
            logger.error(f"Error handling checkout completed: {e}")
            return False
        
        
    @staticmethod
    def _handle_checkout_succeeded(event_data: Dict) -> bool:
        """Process successed payment"""
        try:
            payment_intent = event_data['data']['object']
            metadata = payment_intent.get('metadata', {})
            payment_id = metadata.get('payment_id')
            
            if not payment_id:
                logger.warning("No payment_id in payment intent metadata")
                return False
            
            payment = Payment.objects.get(id=payment_id)
            payment.stripe_payment_intent_id = payment_intent['id']
            payment.save()
            
            return PaymentService.process_successful_payment(payment)
        
        except Payment.DoesNotExist:
            logger.error("Payment not found for checkout session")
            return False
        
        except Exception as e:
            logger.error(f"Error handling checkout completed: {e}")
            return False
        

    @staticmethod
    def _handle_checkout_failed(event_data: Dict) -> bool:
        """Process successed payment"""
        try:
            payment_intent = event_data['data']['object']
            metadata = payment_intent.get('metadata', {})
            payment_id = metadata.get('payment_id')
            
            if not payment_id:
                logger.warning("No payment_id in payment intent metadata")
                return False
            
            payment = Payment.objects.get(id=payment_id)
            
            last_error = payment_intent.get('last_payment_error', {})
            error_message = last_error.get('message', 'Payment failed')
            
            return PaymentService.process_failed_payment(payment, error_message)
            
        except Payment.DoesNotExist:
            logger.error("Payment not found for checkout session")
            return False
        
        except Exception as e:
            logger.error(f"Error handling payment failed: {e}")
            return False
        
        
    @staticmethod
    def _handle_dispute_created(event_data: Dict) -> bool:
        """Process dispute creation"""
        try:
            dispute = event_data['data']['object']
            charge_id = dispute.get('charge')
            
            # There you can implemented logic for processing disputes
            # For instance, send notifications to admins
            
            logger.info(f"Dispute created for charge {charge_id}")
            return True
        
        except Exception as e:
            logger.error(f"Error handling dispute created: {e}")
            return False