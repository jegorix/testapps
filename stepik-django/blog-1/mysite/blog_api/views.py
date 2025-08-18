from django.http import Http404
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics

from blog.models import Post
from .serializers import PostSerializer
# Create your views here.

class PostList(mixins.ListModelMixin,
               mixins.CreateModelMixin,
               generics.GenericAPIView):
    
        queryset = Post.objects.all()
        serializer_class = PostSerializer
        
        def get(self, request, *args, **kwargs):
            return self.list(request, *args, **kwargs)
        
        def post(self, request, *args, **kwargs):
            return self.create(request, *args, **kwargs)
        
        
class PostDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
        
    
    
    
    
    
    
    
    
    

# class PostDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Post.objects.get(id=pk)
#         except Post.DoesNotExist:
#             raise Http404
        
#     def get(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
#     def patch(self, request, pk, format=None):
#         post = self.get_object(pk)
#         serializer = PostSerializer(post, data=request.data, partial=True)
            
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         queryset = self.get_object(pk)
#         queryset.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)