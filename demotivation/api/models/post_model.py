from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


def post_name(instance, filename):
    return f'{settings.MEDIA_ROOT}/posts/{instance.id}/base.png'


def generated_name(instance, filename):
    return f'{settings.MEDIA_ROOT}/posts/{instance.id}/generated.png'


class Post(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL)
    image_file = models.ImageField(upload_to=post_name, blank=True, null=True)
    generated_image = models.ImageField(upload_to=generated_name,
                                        blank=True,
                                        null=True)
    primary_text = models.CharField(max_length=100)
    bottom_text = models.CharField(max_length=200)
