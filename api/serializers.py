
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment, Connection


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = '__all__'
        extra_kwargs= {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    follower_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()

    class Meta:
        model=Profile
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}
    def get_post_count(self, obj):
        return obj.user.post.count()
    def get_follower_count(self, obj):
        return obj.follower.count()
    def get_following_count(self, obj):
        return obj.following.count()


class CommentSerializer(serializers.ModelSerializer):
    img = serializers.ImageField(source='user.profile.img', read_only=True)
    name = serializers.CharField(source='user.profile.name', read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class PostSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.profile.name', read_only=True)
    profile_id = serializers.CharField(source='user.profile.id', read_only=True)
    profile_img = serializers.ImageField(source='user.profile.profile_img', read_only=True)
    comments = CommentSerializer(many=True, source='user', read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

class PostsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    name = serializers.CharField(source='user.profile.name', read_only=True)
    profile_id = serializers.CharField(source='user.profile.id', read_only=True)
    profile_img = serializers.ImageField(source='user.profile.profile_img', read_only=True)
    comment_count = serializers.SerializerMethodField()
    posted_at = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}

    def get_comment_count(self, obj):
        return obj.comment.count()
    def get_posted_at(self, obj):
        return obj.posted_at.strftime('%m月%d日')

class LikedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('liked')
        extra_kwargs = {'user': {'read_only': True}}



class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = '__all__'
