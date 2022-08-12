from django.contrib.auth.models import AbstractUser
from django.db import models

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"

role_choices = [
    (USER, USER),
    (MODERATOR, MODERATOR),
    (ADMIN, ADMIN),
]


class User(AbstractUser):
    bio = models.TextField(
        'Биография',
        blank=True,
    )
