from django.db import models
from django.contrib.auth.models import User
from api.models import Post
from django.conf import settings


def generated_name(instance, filename):
    return f'{settings.MEDIA_ROOT}/posts/{instance.post.id}/comment_{instance.id}.png'


class Comment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self',
                               blank=True,
                               null=True,
                               related_name='children',
                               on_delete=models.CASCADE)
    primary_text = models.CharField(max_length=100)
    bottom_text = models.CharField(max_length=200)
    generated_image = models.ImageField(upload_to=generated_name,
                                        blank=True,
                                        null=True)