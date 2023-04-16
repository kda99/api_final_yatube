from rest_framework import routers
from rest_framework.authtoken import views
from django.urls import include, path

from .views import CommentViewSet, PostViewSet, GroupViewSet


router = routers.DefaultRouter()
router.register(r"posts/(?P<post_id>\d+)/comments", CommentViewSet,
                basename='comments')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')

urlpatterns = [
    path('api/v1/', include(router.urls)),
]
