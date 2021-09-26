from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Post, Comment
from api.serializers import PostSerializer, CommentSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @detail_route(methods=['post'])
    def upload_docs(request):
        try:
            file = request.data['file']
        except KeyError:
            raise ParseError('Request has no resource file attached')
        product = Product.objects.create(image=file, ....)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

# POST to post saves image
