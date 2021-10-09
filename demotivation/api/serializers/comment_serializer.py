from rest_framework import serializers
from api.models import Comment


class CommentSerializer(serializers.Serializer):
    class Meta:
        model = Comment
        fields = ('date_created', 'created_by', 'post', 'parent',
                  'primary_text', 'bottom_text')
