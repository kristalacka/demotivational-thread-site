from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import ParseError
from rest_framework.response import Response
from rest_framework import status

from api.models import Post
from api.serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def create(self, request, *args, **kwargs):
        image_file = request.data.pop('image_file')
        serializer = PostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        post = serializer.save()
        post.image_file = image_file[0]
        post.save()
        return Response({'success': 'true'})

    # TODO override delete to remove images, make retrieve request get public image url or just generate different image based on post
    # Create auth
