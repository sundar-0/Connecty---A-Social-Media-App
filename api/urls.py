from api.views import BlacklistTokenUpdateView
from django.views.generic import base
from votes.views import VoteViewSet
from comments.views import CommentViewSet
from posts.views import PostViewSet
from django.urls import path,include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from user_profile.views import ProfileViewSet
from friends.views import FriendViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
router = DefaultRouter()

urlpatterns=[
    path('token/',TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/blacklist/',BlacklistTokenUpdateView.as_view(),name="blacklist")
]

router.register(r'users', UserViewSet,basename='users')
router.register(r'profiles',ProfileViewSet)
router.register(r'posts',PostViewSet)
router.register(r'comments',CommentViewSet)
router.register(r'votes',VoteViewSet)
router.register(r'friends',FriendViewSet,basename='friends')
urlpatterns=urlpatterns+router.urls