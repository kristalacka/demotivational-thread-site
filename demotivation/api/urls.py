from django.urls import path, include
from api.models.post_model import Post
from api.views import PostViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
# TODO create nested router

urlpatterns = [path('', include(router.urls))]
