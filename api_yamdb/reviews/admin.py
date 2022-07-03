from django.contrib import admin
from django.conf import settings as conf_settings

from .models import (
    Category,
    Genre,
    Title,
    Review,
    Comment,
)

EMPTY_VALUE_DISPLAY = conf_settings.EMPTY_VALUE_DISPLAY


class BaseAbstract(admin.ModelAdmin):
    """ Abstract class. """
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Category)
class CategoryAdmin(BaseAbstract):
    """Category."""
    pass


@admin.register(Genre)
class GenreAdmin(BaseAbstract):
    """Genre."""
    pass


@admin.register(Title)
class TitleAdmin(BaseAbstract):
    """Title."""
    list_display = ('name', 'description', 'category')


@admin.register(Review)
class ReviewAdmin(BaseAbstract):
    """Review."""
    list_display = ('pk', 'text', 'title', 'author')


@admin.register(Comment)
class CommentAdmin(BaseAbstract):
    """Review."""
    list_display = ('pk', 'text', 'review', 'author')
