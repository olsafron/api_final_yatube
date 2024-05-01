from django.urls import include, path
from django.urls.resolvers import URLResolver
from rest_framework.routers import DefaultRouter

from .views import FollowViewSet, GroupViewSet, PostViewSet, CommentViewSet

router = DefaultRouter()

router.register(
    r'posts', PostViewSet
)
router.register(
    r'groups', GroupViewSet
)
router.register(
    r'follow', FollowViewSet, basename='follow'
)
router.register(
    r'posts/(?P<post_id>\d+)/comments', CommentViewSet, basename='comment'
)


# Маршруты первой версии API.
v1_urlpatterns: list[URLResolver] = [
    path('', include(router.urls)),
    path('', include('djoser.urls.jwt')),
]

urlpatterns: list[URLResolver] = [
    path('v1/', include(v1_urlpatterns)),

]
