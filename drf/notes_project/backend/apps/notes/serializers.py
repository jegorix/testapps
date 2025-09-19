# Determine serializers for Note model
from rest_framework import serializers
from django.utils.html import escape
from .models import Note

class NoteSerializer(serializers.ModelSerializer):
    # Base serializer for Note model
    class Meta:
        model = Note
        fields = ['id', 'title', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
        
    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError('Заголовок не может быть пустым')
        return escape(value.strip())
        
    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError('Содержание не может быть пустым')
        return escape(value.strip())
    
class NoteCreateSerialer(NoteSerializer):
    pass

class NoteUpdateSerializer(NoteSerializer):
    title = serializers.CharField(required=False)
    content = serializers.CharField(required=False)