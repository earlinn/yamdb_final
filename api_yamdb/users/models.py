from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    email = models.EmailField(
        'email address',
        unique=True,
        error_messages={
            'unique': "email уже зарегистрирован",
        },
    )
    role = models.TextField(
        choices=(
            ("user", "user"), ("moderator", "moderator"), ("admin", "admin")
        ),
        default="user"
    )
    last_login = None
