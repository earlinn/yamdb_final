from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    APICategoryList, APICategoryDestroy, APIGenreList, APIGenreDestroy,
    CommentViewSet, ReviewViewSet, TitleViewSet
)

router = DefaultRouter()
router.register('titles', TitleViewSet)
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/categories/', APICategoryList.as_view()),
    path('v1/categories/<slug:slug>/', APICategoryDestroy.as_view()),
    path('v1/genres/', APIGenreList.as_view()),
    path('v1/genres/<slug:slug>/', APIGenreDestroy.as_view()),
    path('v1/', include(router.urls)),
]
