from rest_framework import viewsets
from api.models import Comment
from api.serializers import CommentSerializer
from api.services import ImageSerivce
from rest_framework.response import Response
from rest_framework import status
from django.contrib.staticfiles import finders


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        comment = serializer.save()

        service = ImageSerivce()
        service.generate_comment_image(comment)

        result = {
            'generated_image':
            f"posts/{comment.post.id}/comment_{comment.id}.png"
        }
        result.update(serializer.data)

        headers = self.get_success_headers(serializer.data)
        return Response(result,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        result = {
            'generated_image':
            f"posts/{instance.post.id}/comment_{instance.id}.png"
        }
        result.update(serializer.data)
        return Response(result)
