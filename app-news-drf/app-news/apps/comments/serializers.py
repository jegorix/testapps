from rest_framework import serializers
from .models import Comment
from apps.main.models import Post

class CommentSerializer(serializers.ModelSerializer):
    """Base serializer for comments"""
    author_info = serializers.SerializerMethodField()
    replies_count = serializers.SerializerMethodField()
    is_reply = serializers.ReadOnlyField()
    
    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'author_info', 'parent',
            'is_active', 'replies_count', 'is_reply',
            'created_at', 'updated_at'
        ]
        
        read_only_fields = ['author', 'is_active']
        
    def get_author_info(self, obj):
        return {
            'id': obj.author.id,
            'username': obj.author.username,
            'full_name': obj.author.full_name,
            'avatar': obj.author.avatar.url if obj.author.avatar else None,
        }
        
class CommentCreateSerializer(serializers.ModelSerializer):
    """Serializer for comments creation"""
    
    class Meta:
        model = Comment
        fields = ['post', 'parent', 'comment']
        
    def validate_post(self, value):
        if not Post.objects.filter(value.id, status='published').exists():
            raise serializers.ValidationError(
                'Post not found'
            )
        return value
        
    def validate_parent(self, value):
        if value and value.post != self.initial_data.get('post'):
            raise serializers.ValidationError(
                'Parrent comment must belong to the same post.'
            )
        return value

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
    
class CommentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating comments"""
    
    class Meta:
        model = Comment
        fields = ['content']
        
        
class CommentDetailSerializer(CommentSerializer):
    """Detail serializer for comments with replies"""
    
    replies = serializers.SerializerMethodField()
    
    class Meta(CommentSerializer.Meta):
        fields = CommentSerializer.Meta.fields + ['replies']
        
    def get_replies(self, obj):
        if obj.parent is None: # Show replies only for main comments
            replies = obj.replies.filter(is_active=True).order_by('created_at')
            return CommentSerializer(replies, many=True, context=self.context).data
        return []
            
    