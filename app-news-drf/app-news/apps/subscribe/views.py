from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone

from .models import Subscription, SubscriptionPlan, SubscriptionHistory, PinnedPost
from .serializers import (
    SubscriptionSerializer,
    SubscriptionCreateSerializer,
    SubscriptionPlanSerializer,
    SubscriptionHistorySerializer,
    UserSubscriptionStatusSerializer,
    PinnedPostSerializer,
    UnPinPostSerializer,
    PinPostSerializer
)
from apps.main.models import Post

# Create your views here.

class SubscriptionPlanListView(generics.ListAPIView):
    """List of available tariff plans"""
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]
    


class SubscriptionPlanDetailView(generics.RetrieveAPIView):
    """Detail information about tariff plan"""
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]
    
    

class UserSubscriptionView(generics.RetrieveAPIView):
    """Info about current user subscription"""
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Returns user's subscription or None"""
        try:
            return self.request.user.subscription
        except Subscription.DoesNotExist:
            return None
    
    def retreive(self, request):
        """Returns INFO about subscription"""
        subscription = self.get_object()
        if subscription:
            serializer = self.get_serializer(subscription)
            return Response(serializer.data)
        else:
            return Response({
                'detail': 'No subscription found.'
            }, status=status.HTTP_404_NOT_FOUND )

    
class SubscriptionHistoryView(generics.ListAPIView):
    """History of changes user's subscription"""
    serializer_class = SubscriptionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Returns user's subscription history"""
        try:
            subscription = self.request.user.subscription
            return subscription.history.all()
        except Subscription.DoesNotExist:
            return SubscriptionHistory.objects.none()
    
   
    
class PinnedPostView(generics.RetrieveUpdateDestroyAPIView):
    """Manage pinned user post"""
    serializer_class = PinnedPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Returns user's pinned post"""
        try:
            return self.request.user.pinned_post
        except PinnedPost.DoesNotExist:
            return None
        
    def retrieve(self, request):
        """Returns INFO about pinned post"""
        pinned_post = self.get_object()
        if pinned_post:
            serializer = self.get_serializer(pinned_post)
            return Response(serializer.data)
        else:
            return Response({
                'detail': 'No pinned post found.'
            }, status=status.HTTP_404_NOT_FOUND)
            
    def update(self, request, *args, **kwargs):
        """Update pinned post"""
        # Checking subscription
        if not hasattr(request.user, 'subscription') or not request.user.subscription.is_active:
            return Response({
                'error': 'Active subscription required to pin posts.'
            }, status=status.HTTP_403_FORBIDDEN)
            
        return super().update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """Delete pinned post"""
        pinned_post = self.get_object()
        if pinned_post:
            pinned_post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({
                'detail': 'No pinned post found.'
            }, status=status.HTTP_404_NOT_FOUND)
            
    
