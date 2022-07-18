from django_filters import rest_framework as rf_filters
from rest_framework import filters, generics, viewsets
from django.shortcuts import get_object_or_404

from reviews.models import Comment, Review
from titles.models import Category, Genre, Title
from .mixins import ReviewCommentMixin
from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer, CommentSerializer,
    GenreSerializer, ReviewSerializer,
    TitleSerializer, TitleListAndRetrieveSerializer
)


class ReviewViewSet(ReviewCommentMixin):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        queryset = Review.objects.filter(title__id=self.kwargs.get('title_id'))
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(ReviewCommentMixin):
    serializer_class = CommentSerializer

    def get_queryset(self):
        queryset = Comment.objects.filter(
            review__id=self.kwargs.get('review_id')
        )
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, pk=review_id, title__id=title_id)
        serializer.save(author=self.request.user, review=review)


class APICategoryList(generics.ListCreateAPIView):
    """APIView for creating and listing categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class APICategoryDestroy(generics.DestroyAPIView):
    """APIView for destruction categories."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'slug'


class APIGenreList(generics.ListCreateAPIView):
    """APIView for creating and listing genres."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ('name',)


class APIGenreDestroy(generics.DestroyAPIView):
    """APIView for destruction genres."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    lookup_field = 'slug'


class TitleFilter(rf_filters.FilterSet):
    """Class for filtering titles."""

    category = rf_filters.CharFilter(field_name='category__slug')
    genre = rf_filters.CharFilter(field_name='genre__slug')
    name = rf_filters.CharFilter(field_name='name', lookup_expr='icontains')
    year = rf_filters.NumberFilter(field_name='year')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'name', 'year']


class TitleViewSet(viewsets.ModelViewSet):
    """Viewset for reading, creating, modifying and deleting titles."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    filter_backends = (rf_filters.DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleListAndRetrieveSerializer
        return TitleSerializer
