from rest_framework import routers
from django.urls import include, path

from .views import CommentViewSet, PostViewSet, GroupViewSet, FollowViewSet


router = routers.DefaultRouter()
router.register(r"posts/(?P<post_id>\d+)/comments", CommentViewSet,
                basename='comments')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
