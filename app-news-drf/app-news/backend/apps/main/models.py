from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    """Model Category for Posts"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
        

class PostManager(models.Manager):
    """Manager for Post model with additional methods"""
    
    def published(self):
        return self.filter(status='published')
    
    
    def pinned_posts(self):
        """Returns pinned posts in order by pinning time"""
        return self.filter(
            pin_info__isnull=False,
            pin_info__user__subscription__status='active',
            pin_info__user__subscription__end_date__gt=models.functions.Now(),
            status='published'
        ).select_related(
            'pin_info', 'pin_info__user', 'pin_info__user__subscription'
        ).order_by('pin_info__pinned_at')
        
        
    def regular_posts(self):
        """Returns regular unpinned posts"""
        return self.filter(pin_info__isnull=True, status='published')
    
    
    def with_subscription_info(self):
        """Returns info about author's subscription"""
        return self.select_related(
            'author', 
            'author__subscription',
            'category'
        ).prefetch_related('pin_info')
        
        
    def get_posts_for_feed(self):
        """Возвращает посты для ленты с учетом закрепленных постов"""
        from django.db.models import Case, When, Value, BooleanField
        from django.utils import timezone
        
        return self.filter(status='published').annotate(
            is_pinned_flag=Case(
                When(
                    pin_info__isnull=False,
                    pin_info__user__subscription__status='active',
                    pin_info__user__subscription__end_date__gt=timezone.now(),
                    then=Value(True)
                ),
                default=Value(False),
                output_field=BooleanField()
            )
        ).order_by('-is_pinned_flag', '-created_at')
        

            
            
class Post(models.Model):
    """Model Post with pinning support."""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published')
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='published'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)
    
    objects = PostManager()
    
    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['author', '-created_at']),
            
        ]
    
    def __str__(self) -> str:
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"slug": self.slug})
    
    @property
    def comments_count(self):
        """Post`s comments count"""
        return self.comments.filter(is_active=True).count()
    
    @property
    def is_pinned(self):
        """Check if post is pinned"""
        return hasattr(self, 'pin_info') and self.pin_info is not None
    
    @property
    def can_be_pinned_by_user(self):
        """Check can user pin that POST"""
        # focused on POST

        if self.status != 'published':
            return False
        
        return True
    
    def can_be_pinned_by(self, user):
        """Check can USER pin that post"""
        # focused on USER
        if not user or not user.is_authenticated:
            return False
        
        # post must be belong to user
        if self.author != user:
            return False
        
        # post must be published
        if self.status != 'published':
            return False
        
        # user must have active subscription
        if not hasattr(user, 'subscription') or not user.subscription.is_active:
            return False
        
        return True
    
    
    
    def increment_views(self):
        """Increments counts of Views"""
        self.views_count += 1
        self.save(update_fields=['views_count'])
        
        
    def get_pinned_info(self):
        """Returns info about pinned post"""
        if self.is_pinned:
            return {
                'is_pinned': True,
                'pinned_at': self.pin_info.pinned_at,
                'pinned_by': {
                    'id': self.pin_info.user.id,
                    'username': self.pin_info.user.username,
                    'has_active_subscription': self.pin_info.user.subscription.is_active()
                }
            }
            
        return {'is_pinned': False}
        

        
    
    