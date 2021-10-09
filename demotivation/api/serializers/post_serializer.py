from rest_framework import serializers
from api.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'date_created', 'created_by', 'image_file',
                  'primary_text', 'bottom_text', 'generated_image')
