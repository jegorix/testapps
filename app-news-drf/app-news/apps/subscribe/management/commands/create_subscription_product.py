
from django.core.management.base import BaseCommand
from apps.subscribe.models import SubscriptionPlan

class Command(BaseCommand):
    help = 'Create default subscription plans'
    
    def handle(self, *args, **kwargs):
        # Create base subscription plan
        plan, created = SubscriptionPlan.objects.get_or_create(
            name='Premium Monthly',
            defaults={
                'price': 12,
                'duration_days': 30,
                'stripe_price_id': 'price_premium_monthly',
                'features': {
                    'pin_posts': True,
                    'priority': True,
                    'analytics': True
                },
                
                'is_active': True
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Created subscription plan: {plan.name}')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'Subscription plan already exists: {plan.name}')
            )