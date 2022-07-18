from django.db import models


class Category(models.Model):
    """Class to store categories of titles in the database."""
    name = models.CharField(
        'Category name',
        max_length=256,
        help_text='The type to which a title belongs'
    )
    slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Class to store genres of titles in the database."""
    name = models.CharField(
        'Genre name',
        max_length=256,
        help_text='The genre to which a title belongs'
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Class to store titles in the database."""
    name = models.TextField('Title of the work')
    year = models.IntegerField('Year of creation of the work')
    description = models.TextField(
        'Description of the work',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        related_name='titles',
        verbose_name='Genre of the title'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Category of the title'
    )

    def __str__(self):
        return self.name[:256]


class GenreTitle(models.Model):
    """Class to store many-to-many relationships between genres and titles."""
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)
    title = models.ForeignKey(Title, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.title} {self.genre}'
