from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from .models import Subscription, PinnedPost, SubscriptionHistory

@receiver(post_save, sender=Subscription)
def subscription_post_save(sender, instance, created, **kwargs):
    """Handler to save subscription"""
    if created:
        # Create record in history when subscription is created
        SubscriptionHistory.objects.create(
            subscription=instance,
            action='created',
            description=f'Subscription created for plan {instance.plan.name}'
        )
    
    else:
        # check if status changed
        if hasattr(instance, '_previous_status'):
            if instance.__previous_status != instance.status:
                
                SubscriptionHistory.objects.create(
                    subscription=instance,
                    action=instance.status,
                    description=f'Subscription status changed from plan {instance._previous_status} to {instance.status}'
                )
        
        
@receiver(pre_delete, sender=Subscription)
def subscription_pre_delete(sender, instance, **kwargs):
    """Handler to delete subscription"""
    
    # delete pinned post when subscription is deleted
    try:
        instance.user.pinned_post.delete()
    except PinnedPost.DoesNotExist:
        pass
    
@receiver(post_save, sender=PinnedPost)
def pinned_post_post_save(sender, instanse, created, **kwargs):
    """Handler to save pinned post"""
    if created:
        # Check that user has an active subscription
        if not hasattr(instanse.user, 'subscription') or not instanse.user.subscription.is_active:
            instanse.delete()
            return
        
        # Record to history subscription
        
        SubscriptionHistory.objects.create(
            subscription=instanse.user.subscription,
            action='post_pinned',
            description=f'Post "{instanse.post.title}" pinned',
            metadata={
                'post_id': instanse.post.id,
                'post_title': instanse.post.title
            }
        )

@receiver(pre_delete, sender=PinnedPost)
def pinned_post_pre_delete(sender, instance, *kwargs):
    """Handler to delete pinned post"""
    
    # Record to subscription history
    if hasattr(instance.user, 'subscription'):
        SubscriptionHistory.objects.create(
            subscription=instance.user.subscription,
            action='post_unpinned',
            description=f'Post "{instance.post.title}" unpinned.',
            metadata={
                'post_id': instance.post.id,
                'post_title': instance.post.title
            }
        )
