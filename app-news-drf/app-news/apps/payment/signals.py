from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Payment
from .services import PaymentService

@receiver(pre_save, sender=Payment)
def payment_pre_save(sender, instance, *args, **kwargs):
    """Handler before payment save"""
    # Record previous status to following changes
    if instance.pk:
        try:
            previous = Payment.objects.get(pk=instance.pk)
            instance._previous_status = previous.status
        except Payment.DoesNotExist:
            instance._previous_status = None
            
            
@receiver(post_save, sender=Payment)
def payment_post_save(sender, instance, created, **kwargs):
    """Handler for payment save"""
    if not created and hasattr(instance, '_previous_status'):
        
        # if status changed to Succeeded
        if (instance._previous_status in ['pending', 'processing'] and
            instance.status == 'succeeded'):
            PaymentService.process_successful_payment(instance)
            
         # if status changed to Failed
        if (instance._previous_status in ['pending', 'processing'] and
            instance.status == 'failed'):
            PaymentService.process_failed_payment(instance) 
            
        