from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
import cloudinary
from cloudinary.models import CloudinaryField



class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email,
            password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email',
        max_length=50,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email


class Profile(models.Model):
    nickName = models.CharField(max_length=50)
    userProfile = models.OneToOneField(settings.AUTH_USER_MODEL, related_name="userProfile", on_delete=models.CASCADE)
    # img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)
    img = CloudinaryField('image', blank=True, null=True)
    fav_music_genre = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nickName


class Connection(models.Model):
    follower = models.ForeignKey(Profile, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(Profile, related_name='following', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} : {}".format(self.follower.nickName, self.following.nickName)
# follower→フォローボタンを押した人


class Playlist(models.Model):
    userPlaylist = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPlaylist',
        on_delete=models.CASCADE
    )
    title = models.CharField(max_length=100)
    url = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    userPost = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userPost',
        on_delete=models.CASCADE
    )
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    # img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    img = CloudinaryField('image', blank=True, null=True)
    playlist = models.ForeignKey(Playlist, related_name='Posts', on_delete=models.CASCADE,db_column='playlist_url', to_field='url')
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked',blank=True)
    genre = models.CharField(max_length=50)

    def __str__(self):
        return self.description


class Comment(models.Model):
    text = models.CharField(max_length=100)
    userComment = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='userComment',
        on_delete=models.CASCADE
    )
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.text


class AudioFeatures(models.Model):
    playlist = models.ForeignKey(
        Playlist, related_name='AudioFeatures',
        on_delete=models.CASCADE,
        db_column='playlist_url', to_field='url'
    )
    acousticness = models.FloatField()
    danceability = models.FloatField()
    energy = models.FloatField()
    instrumentalness = models.FloatField()
    key = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    mode = models.FloatField()
    speechiness = models.FloatField()
    tempo = models.FloatField()
    time_signature = models.FloatField()
    valence = models.FloatField()

    def __str__(self):
        return self.playlist.title