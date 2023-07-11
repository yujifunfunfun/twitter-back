
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment, Playlist, AudioFeatures, Connection


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ('id','email','password')
        extra_kwargs= {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model=Profile
        fields = ('id', 'nickName', 'userProfile', 'created_on', 'img', 'fav_music_genre')
        extra_kwargs = {'userProfile': {'read_only': True}}


class PostSerializer(serializers.ModelSerializer):
    created_on = serializers.DateTimeField(format="%Y-%m-%d", read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'description', 'userPost', 'created_on', 'img','liked', 'playlist', 'genre')
        extra_kwargs = {'userPost': {'read_only': True}}


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment','post')
        extra_kwargs = {'userComment': {'read_only': True}}


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ('id', 'userPlaylist', 'title', 'url')
        extra_kwargs = {'userPlaylist': {'read_only': True}}


class AudioFeaturesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFeatures
        fields = ('id', 'playlist', 'acousticness', 'danceability', 'energy', 'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence')


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'