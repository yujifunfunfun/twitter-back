from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()
router.register('profile',views.ProfileViewSet, "profile")
router.register('posts', views.PostViewSet, "posts")
router.register('liked', views.LikedViewSet, "liked")
router.register('comment', views.CommentViewSet, "comment")


urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('users/me/', views.MyUserView.as_view(), name='user-me'),
    path('profiles/me/', views.MyProfileView.as_view(), name='profile-me'),
    path('posts/recommended/', views.RecommendPostListView.as_view(), name='posts-recommended'),

    path('',include(router.urls))
]