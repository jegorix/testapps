from rest_framework import serializers
from blog.models import Post


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()
    
    def create(self, validated_data):
        return Comment(**validated_data)
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get("email", instance.email)
        instance.content = validated_data.get("content", instance.content)
        instance.created = validated_data.get("created", instance.created)
        return instance
    

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "author",
            "title",
            "body",
            "created",
        )
        
        model = Post