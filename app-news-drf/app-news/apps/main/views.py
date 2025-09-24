from django.shortcuts import render
from rest_framework import generics, permissions, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404

from .models import Category, Post
from .serializers import (
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer,
    CategorySerializer,
)

from .permissions import IsAuthorOrReadOnly
# Create your views here.

class CategoryListCreateView(generics.ListCreateAPIView):
    """API endpoint for categories"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']
    
    
class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for specific category"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    

class PostListCreateView(generics.ListCreateAPIView):
    """API endpoint for posts with pinned post support.
        Pinned posts show first in order by pinning.
    """
    
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'status']
    search_fields = ['title', 'content']
    ordering_fields = ['-created_at', 'updated_at', 'views_count', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Returns posts, leans on permissons"""
        queryset = Post.objects.select_related('author', 'category')
        
        # filtration for rule access
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        else:
            queryset = queryset.filter(
                Q(status='published') | Q(author=self.request.user)
            )
            
        # checking whether sorting is necessary taking into account pinned posts
        ordering = self.request.query_params.get('ordering', '')
        show_pinned_first =  not ordering or ordering in ['-created_at', 'created_at']
        
        if show_pinned_first:
            return Post.get_posts_for_feed().filter(
                Q(status='published') | (
                Q(author=self.request.user) if self.request.user.is_authenticated else Q
                )
            )
        
        return queryset
    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return PostCreateUpdateSerializer
        return PostListSerializer
    
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Statistics about pinned posts
        if hasattr(response, 'data') and 'results' in response.data:
            pinned_count = sum(1 for post in response.data['results'] if post.get('is_pinned', False))
            response.data['pinned_posts_count'] = pinned_count
            
        return response
         
    
    
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    """API endpoint for specific Post"""
    queryset = Post.objects.select_related('author', 'category')
    serializer_class = PostDetailSerializer
    permission_classes = [IsAuthorOrReadOnly]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PostCreateUpdateSerializer
        return PostDetailSerializer
    
    def retrieve(self, request, *args, **kwargs): 
        """Increments viewers counter while GET request"""
        instance = self.get_object()
        
        if self.request.method == 'GET':
            instance.increment_views()
             
        serializer = self.get_serializer(instance) 
        
        return Response(serializer.data)
    
    
class MyPostView(generics.ListAPIView):
    """API endpoint of posts for specific user"""
    
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'author', 'status']
    search_fields = ['title', 'content']
    ordering_fields = ['-created_at', 'updated_at', 'views_count', 'title']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return Post.objects.filter(
            author = self.request.user,   
        ).select_related('author', 'category')
        
        
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def post_by_category(request, category_slug):
    """Posts of specific category"""
    category = get_object_or_404(Category, slug=category_slug)
    
    # Receive posts taking into account pinned posts
    # Use model manager for receiving with_subscription_info
    
    posts = Post.with_subscription_info().filter(
        category=category,
        status='published'
    )
    
    # Sort posts taking into account pinned posts
    # Use complex annotation for correct sorting
    from django.db.models import Case, When, Value, DateTimeField, BooleanField
    from django.utils import timezone
    
    posts = posts.annotate(
        
        effective_date=Case(
            When(
                pin_info__isnull=True,
                pin_info__user__subscription__status='active',
                pin_info__user__subscription__end_date_gt=timezone.now(),
                then='pin_info__pinned_at'
            ),
            default='created_at',
            output_field=DateTimeField()
        ),
        
        is_pinned_flag=Case(
            When(
                pin_info__isnull=True,
                pin_info__user__subscription__status='active',
                pin_info__user__subscription__end_date_gt=timezone.now(),
                then=Value(True)
            ),
            default=Value(False),
            output_field=BooleanField()
        )
    ).order_by('-is_pinned_flag', 'effective_date', '-created_at')
    
    
    serializer = PostListSerializer(posts, many=True, context={'request': request})
    
    return Response({
        'category': CategorySerializer(category).data,
        'posts': serializer.data,
        'pinned_posts_count': sum(1 for post in serializer.data if post.get('is_pinned', False))
    })
    
    
@api_view(['GET'])
@permission_classes([permissions.AllowAny]) 
def recent_posts(request):
    """10 recent published posts"""
    
    posts = Post.with_subscription_info().filter(
        status='published'
    ).order_by("-created_at")[:10]
    
    serializer = PostListSerializer(posts, many=True, context={'request': request})
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def popular_posts(request):
    """10 most popular posts"""
    
    posts = Post.with_subscription_info().filter(
        status='published'
    ).order_by("-views_count")[:10]
    
    serializer = PostListSerializer(posts, many=True, context={'request': request})
    
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def pinned_posts_only(request):
    """Receive only pinned posts"""
    posts = Post.objects.pinned_posts()
    serializer = PostListSerializer(posts, many=True, context={'request': request})
     
    return Response({
        'count': posts.count(),
        'results': serializer.data
    })


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def featured_posts(request):
    """
    Recomended posts for main page.
    - Pinned posts (max=3)
    - Popular posts by current week
    """
    
    from django.utils import timezone
    from datetime import timedelta
    
    # Receive 3 latest pinned posts
    pinned_posts = Post.objects.pinned_posts()[:3]
    
    # Receive popular posts by current week
    week_ago = timezone.now() - timedelta(days=7)
    
    popular_posts = Post.objects.with_subscription_info().filter(
        status='published',
        created_at__gte=week_ago,
    ).exclude(
        id__in=([post.id for post in pinned_posts])
    ).order_by('-views_count')[:6]
    
    pinned_serializer = PostListSerializer(
        pinned_posts,
        many=True,
        context={'request': request}
    )
    
    popular_serializer = PostListSerializer(
        popular_posts,
        many=True,
        context={'request': request}
    )
    
    return Response({
        'pinned_posts': pinned_serializer.data,
        'popular_posts': popular_serializer.data,
        'total_pinned': Post.objects.pinned_posts().count()
    })


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def toggle_post_pin_status(request, slug):
    """
    Toggle pinned post status.
    If post pinned - unpin, if unpinned - pin
    """
    
    post = get_object_or_404(Post, slug=slug, author=request.user, status='published')
    
    if not hasattr(request.user, 'subscription') or not request.user.subscription.is_active:
        return Response({
            'error': 'Active subscription required to pin posts.'
        }, status=status.HTTP_403_FORBIDDEN)
        
    try:
        from apps.subscribe.models import PinnedPost
        
        # Check if post pinned
        if post.is_pinned:
            # Unpin
            post.pin_info.delete()
            message = 'Post unpinned successfully'
            is_pinned = False
        else:
            # Delete user's pinned post if exists
            if hasattr(request.user, 'pinned_post'):
                request.user.pinned_post.delete()
                
            # Pin new post
            PinnedPost.objects.create(user=request.user, post=post)
            message = 'Post pinned successfully'
            is_pinned = True
            
        return Response({
            'message': message,
            'is_pinned': is_pinned,
            'post': PostDetailSerializer(post, context={'request': request}).data
        })
        
    except Exception as e:
        return Response({
            'error': str(e),
        }, status=status.HTTP_404_NOT_FOUND)