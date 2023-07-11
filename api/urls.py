from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'user'

router = DefaultRouter()
router.register('profile',views.ProfileViewSet, "profile")
router.register('post', views.PostViewSet, "post")
router.register('comment', views.CommentViewSet, "comment")
router.register('playlist', views.PlaylistViewSet, "playlist")
router.register('audio_features', views.AudioFeaturesViewSet, "audio_features")


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    path('myplaylist/', views.MyPlaylistListView.as_view(), name='myplaylist'),
    path('playlist/analyse/<str:playlist_id>/', views.PlaylistView.as_view(), name='playlist'),
    path('track/<str:track_id>/', views.AudioAnaliseView.as_view(), name='audio_analise'),
    path('search/<str:track_id>/<str:playlist_id>/', views.SearchAudioFromPlaylistView.as_view(), name='search_audio_from_playlist'),
    path('follow/', views.FollowView.as_view(), name='follow'),
    path('unfollow/', views.UnfollowView.as_view(), name='unfollow'),
    path('following/<int:user_id>/', views.FollowingListView.as_view(), name='following'),
    path('follower/<int:user_id>/', views.FollowerListView.as_view(), name='follower'),
    path('myfollowing/<int:myprofile_id>/', views.MyFollowingListView.as_view(), name='myfollowing'),
    path('myfollower/<int:myprofile_id>/', views.MyFollowerListView.as_view(), name='myfollower'),
    path('',include(router.urls))
]