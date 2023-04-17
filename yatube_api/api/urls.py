from rest_framework import routers
from django.urls import include, path

from .views import CommentViewSet, PostViewSet, GroupViewSet, FollowViewSet


router = routers.DefaultRouter()
router.register(r"posts/(?P<post_id>\d+)/comments", CommentViewSet,
                basename='comments')
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('djoser.urls.jwt')),
]
