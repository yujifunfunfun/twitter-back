from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import uuid


class CustomUser(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        ordering = ['username']
    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="profile", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    profile_img = models.ImageField(blank=True, null=True)
    header_img = models.ImageField(blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name


class Connection(models.Model):
    follower = models.ForeignKey(Profile, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.follower.name, self.following.name)
# follower→フォローボタンを押した人


class Post(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='post',
        on_delete=models.CASCADE
    )
    text = models.TextField(blank=True, null=True)
    img = models.ImageField(blank=True, null=True)
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked',blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)
    reply_posts = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['posted_at']
    def __str__(self):
        return self.text


class Comment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='comment',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['commented_at']
    def __str__(self):
        return self.text
