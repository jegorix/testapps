# Collect viws for API requests handling
from rest_framework import generics, status
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Note
from .serializers import NoteSerializer, NoteCreateSerialer, NoteUpdateSerializer
# Create your views here.

class NoteListCreateView(generics.ListCreateAPIView):
    # view for notes list and their creation
    queryset = Note.objects.all()
    
    def get_serializer_class(self):
        # returns appropiate serializer depends on request
        if self.request.method == 'POST':
            return NoteCreateSerialer
        
        return NoteSerializer
    
    def get(self, request, *args, **kwargs):
        # handle get request for getting notes list
        return super().get(self, request, *args, **kwargs)
            
            
class NoteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Note.objects.all()
    
    def get_serializer_class(self):
        # returns appropiate serializer depends on request
        if self.request.method in ['PUT', 'PATCH']:
            return NoteUpdateSerializer
        return NoteSerializer
    
    def update(self, request, *args, **kwargs):
        # Handle Note update with validation
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        # method to delete note
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Заметка успешно удалена'},
            status=status.HTTP_204_NO_CONTENT
        )