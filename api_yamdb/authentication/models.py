from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_ROLE = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )

    username = models.CharField(
        max_length=255,
        unique=True
    )
    email = models.EmailField(
        unique=True,
    )
    confirmation_code = models.CharField(
        max_length=500,
        blank=True
    )
    is_active = models.BooleanField(
        default=True
    )
    is_staff = models.BooleanField(
        default=False
    )
    role = models.CharField(
        max_length=20,
        blank=True,
        choices=USER_ROLE,
        default='user'
    )
    bio = models.CharField(
        max_length=200,
        blank=True
    )
    first_name = models.CharField(
        max_length=100,
        unique=False,
        blank=True
    )
    last_name = models.CharField(
        max_length=100,
        unique=False,
        blank=True
    )

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.username

    def get_short_name(self):
        return self.username

    @property
    def is_moderator(self):
        return self.role == 'moderator'

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_user(self):
        return self.role == 'user'

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
