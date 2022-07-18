import datetime as dt

from django.db.models import Avg
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Comment, Review
from titles.models import Category, Genre, GenreTitle, Title


class ReviewSerializer(serializers.ModelSerializer):
    """The serializer for the Review model."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        super().validate(data)
        if self.context['request'].method != 'POST':
            return data

        user = self.context['request'].user
        title_id = (
            self.context['request'].parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(author=user, title__id=title_id).exists():
            raise serializers.ValidationError(
                'Вы можете оставить только один отзыв на это произведение!'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """The serializer for the Comment model."""
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class CategorySerializer(serializers.ModelSerializer):
    """The serializer for the Category model."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """The serializer for the Genre model."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """The serializer for the Title model (post, patch, delete)."""
    category = SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all())
    genre = SlugRelatedField(
        slug_field='slug', queryset=Genre.objects.all(), many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def validate_year(self, value):
        year = dt.date.today().year
        if value > year:
            raise serializers.ValidationError(
                'Год создания произведения не может быть больше текущего года!'
            )
        return value

    def create(self, validated_data):
        genres = validated_data.pop('genre')
        if genres == []:
            raise serializers.ValidationError(
                'Список жанров не может быть пустым!'
            )
        title = Title.objects.create(**validated_data)
        for genre in genres:
            GenreTitle.objects.create(genre=genre, title=title)
        return title


class TitleListAndRetrieveSerializer(serializers.ModelSerializer):
    """The serializer to list and retrieve Title objects."""
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = '__all__'

    def get_rating(self, obj):
        title_reviews = obj.reviews.all()
        rating = title_reviews.aggregate(Avg('score'))['score__avg']
        return rating
