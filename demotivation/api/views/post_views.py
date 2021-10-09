from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from api.models import Post
from api.serializers import PostSerializer
from api.services import ImageSerivce
from django.templatetags.static import static


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

        service = ImageSerivce()
        generated_image = service.generate_post_image(post)
        post.generated_image = generated_image
        post.save()

        headers = self.get_success_headers(serializer.data)

        result = {}
        result.update(serializer.data)
        return Response(result,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    # TODO override delete to remove images?
    # regenerate on update
    # Create auth
