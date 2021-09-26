from rest_framework import serializers
from api.models import Post, Comment


class PostSerializer(serializers.Serializer):
    class Meta:
        model = Post
        fields = ('date_created', 'created_by', 'image_file',
                  'image_url', 'primary_text', 'bottom_text')


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = ('date_created', 'created_by', 'post',
                  'parent', 'primary_text', 'bottom_text')
