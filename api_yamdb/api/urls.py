from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (APICategoryDestroy, APICategoryList, APIGenreDestroy,
                    APIGenreList, CommentViewSet, ReviewViewSet, TitleViewSet)

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
    path('categories/', APICategoryList.as_view()),
    path('categories/<slug:slug>/', APICategoryDestroy.as_view()),
    path('genres/', APIGenreList.as_view()),
    path('genres/<slug:slug>/', APIGenreDestroy.as_view()),
    path('', include(router.urls)),
]
