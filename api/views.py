from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Connection
from django.db.models import Q


class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class MyUserView(APIView):
    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)


class MyProfileView(APIView):
    def get(self, request):
        profile = request.user.profile
        serializer = serializers.ProfileSerializer(profile)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # def create(self, request, *args, **kwargs):
    #     user_id = self.request.user.id
    #     data = request.data
    #     text = data.get('text', None)
    #     img = data.get('img', None)
    #     if text or img:
    #         post = Post.objects.create(user_id=user_id, text=text, img=img)
    #         return Response({"message": "投稿に成功しました"}, status=status.HTTP_201_CREATED)

    #     return Response({"error": "投稿を作成してください"}, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)


class RecommendPostListView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    def get_queryset(self):
        return Post.objects.all().order_by('-posted_at')[:10]


class LikedViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.LikedSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        post_id = self.request.query_params.get('post_id')
        if post_id:
            # Qオブジェクトを使用してor条件を作成
            queryset = Comment.objects.filter(post=post_id)
        else:
            queryset = Comment.objects.all()

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class MyFollowingListView(APIView):
    def get(self, request, format=None):
        userId=self.request.user

        try:
            myprofile = Profile.objects.get(user=userId)
        except Profile.DoesNotExist:
            return Response({'error': 'Invalid  ID'}, status=status.HTTP_404_NOT_FOUND)

        following_list = Connection.objects.filter(follower=myprofile).values_list('following', flat=True)
        following_ids = list(following_list)

        return Response(following_ids)


class MyFollowerListView(generics.ListAPIView):
    def get(self, request, myprofile_id, format=None):
        try:
            myprofile = Profile.objects.get(id=myprofile_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Invalid  ID'}, status=status.HTTP_404_NOT_FOUND)

        follower_list = Connection.objects.filter(following=myprofile).values_list('follower', flat=True)
        follower_ids = list(follower_list)

        return Response(follower_ids)


# フォローしてる人のID
class FollowingListView(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        profile_id = self.request.query_params.get('profile_id')
        userProfile = Profile.objects.get(id=profile_id)
        following_ids = Connection.objects.filter(follower=userProfile).values_list('following', flat=True)
        followingProfiles = Profile.objects.filter(id__in=following_ids)
        return followingProfiles


# フォロワーのID
class FollowerListView(generics.ListAPIView):
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        profile_id = self.request.query_params.get('profile_id')
        userProfile = Profile.objects.get(id=profile_id)
        follower_ids = Connection.objects.filter(following=userProfile).values_list('follower', flat=True)
        followerProfiles = Profile.objects.filter(id__in=follower_ids)
        return followerProfiles



"""フォロー"""
class FollowView(APIView):
    def post(self, request, format=None):
        follower_id = Profile.objects.get(user=self.request.user).id
        following_id = int(request.data.get('following'))
        follow_data = {'follower': follower_id, 'following': following_id}
        serializer = serializers.ConnectionSerializer(data=follow_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""フォロー解除"""
class UnfollowView(APIView):
    def post(self, request, format=None):
        follower_id = Profile.objects.get(user=self.request.user).id
        following_id = request.data.get('following')

        try:
            follower = Profile.objects.get(id=follower_id)
            following = Profile.objects.get(id=following_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)

        try:
            follow = Connection.objects.get(follower=follower, following=following)
        except Connection.DoesNotExist:
            return Response({'error': 'Follow relationship does not exist'}, status=status.HTTP_404_NOT_FOUND)

        follow.delete()

        return Response({'message': 'Unfollowed successfully'}, status=status.HTTP_200_OK)

