from django.db import models
from django.contrib.auth.models import User
from django.core.files import File
import urllib


class Post(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User,  blank=True, null=True, on_delete=models.SET_NULL)
    image_file = models.ImageField(upload_to='images')
    image_url = models.CharField(max_length=255, unique=True)
    primary_text = models.CharField(max_length=100)
    bottom_text = models.CharField(max_length=200)


class Comment(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey(
        'self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    primary_text = models.CharField(max_length=100)
    bottom_text = models.CharField(max_length=200)
