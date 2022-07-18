from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from titles.models import Title
from users.models import User


class Review(models.Model):
    """Class to store reviews in the database."""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Review title'
    )
    text = models.TextField(verbose_name='Content of review')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Review author'
    )
    score = models.IntegerField(
        'Score',
        default=1,
        validators=[MinValueValidator(1),
                    MaxValueValidator(10)]
    )
    pub_date = models.DateTimeField(
        'Date of publication',
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'author'),
                name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Class to store comments on reviews in the database."""
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Review'
    )
    text = models.TextField('Text of the comment')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Comment author'
    )
    pub_date = models.DateTimeField(
        'Date of publication',
        auto_now_add=True
    )

    def __str__(self):
        return self.text
