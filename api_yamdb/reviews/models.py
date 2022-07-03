from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .validators import validate_year

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    name = models.CharField(
        max_length=256
    )
    slug = models.SlugField(
        unique=True, max_length=50
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    name = models.CharField(
        max_length=256
    )
    year = models.PositiveIntegerField(
        validators=[validate_year],
        default=0
    )
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='title_category'
    )
    genre = models.ManyToManyField(
        Genre,
        blank=True,
        related_name='title_genre'
    )

    def __str__(self):
        return f'{self.category} - {self.name[:15]}'

    class Meta:
        ordering = ('-name',)
        verbose_name = 'Тайтл'
        verbose_name_plural = 'Тайтлы'


class Review(models.Model):
    text = models.TextField()
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='review_unique')
        ]
        ordering = ('-pub_date',)
        verbose_name = 'Рецензия'
        verbose_name_plural = 'Рецензии'


class Comment(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField(
        auto_now_add=True
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'text', 'review'),
                name='comment_unique')
        ]
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
