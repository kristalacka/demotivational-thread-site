from rest_framework import serializers
from api.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'date_created', 'created_by', 'post', 'parent',
                  'primary_text', 'bottom_text', 'generated_image')
