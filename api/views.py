from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment, Playlist, AudioFeatures
from rest_framework.views import APIView
from rest_framework.response import Response
from .spotify import analyse_playlist, get_audio_features, search_audio_from_playlist
import re
from rest_framework import status

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .models import Connection, User
from .serializers import UserSerializer, ConnectionSerializer


"""フォロー"""
class FollowView(APIView):
    def post(self, request, format=None):
        follower_id = int(request.data.get('follower'))
        following_id = int(request.data.get('following'))
        follow_data = {'follower': follower_id, 'following': following_id}
        serializer = ConnectionSerializer(data=follow_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""フォロー解除"""
class UnfollowView(APIView):
    def post(self, request, format=None):
        follower_id = request.data.get('follower')
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






class CreateUserView(generics.CreateAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def perform_create(self, serializer):
        serializer.save(userProfile=self.request.user)


class MyProfileListView(generics.ListAPIView):
    queryset = Profile.objects.all()
    serializer_class = serializers.ProfileSerializer

    def get_queryset(self):
        return self.queryset.filter(userProfile=self.request.user)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(userPost=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def perform_create(self, serializer):
        serializer.save(userComment=self.request.user)


class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = serializers.PlaylistSerializer

    def perform_create(self, serializer):
        serializer.save(userPlaylist=self.request.user)


class MyPlaylistListView(generics.ListAPIView):
    queryset = Playlist.objects.all()
    serializer_class = serializers.PlaylistSerializer

    def get_queryset(self):
        return self.queryset.filter(userPlaylist=self.request.user)


class AudioFeaturesViewSet(viewsets.ModelViewSet):
    queryset = AudioFeatures.objects.all()
    serializer_class = serializers.AudioFeaturesSerializer

    def perform_create(self, serializer):
        serializer.save(playlist=self.request.POST["playlist"])


class PlaylistView(APIView):
    def get(self, request, playlist_id):
        audio_features_mean = analyse_playlist(playlist_id)
        playlist_url = "https://open.spotify.com/playlist/" + playlist_id
        anarysed_playlist = Playlist.objects.get(url=playlist_url)
        AudioFeatures.objects.update_or_create(playlist=anarysed_playlist, defaults={'acousticness': audio_features_mean[0], "danceability": audio_features_mean[1], "energy": audio_features_mean[2], "instrumentalness": audio_features_mean[3], "key": audio_features_mean[4], "danceability": audio_features_mean[1], "liveness": audio_features_mean[5], "loudness": audio_features_mean[6], "mode": audio_features_mean[7], "speechiness": audio_features_mean[8], "tempo": audio_features_mean[9], "time_signature": audio_features_mean[10], "valence": audio_features_mean[11]})

        return Response(audio_features_mean)


class AudioAnaliseView(APIView):
    def get(self, request, track_id):
        audio_features_list = []
        audio_features = get_audio_features(track_id)
        audio_features_list.append(round(audio_features['acousticness'] * 100))
        audio_features_list.append(round(audio_features['danceability'] * 100))
        audio_features_list.append(round(audio_features['energy'] * 100))
        audio_features_list.append(round(audio_features['instrumentalness'] * 100))
        audio_features_list.append(audio_features['key'])
        audio_features_list.append(round(audio_features['liveness'] * 100))
        audio_features_list.append(round(audio_features['loudness'], 2))
        audio_features_list.append(audio_features['mode'])
        audio_features_list.append(round(audio_features['speechiness'] * 100))
        audio_features_list.append(round(audio_features['tempo'], 2))
        audio_features_list.append(audio_features['time_signature'])
        audio_features_list.append(round(audio_features['valence'] * 100))

        return Response(audio_features_list)


class SearchAudioFromPlaylistView(APIView):
    def get(self, request, track_id, playlist_id):
        similar_audio_list = search_audio_from_playlist(track_id, playlist_id)

        return Response(similar_audio_list)


class MyFollowingListView(generics.ListAPIView):
    def get(self, request, myprofile_id, format=None):
        try:
            myprofile = Profile.objects.get(id=myprofile_id)
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
class FollowingListView(APIView):
    def get(self, request, user_id, format=None):
        try:
            user = Profile.objects.get(id=user_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)

        following_list = Connection.objects.filter(follower=user).values_list('following', flat=True)
        following_ids = list(following_list)

        return Response(following_ids)


# フォロワーのID
class FollowerListView(APIView):
    def get(self, request, user_id, format=None):
        try:
            user = Profile.objects.get(id=user_id)
        except Profile.DoesNotExist:
            return Response({'error': 'Invalid user ID'}, status=status.HTTP_404_NOT_FOUND)

        follower_list = Connection.objects.filter(following=user).values_list('follower', flat=True)
        follower_ids = list(follower_list)

        return Response(follower_ids)