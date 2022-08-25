from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = "user"
    MODERATOR = "moderator"
    ADMIN = "admin"

    role_choices = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )

    email = models.EmailField("email address", unique=True, blank=False)
    bio = models.TextField(
        "Биография",
        blank=True,
    )
    role = models.TextField("Роль", choices=role_choices, default=USER)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser
